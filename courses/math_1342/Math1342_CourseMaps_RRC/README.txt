MATH 1342 Weekly Course Maps – Fall 2026, Section 019 (MW, in person, RRC Room 8210)
Generated Oct 1, 2026 from the MW syllabus (cjschan.github.io/courses/math_1342/fall2026_mw.html),
the lecture slides (cjschan.github.io/courses/math_1342/lecture_notes), and the Blackboard course
outline for course 50751. Layout follows the Apodaca/Forsythe "Map Your Way to a Quality Course" handout.
The companion set for the online TTh section (036) is in ~/Desktop/Math1342_CourseMaps.

FILES
  Week01.pdf … Week16.pdf        one landscape page per week
  Math1342_CourseMap_All.pdf     all 16 weeks in one file
  source/course_map_data.py      ALL content (course objectives, module objectives, materials,
                                 activities, assessments, # codes). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless)
  source/html/                   the generated HTML pages

HOW TO REBUILD AFTER EDITING
  cd ~/Desktop/Math1342_CourseMaps_RRC/source
  python3 build_course_maps.py
(The script picks the largest font size that fits every week on one page and uses it for all pages.
 Requires Google Chrome in /Applications and pdfinfo from poppler; both are installed.)

HOW TO READ A PAGE
  Course-level Objectives  only the Common Course Objectives this week's module objectives address,
                           numbered as in the syllabus (CO1-CO12).
  Module-level Objectives  written from what the slides actually teach; each ends with the course
                           objective(s) it supports, e.g. (CO2, CO4).
  #                        module objective(s) an item aligns to ("All" = every module objective
                           of the week). "None" marks items that do not teach or assess a module
                           objective of that week (e.g., Test 1 sits in Week 6 but covers Weeks 1-5).

WEEK GROUPING (follows the Blackboard outline and the MW syllabus)
  W1 Intro, 1.1 | W2 1.2, 1.3 | W3 2.1 (Labor Day Mon) | W4 2.2, 2.3 | W5 2.4, 2.5 | W6 P.1, 3.1
  W7 3.2, 3.3 | W8 3.4, 4.1 | W9 4.2, 4.3 | W10 4.4(a), 4.5, 5.1 | W11 6.1, 6.3 | W12 6.2 (Veterans Day Wed)
  W13 6.4, 6.5, Quiz 8 | W14 7.2 (no class Wed) | W15 8.1, Review | W16 Review, Final Exam Wed Dec 9

RESOURCE NAMES (new Blackboard convention, applied to every week)
  e-Text: x.x Title | Interactive Lecture: x.x Title | Slides: x.x Title | Online Homework: x.x Title
  Participation: Topic | Take-Home Quiz N (Monday due dates; Quiz 1 is Wed Sep 9) | Practice Test N,
  Test N, Test N Retake, Final Exam

Blackboard (course _970761_1) vs. MW syllabus, as read on Oct 1, 2026 (second pass):
- All 16 weeks now use the new naming (e-Text: / Interactive Lecture: / Slides: / Online Homework: + section
  number and title; "Participation: Topic"; Kahoots named by topic with "(Kahoot!)").
- Small leftovers: Week 2 "1.3 Experiments and Observational Studies" and Week 3 "2.1 Categorical Variables"
  e-text items lack the "e-Text:" prefix; the three Week 11 items for 6.1 are spelled "eText:" (no hyphen).
- Week 7 has no Interactive Lecture items for 3.2 and 3.3 (the maps follow Blackboard and omit them).
- Week 5: the 2.5 lecture videos are "Interactive Lecture: Section 2.5 ... (Part 1)" and "(Part 2)".
  There is no Interactive Lecture for 2.4 (intentional).
- Week 10 homework 4.4 is split into "(a)" and "(b)"; the syllabus lists 4.4(a) only.
- Quiz 8 sits in Week 13 (due Mon Nov 23) in Blackboard; the maps follow that placement.
- Weeks 1-5 contain "Week N Course Map" items; these are the maps themselves and are not listed on the maps.
- P.1 probability rules are not in the 12 Common Course Objectives (they are in Student Learning Outcome 3).
