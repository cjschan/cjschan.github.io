Week module images – Math 1342, Spring 2027 (Blackboard Ultra, Sec 029 course _979507_1)
One 800x800 PNG per learning module (StartHere.png, Week01.png … Week16.png), drawn to match that week's sections
(see ../README.txt WEEK GROUPING). alt_text.txt holds the alt text entered for each image in Blackboard.

Rebuild:  cd source && /usr/bin/python3 build_module_images.py
  Standard library only; each week is an SVG function in build_module_images.py, rendered with headless Chrome.
  Simulated data uses fixed seeds, so the images are reproducible.

Start Here page images (replace the template's stock photos):
  CourseSchedule.png, TechRequirements.png  1200x800, drawn by the same script (PAGES list)
  Lock4e_Cover.png  publisher cover image, downloaded Nov 2026 from the WileyPLUS 4e page
                    (wileyplus.com/wp-content/uploads/2025/08/Lock-4e-Cover.png); credited "Cover image: Wiley"

Course banner (Blackboard "Course Image": banner across the top of the course page and, center-cropped, the course card):
  CourseBanner.png  2400x480 (1200x240 at 2x). Rebuild: cd source && /usr/bin/python3 build_banner.py
  ACC logo + "MATH 1342 / Elementary Statistics" centered; a simulated sample (fixed seed) as a pale dotplot with
  its normal curve along the bottom. source/ACC-District-Color-Logo.png is ACC's official full-color logo,
  downloaded Nov 2026 from austincc.edu/wp-content/uploads/ACC-District-Color-Logo-PNG.png.
  Alt text: "Austin Community College logo with Math 1342, Elementary Statistics, above a dotplot shaped like a bell curve"
