# TraditionalMongolianNumeralSudoku
this is a supporting repository for the book entitled, Mongolian Script Sudoku,
by Altanzaya Yansanjav, Terbish Batbold, Miles Dyck, Tergel Batbold

## Some notes on how the book was created

Terbish Batbold made the puzzles with the Sudoku puzzle creation app at  https://sudokumaker.app/. Anyone who is interested in making their own Sudoku puzzles should visit this site. Two key features on this site were invaluable for our project: 1) any puzzle can be tested to ensure the solution is unique; and 2) the puzzle and the solutions can be shared through a link or as an image file. We thank Sir Xemic (https://sirxemic.com/), for developing this app and making it freely available. Send him a “tip” (https://ko-fi.com/sirxemic) or give him a shout out on social media. 

Each puzzle with and without solutions was exported from https://sudokumaker.app/ as scalable vector graphics (SVG) files. The next challenge was to replace the Arabic numerals in the puzzles with Mongolian numerals (see /font/README.md, and /font/Khatan_numerals.OTF). The solution was to modify the SVG files using Python codes developed with the help of ChatGPT (see /code/README.md). 

Page design and layout for the book were completed using the open-source, desktop publishing software, Scribus (https://sourceforge.net/projects/scribus/). With 99 puzzles plus solutions, we took advantage of the ability to automate repetitive tasks in Scribus using Python scripts (see code /README.md).   
