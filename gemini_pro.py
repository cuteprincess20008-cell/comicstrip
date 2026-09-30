import json

from google import genai
from google.genai import types

from .config import (
    GEMINI_API_KEY,
    GEMINI_PRO_MODEL
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
# GENERATE STORY TEXT
# ---------------------------------------------------------

def generate_story(
    outline,
    character_name,
    setting,
    tone,
    art_style
):

    if client is None:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    prompt = f"""

You are an expert comic writer.

Expand the following 5-panel comic outline into
complete comic narration and dialogue.

CHARACTER
---------

{character_name}


SETTING
-------

{setting}


TONE
----

{tone}


ART STYLE
---------

{art_style}


OUTLINE
-------

{json.dumps(
    outline,
    ensure_ascii=False,
    indent=2
)}


Return ONLY a JSON array containing exactly 5 objects.

Each object must contain:

panel_number
caption
narration
dialogue


Rules:

- Keep the same story events.
- Keep the character consistent.
- Keep dialogue short enough for a comic panel.
- Make the story flow naturally.
- Do not add extra panels.
- Do not use markdown.
"""


    response = client.models.generate_content(

        model=GEMINI_PRO_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.85,

            response_mime_type="application/json"

        )
    )


    text = response.text.strip()


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
            "Gemini did not return valid story JSON."
        )


    story = json.loads(
        text[
            start:end + 1
        ]
    )


    if len(story) != 5:

        raise ValueError(
            "Gemini did not return exactly 5 story panels."
        )


    return story