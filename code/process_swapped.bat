@echo off
setlocal

set INKSCAPE="C:\Program Files\Inkscape\bin\inkscape.exe"
set INPUT_DIR=C:\Users\MilesIdeaPad\Documents\python\Swapped
set OUTPUT_DIR=C:\Users\MilesIdeaPad\Documents\python\Processed

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

for %%F in ("%INPUT_DIR%\*_swapped.svg") do (
    %INKSCAPE% "%%~fF" --batch-process --actions="select-all;object-to-path;export-filename:%OUTPUT_DIR%\%%~nF_processed.svg;export-plain-svg;export-do"
)

echo Done.
pause
