## License
The code in this director was generated in collaboration with ChatGPT 5.4. MIT License.

# Notes
replace_digits.batch.py and replace_digits_solutions_batch.py are python scripts that were used to swap Aarabic numberals for Mongolian numerals in the Sudoku SVG files (example SVG files - #1.SVG and #1_solved.svg - are included; the scripts, however, assume that 99 SVG files are in the source directory).

the .bat files further processed the SVG files using Inkscape (https://inkscape.org/) after running the python scripts. This step was required for Scribus (https://sourceforge.net/projects/scribus/) to properly display the SVG files. 

Scribus is the open-source desktop publish software we used to create the book pages. We took advantage of the ability to automate repetitive tasks in Scribus using Python scripts - puzpagesvg.py; and solutionpages.py which add one of the 99 puzzles in the order specified in page_dictionary.csv. These scripts are to be executed within Scribus.
