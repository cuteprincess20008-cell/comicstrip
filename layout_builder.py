from pathlib import Path


def build_comic_layout(
    outline,
    story,
    image_paths
):

    story_by_panel = {

        item["panel_number"]:
        item

        for item in story

    }


    layout = []


    for panel in outline:

        panel_number = (
            panel["panel_number"]
        )


        story_data = story_by_panel.get(
            panel_number,
            {}
        )


        image_path = Path(
            image_paths[
                panel_number - 1
            ]
        )


        layout.append({

            "panel_number":
            panel_number,

            "title":
            panel["title"],

            "scene_description":
            panel[
                "scene_description"
            ],

            "image_prompt":
            panel[
                "image_prompt"
            ],

            "image_path":
            str(
                image_path
            ).replace(
                "\\",
                "/"
            ),

            "caption":
            story_data.get(
                "caption",
                ""
            ),

            "narration":
            story_data.get(
                "narration",
                ""
            ),

            "dialogue":
            story_data.get(
                "dialogue",
                ""
            )

        })


    return layout