# Gemini API Code Generation Instructions

> **For AI assistants and code generation tools**

When generating code for the Gemini API in this project, use the **Google GenAI SDK** (`google-genai`), NOT the legacy `google-generativeai` library.

## Python SDK

### Installation
```bash
pip install google-genai
```

### Correct Imports
```python
# ✅ CORRECT - Google GenAI SDK (GA, recommended)
from google import genai
from google.genai import types

# Initialize client
client = genai.Client(api_key="YOUR_API_KEY")
```

### ❌ DO NOT USE (Legacy - deprecated Nov 30, 2025)
```python
# ❌ WRONG - Legacy library
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
```

## API Usage Examples

### Text Generation
```python
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain quantum computing"
)
print(response.text)
```

### Chat/Multi-turn
```python
chat = client.chats.create(model="gemini-2.5-flash")
response = chat.send_message("Hello!")
response = chat.send_message("Tell me more")
```

### Streaming
```python
for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write a story"
):
    print(chunk.text, end="")
```

### Image Generation (Native)
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A sunset over mountains"
)

for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data'):
        # Save image
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

### Vision (Image Understanding)
```python
from PIL import Image

image = Image.open("photo.jpg")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "What's in this image?",
        image
    ]
)
```

### Document Processing (PDF)
```python
# Upload file
file = client.files.upload(file="document.pdf")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Summarize this document",
        file
    ]
)
```

### Function Calling
```python
from google.genai import types

tools = [types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_weather",
            description="Get weather for a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        )
    ]
)]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Paris?",
    config=types.GenerateContentConfig(tools=tools)
)
```

### Thinking/Reasoning
```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Solve: What is 15% of 847?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=1024
        )
    )
)

# Access thoughts
for part in response.candidates[0].content.parts:
    if hasattr(part, 'thought') and part.thought:
        print(f"Thought: {part.text}")
    else:
        print(f"Answer: {part.text}")
```

## Available Models

| Model | Use Case |
|-------|----------|
| `gemini-2.5-flash` | Fast, general purpose |
| `gemini-2.5-pro` | Complex reasoning |
| `gemini-2.5-flash-lite` | Cost-effective |
| `gemini-3-pro-preview` | Advanced thinking |
| `gemini-2.5-flash-image` | Image generation |
| `gemini-3-pro-image-preview` | Advanced images (4K) |

## NovaSystem Services

This project provides wrapper services for Gemini:

| Service | File | Purpose |
|---------|------|---------|
| LLMService | `llm_service.py` | Text (OpenAI-compatible) |
| ImageService | `image_service.py` | Image generation |
| VisionService | `vision_service.py` | Image understanding |
| DocumentService | `document_service.py` | PDF processing |
| ThinkingService | `thinking_service.py` | Reasoning |
| ToolsService | `tools_service.py` | Function calling |
| RateLimiter | `rate_limiter.py` | Quota management |

## References

- [Google GenAI SDK (Python)](https://github.com/googleapis/python-genai)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Migration Guide](https://ai.google.dev/gemini-api/docs/migrate)
