# Development Has Moved
Development of this tool has moved the glocate github page, https://github.com/Daniel-f-morine/glocate

## Installation / Usage

Install dependencies: ``yay -S python-pyautogui python-pyqt5 gosearch-git xdg-utils``  
run ``python /path/to/gosearch_gui_v2.py`` 

## Why use it
The other search tools powered by locate behind the scenes are catfish, which runs the much slower `find` command in addition to locate, and `Krusader` which requires you to install the dolphin file manager and it's hundreds of dependencies.  This program is designed to be more minimal, faster, and eventually more featureful compared to other implementations.
## Note
Right now the gosearch program is used behind the scenes to search for files, however, it is unmaintained and slower than GNU's plocate. Soon, I will begin the process to rewrite it with this tool instead and make further improvements to the app.

## TODO
1. Rewrite using plocate
2. More detailed user documentation
3. Fix some UI bugs
4. Add more advanced searching features, and an option to update the database from within the app
