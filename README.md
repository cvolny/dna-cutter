# dna-cutter

Splitting data/example_gnome.txt by the rules defined in data/cutters.txt:

`python src/cutter.py data/cutters.txt < data/example_gnome.txt | tee data/example_gnome_split.txt`

Validating that the files contain the same data length and contents (by stripping newlines from both):

`./src/validate.sh data/example_gnome.txt data/example_gnome_split.txt`
