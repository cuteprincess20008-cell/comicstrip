from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles
)

from .config import (
    STATIC_DIR
)

from .routes import (
    router
)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(

    title="ComicCraft",

    description=(
        "AI Comic Story Creator "
        "using Gemini and Stable Diffusion."
    ),

    version="1.0.0"

)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

app.mount(

    "/static",

    StaticFiles(
        directory=str(
            STATIC_DIR
        )
    ),

    name="static"

)


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

app.include_router(
    router
)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get(
    "/health"
)

async def health():

    return {

        "status":
        "ok",

        "service":
        "ComicCraft"

    }