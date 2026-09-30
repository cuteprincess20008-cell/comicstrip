from pathlib import Path

import io
import re

import httpx

from PIL import Image

from .config import (
    HF_API_KEY,
    HF_IMAGE_MODEL,
    PANELS_DIR,
    USE_LOCAL_DIFFUSERS
)


# ---------------------------------------------------------
# SAFE FILE NAME
# ---------------------------------------------------------

def create_safe_filename(
    prompt,
    panel_number
):

    slug = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        prompt
    )

    slug = slug.strip(
        "_"
    ).lower()


    if not slug:

        slug = "comic"


    return (
        f"panel_{panel_number}_"
        f"{slug[:60]}.png"
    )


# ---------------------------------------------------------
# LOCAL DIFFUSERS
# ---------------------------------------------------------

def generate_local_image(
    prompt,
    output_path
):

    try:

        import torch

        from diffusers import (
            StableDiffusionPipeline
        )

    except ImportError as exc:

        raise RuntimeError(

            "Local Diffusers is enabled, "
            "but torch/diffusers are not installed."

        ) from exc


    if torch.cuda.is_available():

        device = "cuda"

        dtype = torch.float16

    else:

        device = "cpu"

        dtype = torch.float32


    pipe = StableDiffusionPipeline.from_pretrained(

        HF_IMAGE_MODEL,

        torch_dtype=dtype

    )


    pipe = pipe.to(
        device
    )


    result = pipe(

        prompt,

        num_inference_steps=25

    )


    image = result.images[0]


    image.save(
        output_path
    )


    return str(
        output_path
    )


# ---------------------------------------------------------
# HUGGING FACE HOSTED IMAGE GENERATION
# ---------------------------------------------------------

def generate_huggingface_image(
    prompt,
    output_path
):

    if not HF_API_KEY:

        raise RuntimeError(

            "HF_API_KEY is not configured. "
            "Add your Hugging Face API key to .env."

        )


    url = (
        "https://api-inference.huggingface.co/models/"
        f"{HF_IMAGE_MODEL}"
    )


    headers = {

        "Authorization":
        f"Bearer {HF_API_KEY}"

    }


    payload = {

        "inputs": prompt

    }


    with httpx.Client(
        timeout=180
    ) as http:

        response = http.post(

            url,

            headers=headers,

            json=payload

        )


        response.raise_for_status()


        content_type = (
            response
            .headers
            .get(
                "content-type",
                ""
            )
        )


        if "image" not in content_type:

            try:

                detail = response.json()

            except Exception:

                detail = response.text


            raise RuntimeError(

                "Hugging Face image generation failed: "
                f"{detail}"

            )


        image = Image.open(

            io.BytesIO(
                response.content
            )

        ).convert(
            "RGB"
        )


        image.save(
            output_path,
            "PNG"
        )


    return str(
        output_path
    )


# ---------------------------------------------------------
# MAIN IMAGE FUNCTION
# ---------------------------------------------------------

def generate_image(
    prompt,
    panel_number,
    art_style=""
):

    final_prompt = f"""

{prompt}

Art style:
{art_style}

Comic illustration.

Requirements:
- cinematic composition
- consistent character appearance
- detailed environment
- expressive character
- clean line art
- high quality
- no text
- no watermark
"""


    filename = create_safe_filename(

        final_prompt,

        panel_number

    )


    output_path = (
        PANELS_DIR /
        filename
    )


    if USE_LOCAL_DIFFUSERS:

        return generate_local_image(

            final_prompt,

            output_path

        )


    return generate_huggingface_image(

        final_prompt,

        output_path

    )