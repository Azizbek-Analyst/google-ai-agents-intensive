from fastmcp import FastMCP
from openai import OpenAI
import base64
import os
import io
from typing import List, Dict
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
# 1. Инициализация MCP-сервера
mcp = FastMCP("genai-image-server")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

# OPENAI_API_KEY = ""

# Init MCP server
# client = OpenAI(api_key=OPENAI_API_KEY)

mcp = FastMCP("image-generator")
# Assumes the FastAPI app from above is already defined

# Load model

@mcp.tool()
async def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    model: str = 'imagen-4.0-generate-001',
    max_images: int = 1,
) -> Dict[str, List[str]]:
    """
    Сгенерировать изображение с помощью Google GenAI (Gemini).

    Аргументы:
    - prompt: текстовый запрос (описание сцены / стиля).
    - aspect_ratio: аспект (например '1:1', '9:16', '16:9' и т.д.).
    - model: модель, по умолчанию 'imagen-4.0-generate-001'.
    - max_images: сколько картинок вернуть (1–4).

    Возвращает:
    {
        "images": [<base64_png_1>, <base64_png_2>, ...]
    }
    """

    

    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images= max_images,
        )
    )
    iter = 0
    if max_images > 1:
        for generated_image in response.generated_images:
            iter += 1
            generate_image.image.save(f"generated_image_{iter}.png")
            print("Image saved in folder with the name generated_image + number")
    else:
        return response.generated_images[0].image.save("generated_image.png"), print("Image saved in folder with name generated_image")

if __name__ == "__main__":
    mcp.run()

# run in terminal: fastmcp run mcp_image.py:mcp --transport http --port 8000
