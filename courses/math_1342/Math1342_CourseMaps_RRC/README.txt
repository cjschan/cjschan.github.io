MATH 1342 Weekly Course Maps – Fall 2026, Section 019 (MW, in person, RRC Room 8210)
Generated Oct 1, 2026 from the MW syllabus (cjschan.github.io/courses/math_1342/fall2026_mw.html),
the lecture slides (cjschan.github.io/courses/math_1342/lecture_notes), and the Blackboard course
outline for course 50751. Layout follows the Apodaca/Forsythe "Map Your Way to a Quality Course" handout.
The companion set for the online TTh section (036) is in ~/Desktop/Math1342_CourseMaps.

Updated Oct 3, 2026 to match the revised syllabus: Week 10 covers all of 4.4 (was 4.4(a)); Week 15 adds
9.1 Inference for Slope and Correlation; Week 16 is the Putting It All Together review (Mon Dec 7) and the
final exam, with no separate catch-up day. Blackboard has no 9.1 items yet; the maps list them by convention.

FILES
  Week01.pdf … Week16.pdf        one landscape page per week
  Math1342_CourseMap_All.pdf     all 16 weeks in one file
  Math1342_Weekly_ToDo.docx      student-facing "what to do this week" list for all 16 weeks, to paste
                                 into Blackboard (opens in Google Docs or Word). Rebuild with
                                 python3 source/build_weekly_todo.py after editing course_map_data.py.
  source/course_map_data.py      ALL content (Course Level Objectives, module objectives, materials,
                                 activities, assessments, MO codes). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless)
  source/html/                   the generated HTML pages

HOW TO REBUILD AFTER EDITING
  cd ~/Desktop/Math1342_CourseMaps_RRC/source
  python3 build_course_maps.py
(The script picks the largest font size that fits every week on one page and uses it for all pages.
 Requires Google Chrome in /Applications and pdfinfo from poppler; both are installed.)

HOW TO READ A PAGE (template revised Oct 6, 2026)
  Columns: Module Objectives | Instructional Materials | Learning Activities | Assessments | Tools.
  Module Objectives        written from what the slides actually teach; each ends with the Course Level
                           Objective(s) it supports, e.g. (CLO 2, CLO 7). The 8 CLOs (revised Oct 6, 2026)
                           match the syllabus Student Learning Outcomes; the ones used that week are
                           spelled out under the table.
  Rows                     objectives that share a learning material sit in one row, with the materials,
                           activities, assessments and tools that align to them.
  "Items that cover ..."   items aligned to objectives in more than one row; their objectives are in
                           parentheses.
  "Course resources ..."   items that do not teach or assess an objective of that week (e.g., Test 1 sits
                           in the Week 6 module but covers Weeks 1–5). Those are the gaps/misalignments
                           the handout asks you to look for.
  Tools                    derived from each item's name: e-Text and Online Homework -> WileyPLUS;
                           Interactive Lecture -> WileyPLUS + StatKey; Slides -> Blackboard; quizzes -> Assignment Tool in Blackboard;
                           tests -> Assessment Tool in Blackboard + Respondus; Kahoot!, StatKey; other
                           Participation -> LIVE_TOOL in course_map_data.py (None = no tool listed).

WEEK GROUPING (follows the Blackboard outline and the MW syllabus)
  W1 Intro, 1.1 | W2 1.2, 1.3 | W3 2.1 (Labor Day Mon) | W4 2.2, 2.3 | W5 2.4, 2.5 | W6 P.1, 3.1
  W7 3.2, 3.3 | W8 3.4, 4.1 | W9 4.2, 4.3 | W10 4.4, 4.5, 5.1 | W11 6.1, 6.3 | W12 6.2 (Veterans Day Wed)
  W13 6.4, 6.5, Quiz 8 | W14 7.2 (no class Wed) | W15 8.1, 9.1 | W16 Review (Putting It All Together), Final Exam Wed Dec 9

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
- Week 10 homework 4.4 is split into "(a)" and "(b)"; the syllabus (updated Oct 3, 2026) lists all of 4.4.
- Quiz 8 sits in Week 13 (due Mon Nov 23) in Blackboard; the maps follow that placement.
- Weeks 1-5 contain "Week N Course Map" items; these are the maps themselves and are not listed on the maps.
