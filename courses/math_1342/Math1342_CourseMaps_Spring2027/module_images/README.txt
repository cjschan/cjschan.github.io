Week module images – Math 1342, Spring 2027 (Blackboard Ultra, Sec 029 course _979507_1)
One 800x800 PNG per learning module (StartHere.png, Week01.png … Week16.png), drawn to match that week's sections
(see ../README.txt WEEK GROUPING). alt_text.txt holds the alt text entered for each image in Blackboard.

Rebuild:  cd source && /usr/bin/python3 build_module_images.py
  Standard library only; each week is an SVG function in build_module_images.py, rendered with headless Chrome.
  Simulated data uses fixed seeds, so the images are reproducible.
