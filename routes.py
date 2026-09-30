from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse
)

from fastapi.templating import (
    Jinja2Templates
)


from .config import (
    TEMPLATES_DIR
)

from .schemas import (
    PromptRequest
)

from .gemini_flash import (
    generate_outline
)

from .gemini_pro import (
    generate_story
)

from .image_generator import (
    generate_image
)

from .layout_builder import (
    build_comic_layout
)

from .exporters import (
    save_pdf
)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

templates = Jinja2Templates(

    directory=str(
        TEMPLATES_DIR
    )

)


# ---------------------------------------------------------
# COMPLETE COMIC GENERATION
# ---------------------------------------------------------

def generate_comic(
    data: PromptRequest
):

    # Step 1:
    # Generate 5-panel outline

    outline = generate_outline(

        data.story_prompt,

        data.character_name,

        data.setting,

        data.tone,

        data.art_style

    )


    # Step 2:
    # Generate narration/dialogue

    story = generate_story(

        outline,

        data.character_name,

        data.setting,

        data.tone,

        data.art_style

    )


    # Step 3:
    # Generate images

    image_paths = []


    for panel in outline:

        image_path = generate_image(

            panel[
                "image_prompt"
            ],

            panel[
                "panel_number"
            ],

            data.art_style

        )


        image_paths.append(
            image_path
        )


    # Step 4:
    # Build layout

    layout = build_comic_layout(

        outline,

        story,

        image_paths

    )


    # Step 5:
    # Export PDF

    pdf_path = save_pdf(
        layout
    )


    return (
        layout,
        pdf_path
    )


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)

async def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={}

    )


# ---------------------------------------------------------
# GENERATE FROM WEB FORM
# ---------------------------------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse
)

async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)

):

    try:

        data = PromptRequest(

            story_prompt=
            story_prompt,

            character_name=
            character_name,

            setting=
            setting,

            tone=
            tone,

            art_style=
            art_style

        )


        layout, pdf_path = (
            generate_comic(
                data
            )
        )


        return templates.TemplateResponse(

            request=request,

            name=
            "comic_preview.html",

            context={

                "layout":
                layout,

                "pdf_path":
                pdf_path

            }

        )


    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "error":
                str(exc)

            },

            status_code=500

        )


# ---------------------------------------------------------
# JSON API
# ---------------------------------------------------------

@router.post(
    "/generate-comic/json"
)

async def generate_json(

    data: PromptRequest

):

    try:

        layout, pdf_path = (
            generate_comic(
                data
            )
        )


        return {

            "success":
            True,

            "layout":
            layout,

            "pdf_path":
            pdf_path

        }


    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        )


# ---------------------------------------------------------
# EXPORT SUCCESS PAGE
# ---------------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse
)

async def export_success(

    request: Request,

    pdf: str = ""

):

    return templates.TemplateResponse(

        request=request,

        name=
        "export_success.html",

        context={

            "pdf_path":
            pdf

        }

    )


# ---------------------------------------------------------
# IMAGE TEST API
# ---------------------------------------------------------

@router.post(
    "/test-image"
)

async def test_image(

    prompt: str = Form(...)

):

    try:

        image_path = generate_image(

            prompt,

            0,

            "comic book"

        )


        return {

            "success":
            True,

            "image_path":
            image_path

        }


    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        )