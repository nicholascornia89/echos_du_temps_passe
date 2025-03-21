# Analysis

This short documentation wishes to help the user navigate the Python scripts for statistical analysis of the editions.

## The `model.py`

All utilities functions are stored in the `model.py` script.

## Adding a new piece

1. Copy the `template.py` file and rename it according to the piece's catalogue name. See `K9.py` and `BWV853.py` as examples.
2. Open the Python code in your favorite text editor and manually change the `transcriptionPath` and `pieceName` variables accordingly.
3. Populate the `arrangements` dictionary with all the editions of the piece, including an _urtext_ score as reference for further analysis. Dates of publication have to be integers, no approximation is allowed.
4. Run your `piece_name.py` code from the `analysis-env` virtual environment

From the `analysis` directory open a terminal
```bash
# load virtual environment
source analysis-env/bin/activate
# run the code, you might use python instead of python3
python3 piece_name.py
```

5. Have a look at the generated statistics in the newly created `piece_name` folder.

All statistics and metadata are stored in the `corpus.json` file.