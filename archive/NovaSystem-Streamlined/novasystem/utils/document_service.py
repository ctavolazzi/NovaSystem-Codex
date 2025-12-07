"""
Document Processing Service for NovaSystem.

Uses Gemini's native PDF understanding capabilities:
- Process documents up to 1000 pages
- Analyze text, images, diagrams, charts, tables
- Extract structured data
- Summarize and answer questions
- Transcribe to HTML/Markdown

Requires: pip install google-genai httpx
"""

import os
import sys
import io
import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union, Dict, Any, Type
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

# Attempt to import httpx for URL fetching
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    httpx = None

logger = logging.getLogger(__name__)


def doc_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a document service event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [DOC/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


class OutputFormat(Enum):
    """Output format options for document processing."""
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


@dataclass
class DocumentFile:
    """Represents an uploaded document file."""
    name: str
    uri: str
    mime_type: str
    size_bytes: Optional[int] = None
    display_name: Optional[str] = None

    def to_part(self) -> Any:
        """Convert to a Gemini Part for API calls."""
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai not available")
        return genai.types.Part.from_uri(self.uri, self.mime_type)


@dataclass
class ExtractedData:
    """Structured data extracted from a document."""
    data: Dict[str, Any]
    raw_response: str

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.data, indent=indent)


@dataclass
class DocumentResult:
    """Result from document processing."""
    text: str
    source_files: List[DocumentFile] = field(default_factory=list)
    extracted_data: Optional[ExtractedData] = None
    tokens_used: Optional[int] = None


class DocumentService:
    """
    Service for processing documents with Gemini.

    Features:
    - PDF processing (up to 1000 pages, 50MB)
    - Multi-document comparison
    - Structured data extraction
    - Summarization and Q&A
    - Format conversion (HTML, Markdown)

    Usage:
        service = DocumentService()

        # Summarize a PDF
        result = await service.summarize("report.pdf")

        # Ask questions about a document
        result = await service.ask("What are the main findings?", "paper.pdf")

        # Extract structured data
        result = await service.extract(
            "invoices.pdf",
            schema={"invoice_number": str, "total": float, "items": list}
        )

        # Compare multiple documents
        result = await service.compare(["v1.pdf", "v2.pdf"])

        # Convert to HTML
        result = await service.transcribe("document.pdf", format=OutputFormat.HTML)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash"
    ):
        """
        Initialize the document service.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model to use
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
        self._uploaded_files: Dict[str, DocumentFile] = {}

        doc_log("✅", "INIT", f"DocumentService initialized with {model}")

    async def _load_document(
        self,
        source: Union[str, Path, bytes],
        use_file_api: bool = True
    ) -> Union[DocumentFile, Any]:
        """
        Load a document from various sources.

        Args:
            source: Path, URL, or bytes
            use_file_api: Whether to use Files API (recommended for large docs)

        Returns:
            DocumentFile if using Files API, else Part for inline
        """
        if isinstance(source, bytes):
            # Inline bytes
            if use_file_api:
                doc_io = io.BytesIO(source)
                loop = asyncio.get_event_loop()
                uploaded = await loop.run_in_executor(
                    None,
                    lambda: self.client.files.upload(
                        file=doc_io,
                        config={"mime_type": "application/pdf"}
                    )
                )
                doc_file = DocumentFile(
                    name=uploaded.name,
                    uri=uploaded.uri,
                    mime_type="application/pdf",
                    display_name="uploaded_bytes"
                )
                self._uploaded_files[uploaded.name] = doc_file
                return doc_file
            else:
                return types.Part.from_bytes(data=source, mime_type="application/pdf")

        source_str = str(source)

        # URL
        if source_str.startswith(("http://", "https://")):
            if not HTTPX_AVAILABLE:
                raise ImportError("httpx not available. Install with: pip install httpx")

            doc_log("📥", "DOWNLOAD", f"Fetching document from URL")
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: httpx.get(source_str)
            )
            doc_bytes = response.content

            if use_file_api:
                doc_io = io.BytesIO(doc_bytes)
                uploaded = await loop.run_in_executor(
                    None,
                    lambda: self.client.files.upload(
                        file=doc_io,
                        config={"mime_type": "application/pdf"}
                    )
                )
                doc_file = DocumentFile(
                    name=uploaded.name,
                    uri=uploaded.uri,
                    mime_type="application/pdf",
                    size_bytes=len(doc_bytes),
                    display_name=Path(source_str).name
                )
                self._uploaded_files[uploaded.name] = doc_file
                doc_log("✅", "UPLOAD", f"Uploaded: {doc_file.display_name}")
                return doc_file
            else:
                return types.Part.from_bytes(data=doc_bytes, mime_type="application/pdf")

        # Local file
        path = Path(source_str)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        if use_file_api:
            loop = asyncio.get_event_loop()
            uploaded = await loop.run_in_executor(
                None,
                lambda: self.client.files.upload(file=path)
            )
            doc_file = DocumentFile(
                name=uploaded.name,
                uri=uploaded.uri,
                mime_type="application/pdf",
                size_bytes=path.stat().st_size,
                display_name=path.name
            )
            self._uploaded_files[uploaded.name] = doc_file
            doc_log("✅", "UPLOAD", f"Uploaded: {doc_file.display_name}")
            return doc_file
        else:
            return types.Part.from_bytes(
                data=path.read_bytes(),
                mime_type="application/pdf"
            )

    async def summarize(
        self,
        document: Union[str, Path, bytes],
        length: str = "medium",
        focus: Optional[str] = None
    ) -> DocumentResult:
        """
        Summarize a document.

        Args:
            document: Path, URL, or bytes of the PDF
            length: Summary length (brief, medium, detailed)
            focus: Optional focus area for the summary

        Returns:
            DocumentResult with the summary
        """
        doc_log("📄", "SUMMARIZE", f"Summarizing document ({length})")

        doc = await self._load_document(document)

        length_prompts = {
            "brief": "Provide a brief 2-3 sentence summary of this document.",
            "medium": "Provide a comprehensive summary of this document in about 3-5 paragraphs.",
            "detailed": "Provide a detailed summary of this document, covering all major sections and key points."
        }

        prompt = length_prompts.get(length, length_prompts["medium"])
        if focus:
            prompt += f" Focus particularly on: {focus}"

        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        doc_log("✅", "SUMMARIZE", f"Summary generated ({len(response.text)} chars)")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else []
        )

    async def ask(
        self,
        question: str,
        document: Union[str, Path, bytes]
    ) -> DocumentResult:
        """
        Ask a question about a document.

        Args:
            question: The question to ask
            document: Path, URL, or bytes of the PDF

        Returns:
            DocumentResult with the answer
        """
        doc_log("❓", "ASK", f"Question: {question[:50]}...")

        doc = await self._load_document(document)
        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), question]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        doc_log("✅", "ASK", f"Answer received ({len(response.text)} chars)")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else []
        )

    async def extract(
        self,
        document: Union[str, Path, bytes],
        schema: Dict[str, Any],
        instructions: Optional[str] = None
    ) -> DocumentResult:
        """
        Extract structured data from a document.

        Args:
            document: Path, URL, or bytes of the PDF
            schema: Expected data structure (for guidance)
            instructions: Optional additional extraction instructions

        Returns:
            DocumentResult with extracted data
        """
        doc_log("🔍", "EXTRACT", f"Extracting data with schema")

        doc = await self._load_document(document)

        prompt = f"""Extract the following information from this document and return it as JSON.

Expected schema:
```json
{json.dumps(schema, indent=2)}
```

{instructions or "Extract all matching data from the document."}

Return ONLY valid JSON, no explanations."""

        config = types.GenerateContentConfig(
            response_mime_type="application/json"
        )

        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )
        )

        # Parse JSON
        try:
            data = json.loads(response.text)
            extracted = ExtractedData(data=data, raw_response=response.text)
            doc_log("✅", "EXTRACT", f"Extracted {len(data)} fields")
        except json.JSONDecodeError:
            # Try to clean up response
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            try:
                data = json.loads(text.strip())
                extracted = ExtractedData(data=data, raw_response=response.text)
            except:
                extracted = ExtractedData(data={}, raw_response=response.text)
                doc_log("⚠️", "EXTRACT", "Could not parse JSON response")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else [],
            extracted_data=extracted
        )

    async def compare(
        self,
        documents: List[Union[str, Path, bytes]],
        question: Optional[str] = None
    ) -> DocumentResult:
        """
        Compare multiple documents.

        Args:
            documents: List of document sources
            question: Optional specific comparison question

        Returns:
            DocumentResult with comparison analysis
        """
        if len(documents) < 2:
            raise ValueError("Need at least 2 documents to compare")

        doc_log("🔄", "COMPARE", f"Comparing {len(documents)} documents")

        docs = []
        for d in documents:
            doc = await self._load_document(d)
            docs.append(doc)

        prompt = question or "Compare these documents. What are the key differences and similarities?"

        contents = [d if isinstance(d, types.Part) else d.to_part() for d in docs]
        contents.append(prompt)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        doc_log("✅", "COMPARE", f"Comparison complete")

        return DocumentResult(
            text=response.text,
            source_files=[d for d in docs if isinstance(d, DocumentFile)]
        )

    async def transcribe(
        self,
        document: Union[str, Path, bytes],
        format: OutputFormat = OutputFormat.MARKDOWN,
        preserve_layout: bool = True
    ) -> DocumentResult:
        """
        Transcribe document content to a different format.

        Args:
            document: Path, URL, or bytes of the PDF
            format: Output format (markdown, html, text)
            preserve_layout: Whether to try to preserve document layout

        Returns:
            DocumentResult with transcribed content
        """
        doc_log("📝", "TRANSCRIBE", f"Transcribing to {format.value}")

        doc = await self._load_document(document)

        format_prompts = {
            OutputFormat.TEXT: "Transcribe this document as plain text.",
            OutputFormat.MARKDOWN: "Transcribe this document to Markdown format, preserving headings, lists, and formatting.",
            OutputFormat.HTML: "Transcribe this document to clean, semantic HTML. Include proper heading tags, paragraphs, lists, and tables.",
            OutputFormat.JSON: "Extract all content from this document as structured JSON with sections, headings, and content."
        }

        prompt = format_prompts[format]
        if preserve_layout:
            prompt += " Preserve the original document layout and structure as much as possible."

        config = None
        if format == OutputFormat.JSON:
            config = types.GenerateContentConfig(
                response_mime_type="application/json"
            )

        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )
        )

        doc_log("✅", "TRANSCRIBE", f"Transcription complete ({len(response.text)} chars)")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else []
        )

    async def analyze_tables(
        self,
        document: Union[str, Path, bytes],
        output_format: str = "markdown"
    ) -> DocumentResult:
        """
        Extract and analyze tables from a document.

        Args:
            document: Path, URL, or bytes of the PDF
            output_format: Table output format (markdown, csv, json)

        Returns:
            DocumentResult with extracted tables
        """
        doc_log("📊", "TABLES", f"Extracting tables ({output_format})")

        doc = await self._load_document(document)

        format_instructions = {
            "markdown": "Format each table in Markdown table syntax.",
            "csv": "Format each table as CSV data.",
            "json": "Format each table as a JSON array of objects."
        }

        prompt = f"""Identify and extract ALL tables from this document.
For each table:
1. Provide a title or description
2. Extract the complete table data

{format_instructions.get(output_format, format_instructions['markdown'])}

If there are no tables, indicate that clearly."""

        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        doc_log("✅", "TABLES", f"Table extraction complete")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else []
        )

    async def analyze_charts(
        self,
        document: Union[str, Path, bytes]
    ) -> DocumentResult:
        """
        Analyze charts and graphs in a document.

        Args:
            document: Path, URL, or bytes of the PDF

        Returns:
            DocumentResult with chart analysis
        """
        doc_log("📈", "CHARTS", "Analyzing charts and graphs")

        doc = await self._load_document(document)

        prompt = """Analyze all charts, graphs, and diagrams in this document.
For each visual:
1. Describe what type of chart/graph it is
2. Explain what data it represents
3. Summarize the key insights or trends shown
4. Note any labels, legends, or annotations

If there are no charts or graphs, indicate that clearly."""

        contents = [doc if isinstance(doc, types.Part) else doc.to_part(), prompt]

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
        )

        doc_log("✅", "CHARTS", "Chart analysis complete")

        return DocumentResult(
            text=response.text,
            source_files=[doc] if isinstance(doc, DocumentFile) else []
        )

    def list_uploaded_files(self) -> List[DocumentFile]:
        """List all files uploaded in this session."""
        return list(self._uploaded_files.values())


# Quick access functions

async def summarize_pdf(
    pdf_path: str,
    length: str = "medium"
) -> str:
    """Quick function to summarize a PDF."""
    service = DocumentService()
    result = await service.summarize(pdf_path, length=length)
    return result.text


async def ask_pdf(
    question: str,
    pdf_path: str
) -> str:
    """Quick function to ask a question about a PDF."""
    service = DocumentService()
    result = await service.ask(question, pdf_path)
    return result.text


async def extract_from_pdf(
    pdf_path: str,
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    """Quick function to extract structured data from a PDF."""
    service = DocumentService()
    result = await service.extract(pdf_path, schema)
    return result.extracted_data.data if result.extracted_data else {}


async def pdf_to_markdown(pdf_path: str) -> str:
    """Quick function to convert PDF to Markdown."""
    service = DocumentService()
    result = await service.transcribe(pdf_path, OutputFormat.MARKDOWN)
    return result.text


async def pdf_to_html(pdf_path: str) -> str:
    """Quick function to convert PDF to HTML."""
    service = DocumentService()
    result = await service.transcribe(pdf_path, OutputFormat.HTML)
    return result.text
