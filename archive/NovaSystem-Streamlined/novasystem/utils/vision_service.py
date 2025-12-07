"""
Vision Service for NovaSystem.

Uses Gemini's multimodal capabilities for image understanding:
- Image captioning
- Visual question answering
- Object detection with bounding boxes
- Segmentation masks
- Multi-image analysis

Requires: pip install google-genai Pillow
"""

import os
import sys
import base64
import asyncio
import json
import io
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union, Tuple, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

# Attempt to import google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    types = None

# Attempt to import PIL
try:
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None
    ImageDraw = None
    np = None

logger = logging.getLogger(__name__)


def vision_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a vision service event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [VISION/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


@dataclass
class BoundingBox:
    """A detected object with bounding box."""
    label: str
    x1: int  # Left
    y1: int  # Top
    x2: int  # Right
    y2: int  # Bottom
    confidence: Optional[float] = None

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "box": [self.x1, self.y1, self.x2, self.y2],
            "width": self.width,
            "height": self.height
        }


@dataclass
class SegmentationMask:
    """A segmentation mask for an object."""
    label: str
    box: BoundingBox
    mask: "Image.Image"  # Binary mask image

    def to_overlay(
        self,
        original_image: "Image.Image",
        color: Tuple[int, int, int, int] = (255, 0, 0, 128)
    ) -> "Image.Image":
        """Create an overlay of the mask on the original image."""
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available")

        # Create RGBA overlay
        overlay = Image.new('RGBA', original_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Resize mask to bounding box size
        mask_resized = self.mask.resize(
            (self.box.width, self.box.height),
            Image.Resampling.BILINEAR
        )
        mask_array = np.array(mask_resized)

        # Apply mask
        for y in range(self.box.y1, self.box.y2):
            for x in range(self.box.x1, self.box.x2):
                if mask_array[y - self.box.y1, x - self.box.x1] > 127:
                    draw.point((x, y), fill=color)

        # Composite
        return Image.alpha_composite(original_image.convert('RGBA'), overlay)


@dataclass
class VisionResult:
    """Result from a vision analysis."""
    text: str
    objects: List[BoundingBox] = field(default_factory=list)
    segments: List[SegmentationMask] = field(default_factory=list)
    raw_response: Optional[str] = None


class VisionService:
    """
    Service for analyzing images with Gemini.

    Features:
    - Image captioning and description
    - Visual question answering
    - Object detection with bounding boxes
    - Segmentation masks
    - Multi-image comparison

    Usage:
        service = VisionService()

        # Caption an image
        result = await service.caption("photo.jpg")
        print(result.text)

        # Ask about an image
        result = await service.ask("What color is the car?", "car.jpg")

        # Detect objects
        result = await service.detect_objects("scene.jpg")
        for obj in result.objects:
            print(f"{obj.label}: {obj.x1},{obj.y1} -> {obj.x2},{obj.y2}")

        # Segment objects
        result = await service.segment("room.jpg", "wooden and glass items")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash"
    ):
        """
        Initialize the vision service.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model to use (gemini-2.5-flash, gemini-2.5-pro, etc.)
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            )

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        vision_log("✅", "INIT", f"VisionService initialized with {model}")

    def _load_image(self, image: Union[str, Path, bytes, "Image.Image"]) -> "Image.Image":
        """Load an image from various sources."""
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available. Install with: pip install Pillow")

        if isinstance(image, (str, Path)):
            path = Path(image)
            if not path.exists():
                raise FileNotFoundError(f"Image not found: {path}")
            return Image.open(path)
        elif isinstance(image, bytes):
            return Image.open(io.BytesIO(image))
        elif hasattr(image, 'mode'):  # PIL Image
            return image
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")

    def _prepare_image(self, image: "Image.Image", max_size: int = 1024) -> "Image.Image":
        """Resize image if needed."""
        img = image.copy()
        img.thumbnail([max_size, max_size], Image.Resampling.LANCZOS)
        return img

    async def caption(
        self,
        image: Union[str, Path, bytes, "Image.Image"],
        style: str = "descriptive"
    ) -> VisionResult:
        """
        Generate a caption for an image.

        Args:
            image: Image to caption
            style: Caption style (descriptive, brief, technical, creative)

        Returns:
            VisionResult with the caption text
        """
        vision_log("📝", "CAPTION", f"Generating {style} caption")

        pil_image = self._load_image(image)
        pil_image = self._prepare_image(pil_image)

        prompts = {
            "descriptive": "Describe this image in detail.",
            "brief": "Provide a brief, one-sentence caption for this image.",
            "technical": "Describe the technical aspects of this image (composition, lighting, colors, etc.)",
            "creative": "Write a creative, evocative caption for this image."
        }
        prompt = prompts.get(style, prompts["descriptive"])

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=[pil_image, prompt]
            )
        )

        vision_log("✅", "CAPTION", f"Caption generated ({len(response.text)} chars)")
        return VisionResult(text=response.text, raw_response=response.text)

    async def ask(
        self,
        question: str,
        image: Union[str, Path, bytes, "Image.Image"]
    ) -> VisionResult:
        """
        Ask a question about an image.

        Args:
            question: The question to ask
            image: The image to analyze

        Returns:
            VisionResult with the answer
        """
        vision_log("❓", "ASK", f"Question: {question[:50]}...")

        pil_image = self._load_image(image)
        pil_image = self._prepare_image(pil_image)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=[pil_image, question]
            )
        )

        vision_log("✅", "ASK", f"Answer received ({len(response.text)} chars)")
        return VisionResult(text=response.text, raw_response=response.text)

    async def detect_objects(
        self,
        image: Union[str, Path, bytes, "Image.Image"],
        target: Optional[str] = None
    ) -> VisionResult:
        """
        Detect objects in an image and return bounding boxes.

        Args:
            image: Image to analyze
            target: Optional specific target (e.g., "green objects", "people")

        Returns:
            VisionResult with detected objects
        """
        vision_log("🔍", "DETECT", f"Detecting objects" + (f" ({target})" if target else ""))

        pil_image = self._load_image(image)
        pil_image = self._prepare_image(pil_image)
        width, height = pil_image.size

        if target:
            prompt = f"Detect all {target} in the image. "
        else:
            prompt = "Detect all prominent items in the image. "

        prompt += "Return a JSON array where each object has 'label' (string) and 'box_2d' ([ymin, xmin, ymax, xmax] normalized to 0-1000)."

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=[pil_image, prompt],
                config=config
            )
        )

        # Parse JSON response
        try:
            data = json.loads(response.text)
            objects = []
            for item in data:
                box = item.get("box_2d", [])
                if len(box) >= 4:
                    # Convert normalized coords to absolute
                    y1 = int(box[0] / 1000 * height)
                    x1 = int(box[1] / 1000 * width)
                    y2 = int(box[2] / 1000 * height)
                    x2 = int(box[3] / 1000 * width)

                    objects.append(BoundingBox(
                        label=item.get("label", "unknown"),
                        x1=x1, y1=y1, x2=x2, y2=y2
                    ))

            vision_log("✅", "DETECT", f"Found {len(objects)} objects")
            return VisionResult(
                text=f"Detected {len(objects)} objects",
                objects=objects,
                raw_response=response.text
            )

        except json.JSONDecodeError as e:
            vision_log("⚠️", "DETECT", f"JSON parse error: {e}")
            return VisionResult(text=response.text, raw_response=response.text)

    async def segment(
        self,
        image: Union[str, Path, bytes, "Image.Image"],
        target: str
    ) -> VisionResult:
        """
        Segment specific objects in an image.

        Args:
            image: Image to analyze
            target: What to segment (e.g., "wooden and glass items")

        Returns:
            VisionResult with segmentation masks
        """
        vision_log("✂️", "SEGMENT", f"Segmenting: {target}")

        pil_image = self._load_image(image)
        pil_image = self._prepare_image(pil_image)
        width, height = pil_image.size

        prompt = f"""
        Give the segmentation masks for {target}.
        Output a JSON list where each entry contains:
        - "box_2d": [ymin, xmin, ymax, xmax] normalized to 0-1000
        - "mask": base64 encoded PNG of the segmentation mask
        - "label": descriptive text label
        """

        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=[pil_image, prompt],
                config=config
            )
        )

        # Parse response
        try:
            # Clean up JSON if wrapped in markdown
            json_text = response.text
            if "```json" in json_text:
                json_text = json_text.split("```json")[1].split("```")[0]
            elif "```" in json_text:
                json_text = json_text.split("```")[1].split("```")[0]

            data = json.loads(json_text)
            segments = []

            for item in data:
                box = item.get("box_2d", [])
                mask_b64 = item.get("mask", "")

                if len(box) >= 4 and mask_b64:
                    # Convert coords
                    y1 = int(box[0] / 1000 * height)
                    x1 = int(box[1] / 1000 * width)
                    y2 = int(box[2] / 1000 * height)
                    x2 = int(box[3] / 1000 * width)

                    # Skip invalid boxes
                    if y1 >= y2 or x1 >= x2:
                        continue

                    bbox = BoundingBox(
                        label=item.get("label", "unknown"),
                        x1=x1, y1=y1, x2=x2, y2=y2
                    )

                    # Decode mask
                    if mask_b64.startswith("data:image/png;base64,"):
                        mask_b64 = mask_b64[22:]

                    try:
                        mask_data = base64.b64decode(mask_b64)
                        mask_img = Image.open(io.BytesIO(mask_data))

                        segments.append(SegmentationMask(
                            label=item.get("label", "unknown"),
                            box=bbox,
                            mask=mask_img
                        ))
                    except Exception as e:
                        vision_log("⚠️", "SEGMENT", f"Mask decode error: {e}")

            vision_log("✅", "SEGMENT", f"Found {len(segments)} segments")
            return VisionResult(
                text=f"Segmented {len(segments)} objects",
                segments=segments,
                raw_response=response.text
            )

        except json.JSONDecodeError as e:
            vision_log("⚠️", "SEGMENT", f"JSON parse error: {e}")
            return VisionResult(text=response.text, raw_response=response.text)

    async def compare(
        self,
        images: List[Union[str, Path, bytes, "Image.Image"]],
        question: Optional[str] = None
    ) -> VisionResult:
        """
        Compare multiple images.

        Args:
            images: List of images to compare
            question: Optional specific comparison question

        Returns:
            VisionResult with comparison analysis
        """
        vision_log("🔄", "COMPARE", f"Comparing {len(images)} images")

        pil_images = [self._prepare_image(self._load_image(img)) for img in images]

        if question:
            prompt = question
        else:
            prompt = "What are the differences and similarities between these images?"

        contents = pil_images + [prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        vision_log("✅", "COMPARE", f"Comparison complete")
        return VisionResult(text=response.text, raw_response=response.text)

    async def analyze(
        self,
        image: Union[str, Path, bytes, "Image.Image"],
        aspects: List[str] = None
    ) -> VisionResult:
        """
        Perform comprehensive analysis of an image.

        Args:
            image: Image to analyze
            aspects: Specific aspects to analyze (colors, composition, mood, etc.)

        Returns:
            VisionResult with detailed analysis
        """
        vision_log("🔬", "ANALYZE", "Performing comprehensive analysis")

        pil_image = self._load_image(image)
        pil_image = self._prepare_image(pil_image)

        aspects_list = aspects or ["composition", "colors", "mood", "objects", "style"]
        prompt = f"""Analyze this image comprehensively, covering these aspects:
{chr(10).join(f'- {aspect}' for aspect in aspects_list)}

Provide detailed observations for each aspect."""

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=[pil_image, prompt]
            )
        )

        vision_log("✅", "ANALYZE", f"Analysis complete ({len(response.text)} chars)")
        return VisionResult(text=response.text, raw_response=response.text)

    def draw_boxes(
        self,
        image: Union[str, Path, bytes, "Image.Image"],
        boxes: List[BoundingBox],
        output_path: Optional[str] = None
    ) -> "Image.Image":
        """
        Draw bounding boxes on an image.

        Args:
            image: Original image
            boxes: List of bounding boxes to draw
            output_path: Optional path to save annotated image

        Returns:
            Annotated PIL Image
        """
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available")

        pil_image = self._load_image(image).convert("RGB")
        draw = ImageDraw.Draw(pil_image)

        # Colors for different objects
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (128, 0, 0), (0, 128, 0), (0, 0, 128)
        ]

        for i, box in enumerate(boxes):
            color = colors[i % len(colors)]
            draw.rectangle(
                [box.x1, box.y1, box.x2, box.y2],
                outline=color,
                width=3
            )
            draw.text(
                (box.x1, max(0, box.y1 - 15)),
                box.label,
                fill=color
            )

        if output_path:
            pil_image.save(output_path)
            vision_log("💾", "DRAW", f"Saved annotated image to {output_path}")

        return pil_image


# Quick access functions

async def caption_image(image_path: str, style: str = "descriptive") -> str:
    """Quick function to caption an image."""
    service = VisionService()
    result = await service.caption(image_path, style)
    return result.text


async def ask_about_image(question: str, image_path: str) -> str:
    """Quick function to ask about an image."""
    service = VisionService()
    result = await service.ask(question, image_path)
    return result.text


async def detect_in_image(
    image_path: str,
    target: Optional[str] = None,
    annotate: bool = False,
    output_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Quick function to detect objects in an image.

    Args:
        image_path: Path to image
        target: Optional specific target
        annotate: Whether to save annotated image
        output_path: Path for annotated image

    Returns:
        List of detected objects as dicts
    """
    service = VisionService()
    result = await service.detect_objects(image_path, target)

    if annotate and result.objects:
        service.draw_boxes(
            image_path,
            result.objects,
            output_path or "detected_objects.png"
        )

    return [obj.to_dict() for obj in result.objects]
