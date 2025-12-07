#!/usr/bin/env python3
"""
Market Research Agent Example.

Demonstrates NovaSystem's capabilities:
1. Gemini integration via OpenAI-compatible API
2. Structured prompt building
3. JSON schema extraction
4. Report generation

Based on the Vercel AI SDK market research example, implemented in Python.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.llm_service import LLMService
from novasystem.utils.prompt_builder import (
    PromptBuilder, 
    Verbosity, 
    Tone, 
    Example,
    format_json_output_prompt
)


@dataclass
class ChartConfig:
    """Configuration for a chart."""
    type: str  # "bar" or "line"
    labels: List[str]
    data: List[float]
    label: str
    colors: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "labels": self.labels,
            "data": self.data,
            "label": self.label,
            "colors": self.colors
        }


class MarketResearchAgent:
    """
    Agent that performs market research and generates reports.
    
    Uses Gemini for:
    - Research synthesis
    - Structured data extraction
    - Report generation
    """

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.llm_service = LLMService()
        self.model = model
        
        # Verify Gemini is available
        if not self.llm_service.gemini_client:
            raise ValueError(
                "Gemini API not configured. Set GEMINI_API_KEY environment variable."
            )
        
        print(f"✅ MarketResearchAgent initialized with {model}")

    async def research_market(self, topic: str, region: str = "North America") -> str:
        """
        Step 1: Research market trends.
        
        In a production environment, this would use Google Search grounding.
        For this example, we use Gemini's knowledge.
        """
        print(f"\n🔍 Researching: {topic} in {region}...")
        
        builder = PromptBuilder()
        builder.set_role(
            "You are an expert market research analyst with access to current market data. "
            "Provide detailed, data-driven analysis with specific statistics and figures."
        )
        builder.set_verbosity(Verbosity.HIGH)
        builder.set_tone(Tone.FORMAL)
        builder.add_constraint("Include specific market size figures in USD")
        builder.add_constraint("Name key players with approximate market shares")
        builder.add_constraint("Identify 3-5 primary consumer drivers")
        builder.add_constraint("Include growth projections if available")
        
        messages = builder.build_messages(
            task=f"""Provide a comprehensive market analysis for {topic} in {region} for 2024-2025.
            
Include:
1. Total market size (current and projected)
2. Key players and their approximate market shares (as percentages)
3. Primary consumer drivers
4. Growth trends and projections
5. Any notable challenges or opportunities""",
            context=f"Focus on: {topic}\nRegion: {region}\nTime period: 2024-2025"
        )
        
        response = await self.llm_service.get_completion(
            messages=messages,
            model=self.model,
            temperature=0.3  # Lower temperature for factual research
        )
        
        print(f"✅ Research complete ({len(response)} chars)")
        return response

    async def extract_chart_data(self, research_text: str) -> List[ChartConfig]:
        """
        Step 2: Extract structured chart data from research.
        
        Uses JSON schema extraction to get chart-ready data.
        """
        print("\n📊 Extracting chart data...")
        
        # Define the expected schema
        schema = {
            "charts": [
                {
                    "type": "bar|line",
                    "label": "Chart title",
                    "labels": ["Label1", "Label2"],
                    "data": [10, 20],
                    "colors": ["rgba(54, 162, 235, 0.8)"]
                }
            ]
        }
        
        builder = PromptBuilder()
        builder.set_role(
            "You are a data visualization expert. Extract meaningful chart data from market research."
        )
        builder.set_verbosity(Verbosity.LOW)
        builder.add_constraint("Output ONLY valid JSON, no additional text")
        builder.add_constraint("Create 2-3 meaningful charts")
        builder.add_constraint("Use realistic data from the research")
        builder.add_constraint("Colors should be in rgba format")
        
        # Add example for few-shot learning
        builder.add_example(Example(
            input="Market share: Company A 40%, Company B 30%, Others 30%",
            output=json.dumps({
                "charts": [{
                    "type": "bar",
                    "label": "Market Share by Company",
                    "labels": ["Company A", "Company B", "Others"],
                    "data": [40, 30, 30],
                    "colors": ["rgba(54, 162, 235, 0.8)", "rgba(255, 99, 132, 0.8)", "rgba(75, 192, 192, 0.8)"]
                }]
            }, indent=2)
        ))
        
        builder.set_output_format(f"```json\n{json.dumps(schema, indent=2)}\n```")
        
        messages = builder.build_messages(
            task=f"""Extract 2-3 meaningful charts from this market research.
            
Return ONLY a JSON object with a "charts" array. Each chart should have:
- type: "bar" or "line"
- label: descriptive title
- labels: array of category names
- data: array of numeric values
- colors: array of rgba color strings

Research Text:
{research_text}""",
            context="Extract numerical data that would be meaningful in a chart."
        )
        
        response = await self.llm_service.get_completion(
            messages=messages,
            model=self.model,
            temperature=0.1  # Very low for structured output
        )
        
        # Parse JSON from response (handle markdown code blocks)
        try:
            json_str = response
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            
            data = json.loads(json_str.strip())
            charts = [
                ChartConfig(
                    type=c.get("type", "bar"),
                    labels=c.get("labels", []),
                    data=c.get("data", []),
                    label=c.get("label", ""),
                    colors=c.get("colors", ["rgba(54, 162, 235, 0.8)"])
                )
                for c in data.get("charts", [])
            ]
            print(f"✅ Extracted {len(charts)} chart configurations")
            return charts
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing error: {e}")
            print(f"   Response was: {response[:200]}...")
            return []

    async def generate_html_report(
        self, 
        research_text: str, 
        charts: List[ChartConfig],
        title: str = "Market Analysis Report"
    ) -> str:
        """
        Step 3: Generate a professional HTML report.
        """
        print("\n📝 Generating HTML report...")
        
        chart_configs = [c.to_dict() for c in charts]
        
        builder = PromptBuilder()
        builder.set_role(
            "You are an expert financial analyst and report writer. "
            "Create professional, well-formatted reports."
        )
        builder.set_verbosity(Verbosity.HIGH)
        builder.set_tone(Tone.FORMAL)
        builder.add_constraint("Output ONLY valid HTML, no markdown")
        builder.add_constraint("Use modern, clean styling with CSS")
        builder.add_constraint("Include Chart.js for visualizations")
        
        messages = builder.build_messages(
            task=f"""Generate a comprehensive market analysis report in HTML format.

**Instructions:**
1. Write a complete HTML document with embedded CSS
2. Use the provided research text as the main content
3. Structure with clear headings, paragraphs, and bullet points
4. Include Chart.js charts using the provided configurations
5. Add a professional header with the title and date
6. Use a clean, modern design with a blue color scheme

**Title:** {title}
**Date:** {datetime.now().strftime("%B %d, %Y")}

**Chart Rendering:**
Include this in the head: <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

For each chart, create:
<div style="max-width: 600px; margin: 20px auto;">
    <canvas id="chart1"></canvas>
</div>
<script>
    new Chart(document.getElementById('chart1'), CONFIG_HERE);
</script>

**Research Text:**
{research_text}

**Chart Configurations:**
{json.dumps(chart_configs, indent=2)}

Return ONLY the HTML code.""",
            context="Create a professional market research report."
        )
        
        response = await self.llm_service.get_completion(
            messages=messages,
            model=self.model,
            temperature=0.5
        )
        
        # Clean up response (remove markdown code blocks if present)
        html = response
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        elif "```" in html:
            html = html.split("```")[1].split("```")[0]
        
        print(f"✅ Generated HTML report ({len(html)} chars)")
        return html.strip()

    async def run_analysis(
        self, 
        topic: str, 
        region: str = "North America",
        output_file: str = "market_report.html"
    ) -> str:
        """
        Run the complete market research analysis pipeline.
        
        Returns the path to the generated report.
        """
        print(f"\n{'='*60}")
        print(f"🚀 Market Research Agent")
        print(f"   Topic: {topic}")
        print(f"   Region: {region}")
        print(f"{'='*60}")
        
        start_time = datetime.now()
        
        # Step 1: Research
        research = await self.research_market(topic, region)
        
        # Step 2: Extract chart data
        charts = await self.extract_chart_data(research)
        
        # Step 3: Generate report
        html = await self.generate_html_report(
            research, 
            charts,
            title=f"{topic} - Market Analysis"
        )
        
        # Save report
        output_path = Path(output_file)
        output_path.write_text(html)
        
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\n{'='*60}")
        print(f"✅ Analysis complete!")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Report saved to: {output_path.absolute()}")
        print(f"{'='*60}\n")
        
        return str(output_path.absolute())


async def main():
    """Run the market research agent example."""
    
    # Example: Plant-based milk market analysis
    agent = MarketResearchAgent(model="gemini-2.5-flash")
    
    report_path = await agent.run_analysis(
        topic="Plant-based milk",
        region="North America",
        output_file="plant_milk_market_report.html"
    )
    
    print(f"\n📄 Open the report: file://{report_path}")
    print("\nTo convert to PDF, you can use a browser or tools like wkhtmltopdf.")


if __name__ == "__main__":
    asyncio.run(main())
