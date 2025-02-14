import musicdiff
import music21 as m21
from pathlib import Path

# Importing files:
# base_path = "../../encoded_music/project_transcriptions/bach_wtc/BWV853/"
urtext_path = "K9_gilbert.musicxml"
arrangement_path = "K9_czerny.musicxml"
output_path = "output"


# Difference between scores pdfs and MusicXML files are generated

# See integer mapping of detail level
# https://gregchapman-dev.github.io/musicdiff/musicdiff/detaillevel.html#DetailLevel


def generate_differences():
    musicdiff.diff(
        urtext_path,
        arrangement_path,
        output_path + "_gilbert.pdf",
        output_path + "_czerny.pdf",
        force_parse=True,
        visualize_diffs=True,
        print_text_output=False,
        detail=musicdiff.DetailLevel.Slurs,
    )


generate_differences()
