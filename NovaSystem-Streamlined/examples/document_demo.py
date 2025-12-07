#!/usr/bin/env python3
"""
Document Processing Demo for NovaSystem.

Demonstrates Gemini's PDF understanding capabilities:
1. Document summarization
2. Question answering about documents
3. Structured data extraction
4. Multi-document comparison
5. Format conversion (Markdown, HTML)
6. Table and chart analysis

Requires: pip install google-genai httpx

Usage:
    python document_demo.py --pdf path/to/document.pdf
    python document_demo.py --url https://example.com/paper.pdf
    python document_demo.py --demo summarize --pdf report.pdf
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.document_service import (
    DocumentService,
    OutputFormat,
    summarize_pdf,
    ask_pdf,
    extract_from_pdf,
    pdf_to_markdown
)


# Sample PDF URLs for testing
SAMPLE_PDFS = {
    "gemini": "https://arxiv.org/pdf/2312.11805",  # Gemini paper
    "attention": "https://arxiv.org/pdf/1706.03762",  # Attention Is All You Need
    "nasa": "https://www.nasa.gov/wp-content/uploads/static/history/alsj/a17/A17_FlightPlan.pdf"
}


async def demo_summarize(pdf_source: str):
    """Demo: Summarize a document."""
    print("\n" + "="*60)
    print("📄 Demo: Document Summarization")
    print("="*60)

    service = DocumentService()

    print(f"\n📥 Loading: {pdf_source[:60]}...")

    # Try different summary lengths
    for length in ["brief", "medium"]:
        print(f"\n📝 {length.capitalize()} summary:")
        result = await service.summarize(pdf_source, length=length)
        summary = result.text[:500] + "..." if len(result.text) > 500 else result.text
        print(f"   {summary}")


async def demo_qa(pdf_source: str, questions: list = None):
    """Demo: Question answering about documents."""
    print("\n" + "="*60)
    print("❓ Demo: Document Q&A")
    print("="*60)

    service = DocumentService()

    default_questions = [
        "What is the main topic of this document?",
        "What are the key findings or conclusions?",
        "Who are the authors or contributors?",
    ]

    questions = questions or default_questions

    print(f"\n📥 Loading document...")

    for q in questions:
        print(f"\n❓ {q}")
        result = await service.ask(q, pdf_source)
        answer = result.text[:400] + "..." if len(result.text) > 400 else result.text
        print(f"💬 {answer}")


async def demo_extract(pdf_source: str):
    """Demo: Structured data extraction."""
    print("\n" + "="*60)
    print("🔍 Demo: Data Extraction")
    print("="*60)

    service = DocumentService()

    # Define schema for academic paper
    schema = {
        "title": "string",
        "authors": ["string"],
        "abstract": "string",
        "keywords": ["string"],
        "sections": ["string"],
        "references_count": "number"
    }

    print(f"\n📥 Loading document...")
    print(f"📋 Schema: {list(schema.keys())}")

    result = await service.extract(
        pdf_source,
        schema=schema,
        instructions="Extract metadata from this academic paper."
    )

    if result.extracted_data and result.extracted_data.data:
        print("\n✅ Extracted data:")
        for key, value in result.extracted_data.data.items():
            if isinstance(value, list):
                print(f"   {key}: {len(value)} items")
                for item in value[:3]:
                    print(f"      - {str(item)[:60]}")
            else:
                val_str = str(value)[:100]
                print(f"   {key}: {val_str}")
    else:
        print("\n⚠️ Extraction returned no structured data")
        print(f"Raw response: {result.text[:300]}...")


async def demo_compare(pdf_sources: list):
    """Demo: Compare multiple documents."""
    print("\n" + "="*60)
    print("🔄 Demo: Document Comparison")
    print("="*60)

    if len(pdf_sources) < 2:
        print("⚠️ Need at least 2 documents for comparison")
        # Use sample papers
        pdf_sources = [SAMPLE_PDFS["gemini"], SAMPLE_PDFS["attention"]]
        print(f"Using sample papers for demo...")

    service = DocumentService()

    print(f"\n📥 Loading {len(pdf_sources)} documents...")

    result = await service.compare(
        pdf_sources,
        question="Compare the main contributions and methodologies of these papers. Create a comparison table."
    )

    print(f"\n📊 Comparison:\n{result.text}")


async def demo_transcribe(pdf_source: str, format: str = "markdown"):
    """Demo: Convert document to different formats."""
    print("\n" + "="*60)
    print(f"📝 Demo: Transcribe to {format.upper()}")
    print("="*60)

    service = DocumentService()

    format_enum = OutputFormat(format.lower())

    print(f"\n📥 Loading document...")

    result = await service.transcribe(pdf_source, format=format_enum)

    # Show preview
    preview = result.text[:1000] + "\n..." if len(result.text) > 1000 else result.text
    print(f"\n📄 Transcription preview:\n{preview}")

    # Save to file
    ext = {"markdown": "md", "html": "html", "text": "txt", "json": "json"}
    output_file = f"transcribed_document.{ext.get(format, 'txt')}"
    Path(output_file).write_text(result.text)
    print(f"\n💾 Saved to: {output_file}")


async def demo_tables(pdf_source: str):
    """Demo: Extract tables from document."""
    print("\n" + "="*60)
    print("📊 Demo: Table Extraction")
    print("="*60)

    service = DocumentService()

    print(f"\n📥 Loading document...")

    result = await service.analyze_tables(pdf_source, output_format="markdown")

    print(f"\n📋 Extracted tables:\n{result.text[:2000]}...")


async def demo_charts(pdf_source: str):
    """Demo: Analyze charts and graphs."""
    print("\n" + "="*60)
    print("📈 Demo: Chart Analysis")
    print("="*60)

    service = DocumentService()

    print(f"\n📥 Loading document...")

    result = await service.analyze_charts(pdf_source)

    print(f"\n📊 Chart analysis:\n{result.text}")


async def run_all_demos(pdf_source: str):
    """Run all demos on a single document."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Document Processing Demo")
    print("    Using Gemini Native PDF Understanding")
    print("="*60)

    demos = [
        ("Summarize", lambda: demo_summarize(pdf_source)),
        ("Q&A", lambda: demo_qa(pdf_source)),
        ("Extract", lambda: demo_extract(pdf_source)),
        ("Transcribe", lambda: demo_transcribe(pdf_source, "markdown")),
    ]

    for name, demo_func in demos:
        try:
            await demo_func()
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Document Processing Demo")
    parser.add_argument(
        "--pdf",
        type=str,
        help="Path to local PDF file"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL of PDF to process"
    )
    parser.add_argument(
        "--sample",
        choices=["gemini", "attention", "nasa"],
        help="Use a sample PDF"
    )
    parser.add_argument(
        "--demo",
        choices=["all", "summarize", "qa", "extract", "compare", "transcribe", "tables", "charts"],
        default="all",
        help="Which demo to run"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "text", "json"],
        default="markdown",
        help="Output format for transcription"
    )
    parser.add_argument(
        "--question",
        type=str,
        help="Specific question to ask"
    )

    args = parser.parse_args()

    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("   Get your key at: https://aistudio.google.com/apikey")
        return

    # Determine PDF source
    pdf_source = None
    if args.pdf:
        pdf_source = args.pdf
    elif args.url:
        pdf_source = args.url
    elif args.sample:
        pdf_source = SAMPLE_PDFS[args.sample]
        print(f"📚 Using sample: {args.sample}")
    else:
        # Default to Gemini paper
        pdf_source = SAMPLE_PDFS["gemini"]
        print("📚 No PDF specified, using Gemini paper as sample")

    print(f"📄 Source: {pdf_source[:70]}...")

    # Run demos
    if args.demo == "all":
        await run_all_demos(pdf_source)
    elif args.demo == "summarize":
        await demo_summarize(pdf_source)
    elif args.demo == "qa":
        questions = [args.question] if args.question else None
        await demo_qa(pdf_source, questions)
    elif args.demo == "extract":
        await demo_extract(pdf_source)
    elif args.demo == "compare":
        # Use multiple sample PDFs for comparison
        await demo_compare([SAMPLE_PDFS["gemini"], SAMPLE_PDFS["attention"]])
    elif args.demo == "transcribe":
        await demo_transcribe(pdf_source, args.format)
    elif args.demo == "tables":
        await demo_tables(pdf_source)
    elif args.demo == "charts":
        await demo_charts(pdf_source)


if __name__ == "__main__":
    asyncio.run(main())
