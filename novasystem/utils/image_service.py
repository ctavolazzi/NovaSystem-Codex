"""
Image Generation Service for NovaSystem.

Uses Gemini's native image generation capabilities:
- gemini-2.5-flash-image: Fast, efficient (1024px max)
- gemini-3-pro-image-preview: Advanced, up to 4K, thinking mode

Requires: pip install google-genai Pillow
"""

import os
import sys
import base64
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Attempt to import google-genai for image generation
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    types = None

# Attempt to import PIL for image handling
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None

logger = logging.getLogger(__name__)


def img_log(emoji: str, category: str, message: str, details: dict = None):
    """Log an image service event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [IMG/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


class ImageModel(Enum):
    """Available Gemini image generation models."""
    FLASH = "gemini-2.5-flash-image"  # Fast, efficient
    PRO = "gemini-3-pro-image-preview"  # Advanced, 4K capable


class AspectRatio(Enum):
    """Supported aspect ratios for image generation."""
    SQUARE = "1:1"
    PORTRAIT_2_3 = "2:3"
    LANDSCAPE_3_2 = "3:2"
    PORTRAIT_3_4 = "3:4"
    LANDSCAPE_4_3 = "4:3"
    PORTRAIT_4_5 = "4:5"
    LANDSCAPE_5_4 = "5:4"
    VERTICAL_9_16 = "9:16"
    WIDESCREEN_16_9 = "16:9"
    ULTRAWIDE_21_9 = "21:9"


class ImageSize(Enum):
    """Output image sizes (Pro model only)."""
    ONE_K = "1K"
    TWO_K = "2K"
    FOUR_K = "4K"


@dataclass
class GeneratedImage:
    """Container for a generated image."""
    data: bytes
    mime_type: str = "image/png"
    text_response: Optional[str] = None

    def save(self, path: Union[str, Path]) -> Path:
        """Save the image to a file."""
        path = Path(path)
        path.write_bytes(self.data)
        img_log("💾", "SAVE", f"Image saved to {path}")
        return path

    def to_pil(self) -> "Image.Image":
        """Convert to PIL Image."""
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available. Install with: pip install Pillow")
        from io import BytesIO
        return Image.open(BytesIO(self.data))

    def to_base64(self) -> str:
        """Get base64 encoded string."""
        return base64.b64encode(self.data).decode('utf-8')


class ImageService:
    """
    Service for generating and editing images with Gemini.

    Features:
    - Text-to-image generation
    - Image editing (with text prompts)
    - Style transfer
    - Multi-image composition
    - Multi-turn conversational editing

    Usage:
        service = ImageService()

        # Generate an image
        result = await service.generate("A sunset over mountains")
        result.save("sunset.png")

        # Edit an image
        result = await service.edit(
            "Add a castle on the hill",
            input_image="landscape.png"
        )
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image service.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            )

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        # Initialize the client
        self.client = genai.Client(api_key=self.api_key)
        img_log("✅", "INIT", "ImageService initialized")

    async def generate(
        self,
        prompt: str,
        model: ImageModel = ImageModel.FLASH,
        aspect_ratio: AspectRatio = AspectRatio.SQUARE,
        size: Optional[ImageSize] = None,
        include_text: bool = True
    ) -> GeneratedImage:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            model: Which Gemini image model to use
            aspect_ratio: Aspect ratio for the output image
            size: Image size (Pro model only: 1K, 2K, 4K)
            include_text: Whether to include text in response

        Returns:
            GeneratedImage with the generated image data
        """
        img_log("🎨", "GENERATE", f"Generating image", {
            "prompt_preview": prompt[:60],
            "model": model.value,
            "aspect_ratio": aspect_ratio.value
        })

        # Build config
        config_dict = {
            "response_modalities": ["TEXT", "IMAGE"] if include_text else ["IMAGE"]
        }

        image_config = {"aspect_ratio": aspect_ratio.value}
        if size and model == ImageModel.PRO:
            image_config["image_size"] = size.value

        config_dict["image_config"] = types.ImageConfig(**image_config)
        config = types.GenerateContentConfig(**config_dict)

        # Generate (run sync call in executor)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=model.value,
                contents=[prompt],
                config=config
            )
        )

        return self._parse_response(response)

    async def edit(
        self,
        prompt: str,
        input_image: Union[str, Path, bytes, "Image.Image"],
        model: ImageModel = ImageModel.FLASH,
        aspect_ratio: Optional[AspectRatio] = None
    ) -> GeneratedImage:
        """
        Edit an existing image with a text prompt.

        Args:
            prompt: Instructions for editing the image
            input_image: Path to image, bytes, or PIL Image
            model: Which Gemini image model to use
            aspect_ratio: Optional aspect ratio override

        Returns:
            GeneratedImage with the edited image
        """
        img_log("✏️", "EDIT", f"Editing image", {
            "prompt_preview": prompt[:60],
            "model": model.value
        })

        # Load input image
        pil_image = self._load_image(input_image)

        # Build config
        config_dict = {"response_modalities": ["TEXT", "IMAGE"]}
        if aspect_ratio:
            config_dict["image_config"] = types.ImageConfig(
                aspect_ratio=aspect_ratio.value
            )
        config = types.GenerateContentConfig(**config_dict)

        # Generate
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=model.value,
                contents=[prompt, pil_image],
                config=config
            )
        )

        return self._parse_response(response)

    async def compose(
        self,
        prompt: str,
        images: List[Union[str, Path, bytes, "Image.Image"]],
        model: ImageModel = ImageModel.PRO,
        aspect_ratio: AspectRatio = AspectRatio.SQUARE,
        size: ImageSize = ImageSize.TWO_K
    ) -> GeneratedImage:
        """
        Compose a new image from multiple input images.

        Args:
            prompt: Instructions for composition
            images: List of input images (up to 14 for Pro model)
            model: Which model to use (Pro recommended for multi-image)
            aspect_ratio: Aspect ratio for output
            size: Image size (Pro model)

        Returns:
            GeneratedImage with the composed result
        """
        max_images = 14 if model == ImageModel.PRO else 3
        if len(images) > max_images:
            raise ValueError(f"Maximum {max_images} images for {model.value}")

        img_log("🖼️", "COMPOSE", f"Composing from {len(images)} images", {
            "prompt_preview": prompt[:60],
            "model": model.value
        })

        # Load all images
        pil_images = [self._load_image(img) for img in images]

        # Build contents
        contents = [prompt] + pil_images

        # Build config
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio.value,
                image_size=size.value if model == ImageModel.PRO else None
            )
        )

        # Generate
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=model.value,
                contents=contents,
                config=config
            )
        )

        return self._parse_response(response)

    async def style_transfer(
        self,
        content_image: Union[str, Path, bytes, "Image.Image"],
        style_description: str,
        model: ImageModel = ImageModel.FLASH
    ) -> GeneratedImage:
        """
        Apply a style transformation to an image.

        Args:
            content_image: The image to transform
            style_description: Description of the target style
            model: Which model to use

        Returns:
            GeneratedImage with the styled result
        """
        prompt = f"Transform this image into the artistic style of {style_description}. " \
                 f"Preserve the original composition but render all elements in the new style."

        return await self.edit(prompt, content_image, model)

    def _load_image(self, image: Union[str, Path, bytes, "Image.Image"]) -> "Image.Image":
        """Load an image from various sources."""
        if not PIL_AVAILABLE:
            raise ImportError("PIL not available. Install with: pip install Pillow")

        if isinstance(image, (str, Path)):
            return Image.open(image)
        elif isinstance(image, bytes):
            from io import BytesIO
            return Image.open(BytesIO(image))
        elif hasattr(image, 'mode'):  # PIL Image
            return image
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")

    def _parse_response(self, response) -> GeneratedImage:
        """Parse the API response to extract image and text."""
        text_response = None
        image_data = None
        mime_type = "image/png"

        for part in response.parts:
            if part.text is not None:
                text_response = part.text
            elif part.inline_data is not None:
                # Get image as PIL Image then convert to bytes
                pil_image = part.as_image()
                from io import BytesIO
                buffer = BytesIO()
                pil_image.save(buffer, format='PNG')
                image_data = buffer.getvalue()

        if image_data is None:
            raise ValueError("No image in response")

        img_log("✅", "RESPONSE", f"Image generated", {
            "size": f"{len(image_data)} bytes",
            "has_text": text_response is not None
        })

        return GeneratedImage(
            data=image_data,
            mime_type=mime_type,
            text_response=text_response
        )


class ConversationalImageEditor:
    """
    Multi-turn image editing with conversation history.

    Allows iterative refinement of images through conversation.

    Usage:
        editor = ConversationalImageEditor()

        # Start with initial generation
        result = await editor.send("Create a mountain landscape")

        # Refine iteratively
        result = await editor.send("Add a lake in the foreground")
        result = await editor.send("Make it sunset colors")
        result = await editor.send("Add a cabin by the lake")

        result.save("final_landscape.png")
    """

    def __init__(
        self,
        model: ImageModel = ImageModel.PRO,
        api_key: Optional[str] = None
    ):
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package not installed")

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

        # Create chat session
        self.chat = self.client.chats.create(
            model=model.value,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        img_log("💬", "CHAT", f"Conversational editor initialized", {
            "model": model.value
        })

    async def send(
        self,
        message: str,
        aspect_ratio: Optional[AspectRatio] = None,
        size: Optional[ImageSize] = None
    ) -> GeneratedImage:
        """
        Send a message to refine the image.

        Args:
            message: The editing instruction or prompt
            aspect_ratio: Optional aspect ratio for this turn
            size: Optional size for this turn (Pro model)

        Returns:
            GeneratedImage with the current result
        """
        img_log("💬", "SEND", f"Sending message", {
            "message_preview": message[:60]
        })

        # Build config for this turn
        config = None
        if aspect_ratio or size:
            image_config = {}
            if aspect_ratio:
                image_config["aspect_ratio"] = aspect_ratio.value
            if size and self.model == ImageModel.PRO:
                image_config["image_size"] = size.value

            config = types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE'],
                image_config=types.ImageConfig(**image_config)
            )

        # Send message (sync, run in executor)
        loop = asyncio.get_event_loop()
        if config:
            response = await loop.run_in_executor(
                None,
                lambda: self.chat.send_message(message, config=config)
            )
        else:
            response = await loop.run_in_executor(
                None,
                lambda: self.chat.send_message(message)
            )

        return self._parse_response(response)

    def _parse_response(self, response) -> GeneratedImage:
        """Parse chat response to extract image."""
        text_response = None
        image_data = None

        for part in response.parts:
            if part.text is not None:
                text_response = part.text
            elif hasattr(part, 'as_image'):
                pil_image = part.as_image()
                from io import BytesIO
                buffer = BytesIO()
                pil_image.save(buffer, format='PNG')
                image_data = buffer.getvalue()

        if image_data is None:
            raise ValueError("No image in response")

        img_log("✅", "CHAT/RESPONSE", f"Image updated", {
            "size": f"{len(image_data)} bytes"
        })

        return GeneratedImage(
            data=image_data,
            mime_type="image/png",
            text_response=text_response
        )


# Quick access functions

async def generate_image(
    prompt: str,
    output_path: Optional[str] = None,
    model: str = "flash",
    aspect_ratio: str = "1:1"
) -> GeneratedImage:
    """
    Quick function to generate an image.

    Args:
        prompt: Text description
        output_path: Optional path to save the image
        model: "flash" or "pro"
        aspect_ratio: e.g., "1:1", "16:9", "9:16"

    Returns:
        GeneratedImage
    """
    service = ImageService()

    model_enum = ImageModel.PRO if model.lower() == "pro" else ImageModel.FLASH
    ratio_enum = AspectRatio(aspect_ratio)

    result = await service.generate(prompt, model_enum, ratio_enum)

    if output_path:
        result.save(output_path)

    return result


async def edit_image(
    prompt: str,
    input_image: str,
    output_path: Optional[str] = None
) -> GeneratedImage:
    """
    Quick function to edit an image.

    Args:
        prompt: Editing instructions
        input_image: Path to input image
        output_path: Optional path to save result

    Returns:
        GeneratedImage
    """
    service = ImageService()
    result = await service.edit(prompt, input_image)

    if output_path:
        result.save(output_path)

    return result
