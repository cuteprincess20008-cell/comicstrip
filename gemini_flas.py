import json

from google import genai
from google.genai import types

from .config import (
    GEMINI_API_KEY,
    GEMINI_FLASH_MODEL
)


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ---------------------------------------------------------
# JSON EXTRACTION
# ---------------------------------------------------------

def extract_json_array(text: str):

    text = text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```"):

        parts = text.split(
            "\n",
            1
        )

        if len(parts) == 2:
            text = parts[1]

        if text.endswith("```"):
            text = text[:-3]

    start = text.find("[")

    end = text.rfind("]")

    if start == -1 or end == -1:

        raise ValueError(
            "Gemini did not return a valid JSON array."
        )

    json_text = text[
        start:end + 1
    ]

    return json.loads(
        json_text
    )


# ---------------------------------------------------------
# GENERATE 5-PANEL OUTLINE
# ---------------------------------------------------------

def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add your Gemini API key to the .env file."
        )


    prompt = f"""

You are an expert comic story planner.

Create a complete 5-panel comic story outline.

USER INPUT
----------

Story Prompt:
{story_prompt}

Character Name:
{character_name}

Setting:
{setting}

Story Tone:
{tone}

Art Style:
{art_style}


REQUIREMENTS
------------

Create exactly 5 connected panels.

The story must have:

Panel 1:
Introduction

Panel 2:
Development

Panel 3:
Problem or conflict

Panel 4:
Climax or important event

Panel 5:
Resolution


Return ONLY a JSON array.

Each object must contain:

panel_number
title
scene_description
image_prompt

Example format:

[
  {{
    "panel_number": 1,
    "title": "Beginning",
    "scene_description": "Description of the scene",
    "image_prompt": "Detailed visual prompt"
  }}
]

Do not include markdown.
Do not include explanations outside the JSON.
Make the character visually consistent across all panels.
"""


    response = client.models.generate_content(

        model=GEMINI_FLASH_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.8,

            response_mime_type="application/json"

        )
    )


    panels = extract_json_array(
        response.text
    )


    if len(panels) != 5:

        raise ValueError(
            "Gemini did not generate exactly 5 panels."
        )


    for index, panel in enumerate(
        panels,
        start=1
    ):

        panel["panel_number"] = index


        required_fields = [
            "title",
            "scene_description",
            "image_prompt"
        ]


        for field in required_fields:

            if not panel.get(field):

                raise ValueError(
                    f"Panel {index} is missing {field}."
                )


    return panels