from datetime import datetime
from pathlib import Path

from fpdf import FPDF

from .config import (
    EXPORTS_DIR,
    BASE_DIR
)


# ---------------------------------------------------------
# FIND IMAGE
# ---------------------------------------------------------

def get_asset_path(
    path_value
):

    path = Path(
        path_value
    )


    if path.is_absolute():

        return path


    if str(path).startswith(
        "static"
    ):

        return (
            BASE_DIR /
            path
        )


    return (
        BASE_DIR /
        "static" /
        path
    )


# ---------------------------------------------------------
# CREATE PDF
# ---------------------------------------------------------

def save_pdf(
    layout
):

    filename = (

        "comic_"

        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        + ".pdf"

    )


    output_path = (
        EXPORTS_DIR /
        filename
    )


    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )


    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )


    for panel in layout:

        pdf.add_page()


        # Panel title

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )


        pdf.multi_cell(

            0,

            10,

            (
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            )

        )


        # Image

        image_path = get_asset_path(

            panel[
                "image_path"
            ]

        )


        if image_path.exists():

            pdf.image(

                str(image_path),

                x=15,

                y=35,

                w=180

            )

            pdf.set_y(
                140
            )

        else:

            pdf.set_y(
                40
            )


        # Scene description

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )


        pdf.multi_cell(

            0,

            6,

            panel[
                "scene_description"
            ]

        )


        # Caption

        if panel["caption"]:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                6,
                "Caption"
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(

                0,

                6,

                panel[
                    "caption"
                ]

            )


        # Narration

        if panel["narration"]:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                6,
                "Narration"
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(

                0,

                6,

                panel[
                    "narration"
                ]

            )


        # Dialogue

        if panel["dialogue"]:

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                6,
                "Dialogue"
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(

                0,

                6,

                panel[
                    "dialogue"
                ]

            )


    pdf.output(
        str(output_path)
    )


    return (
        "/static/exports/"
        + filename
    )