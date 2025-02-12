import musicdiff
from musicdiff import Visualization
import music21 as m21

# Importing files:
base_path = "../../encoded_music/project_transcriptions/bach_wtc/BWV853/"
urtext_path = base_path+"/musicxml/BWV853_durr.musicxml"
arrangement_path = base_path+"/musicxml/BWV853_czerny.musicxml"
output_path = base_path+"output"

print(output_path)

# Difference between scores
#diff(urtext_path,arrangement_path,output_path+"1.pdf",output_path+"2.pdf")
Visualization.show_diffs(urtext_path,arrangement_path)
# Render scores
m21.converter.parse(output_path+"2.musicxml").show()


