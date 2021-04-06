# PyBingo
Bingo generator written mostly out of boredom.

Needs Pillow to work, not sure which is the lowest level supported but 8.2.0+ works
https://pillow.readthedocs.io/en/stable/

All the boards are 5x5 with a free space in the middle.
All the boards generated have the same fields, but in a different order.
LastRun can be saved and ran again, if needed.
Requires minimum of 25 data entries into the data csv file.
Data can be tagged, and ignored if needed.
Almost all the parameters can be tweaked from settings.txt

First time run checklist:
- Install Pillow
- Copy defaultsettings.txt and rename it settings.txt
- Configure settings as you see fit

For better looking boards:
- Get a truetypefont from somewhere and put in the working directory
- Also get an random image and place it next to the font

Attentions/maybe going to be improved:
- All the required files must be in the working directory
  - centerimage, settings and font
- If no font is present "better than nothing" font is used, which size cannot be changed

All the generated boards are saved into generated/ with given names {epoch}board{x}.jpg
