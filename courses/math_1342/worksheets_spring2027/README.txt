Spring 2027 Math 1342 handouts, all built in one shared look.

  W##_<name>.docx            8 participation worksheets (Weeks 8-14)
  W##_<name>_Key.docx        their answer keys (posted in Blackboard, released 12:00 AM the day after each activity is due)
  Practice_Test_1-3.docx     Practice Tests (no keys)
  Test_1-3_Study_Guide.docx  Study Guides
  Test_1-3_Study_Guide_Solutions.docx   full worked solutions to each guide's practice problems

originals/   the Fall 2026 / Spring Blackboard files these were rebuilt from
source/      build scripts:  cd source && python3 build_docs.py   (needs python-docx and pandoc)
             worksheets.py  worksheet + key content (answers computed in the script)
             solutions.py   study-guide solutions
             convert.py     re-lays-out the practice tests and study guides from originals/
             wslib.py       the shared document style
