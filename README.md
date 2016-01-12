# Fix_LiftIOver_Results
LiftOver is a UCSC program that liftover annotations. It gives two output files: the main results and another file with sequences that can not be mapped to the new annotation. This program reads the error file and insert the non-mapped sequences in the main results file at the right position. This way you can keep the initial index intacted.
