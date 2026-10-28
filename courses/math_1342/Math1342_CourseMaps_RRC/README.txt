MATH 1342 Weekly Course Maps – Fall 2026, Section 019 (MW, in person, RRC Room 8210)
Generated Oct 1, 2026 from the MW syllabus (cjschan.github.io/courses/math_1342/fall2026_mw.html),
the lecture slides (cjschan.github.io/courses/math_1342/lecture_notes), and the Blackboard course
outline for course 50751. Layout follows the Apodaca/Forsythe "Map Your Way to a Quality Course" handout.
The companion set for the online TTh section (036) is in /Users/cjschan/dev/cjschan.github.io/courses/math_1342/Math1342_CourseMaps_DIL.

Updated Oct 3, 2026 to match the revised syllabus: Week 10 covers all of 4.4 (was 4.4(a)); Week 15 adds
9.1 Inference for Slope and Correlation; Week 16 is the Putting It All Together review (Mon Dec 7) and the
final exam, with no separate catch-up day. Blackboard has no 9.1 items yet; the maps list them by convention.

Updated Oct 8, 2026 from the Blackboard outline: Online Homework 3.1 is due Sun Oct 11; Week 7 lists the real
Participation items (Sampling Distribution (Kahoot!), Confidence Intervals, Bootstrap Confidence Intervals); Week 8 lists
Participation: Confidence Intervals Using Percentiles; Week 15 adds the Course Evaluation.

FILES
  Week01.pdf … Week16.pdf        one landscape page per week
  Math1342_CourseMap_All.pdf     all 16 weeks in one file
  Math1342_Weekly_ToDo.docx      student-facing "what to do this week" list for all 16 weeks, to paste
                                 into Blackboard (opens in Google Docs or Word). Rebuild with
                                 /usr/bin/python3 source/build_weekly_todo.py (python-docx is installed there, not in anaconda) after editing course_map_data.py.
  source/course_map_data.py      ALL content (Course Level Objectives, module objectives, materials,
                                 activities, assessments, rows). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless)
  source/html/                   the generated HTML pages

HOW TO REBUILD AFTER EDITING
  cd /Users/cjschan/dev/cjschan.github.io/courses/math_1342/Math1342_CourseMaps_RRC/source
  python3 build_course_maps.py
(The script picks the largest font size that fits every week on one page and uses it for all pages.
 Requires Google Chrome in /Applications and pdfinfo from poppler; both are installed.)

HOW TO READ A PAGE (template revised Oct 28, 2026 to the same row layout as the TTh/DIL maps)
  Header: "Week N", then "Course Level Objectives:" with only the CLOs used that week.
  Columns: Module Objectives | Instructional Materials | Learning Activities | Assessments | Tools.
  Module Objectives        one Bloom's-verb outcome each, numbered across the week, each ending with its
                           CLO(s), e.g. (CLO 2, CLO 7).
  Rows                     one row per section (rows are set explicitly in course_map_data.py), with the
                           materials, activities, assessments and tools that align to that row.
  Your Turn                each slide deck has one Your Turn; it is named in that section's Learning Activities.
  Take-Home Quizzes        listed in every row whose objectives the quiz covers (coverage from quizzes_fall2026/),
                           followed by "(all objectives)" or "(objectives 3-6)" in gray.
  Tests                    Test N, Test N Study Guide and Practice Test N are listed in every row whose objectives
                           the test covers (Test 1: Weeks 1-5, Test 2: Weeks 6-9, Test 3: Weeks 10-13).
  "Also this week"         a line under the table for test sittings, retakes and the course evaluation, which do
                           not assess that week's objectives (Test 1 in Week 6, Test 2 in Week 10).
  Tools                    e-Text, Online Homework -> WileyPLUS; Interactive Lecture -> WileyPLUS + StatKey;
                           Slides, quizzes, study guides -> Blackboard; tests -> Blackboard + Respondus; Kahoot!;
                           StatKey; other Participation -> LIVE_TOOL in course_map_data.py (None = no tool listed).
  Font size                one size for every page (the largest that fits); Week 10 (three sections) only fits
                           below 9pt, so it gets its own smaller size.

WEEK GROUPING (follows the Blackboard outline and the MW syllabus)
  W1 Intro, 1.1 | W2 1.2, 1.3 | W3 2.1 (Labor Day Mon) | W4 2.2, 2.3 | W5 2.4, 2.5 | W6 P.1, 3.1
  W7 3.2, 3.3 | W8 3.4, 4.1 | W9 4.2, 4.3 | W10 4.4, 4.5, 5.1 | W11 6.1, 6.3 | W12 6.2 (Veterans Day Wed)
  W13 6.4, 6.5, Quiz 8 | W14 7.2 (no class Wed) | W15 8.1, 9.1 | W16 Review (Putting It All Together), Final Exam Wed Dec 9

RESOURCE NAMES (new Blackboard convention, applied to every week)
  e-Text: x.x Title | Interactive Lecture: x.x Title | Slides: x.x Title | Online Homework: x.x Title
  Participation: Topic | Take-Home Quiz N (Monday due dates; Quiz 1 is Wed Sep 9) | Test N,
  Test N Study Guide, Practice Test N, Test N Retake, Final Exam

Blackboard (course _970761_1) vs. MW syllabus and maps, as read on Oct 8, 2026:
- Weeks 1-5 and 9-15 match the maps. Weeks 9-16 are still hidden from students.
- Week 6: Online Homework 3.1 is due Sun Oct 11 in Blackboard (not Oct 4); the maps follow Blackboard.
- Week 7 Participation items are now in Blackboard: Sampling Distribution (Kahoot!) (Mon Oct 5, a 3.1 review),
  Confidence Intervals, and Bootstrap Confidence Intervals (Wed Oct 7). The Confidence Intervals item is
  titled "Participation: Confidence Intervals.docx" and has no due date; the maps drop the ".docx".
- Week 8: "Participation: Confidence Intervals Using Percentiles" (Mon Oct 12) exists but is hidden from
  students. There is no 4.1 participation item yet; "Writing Hypotheses" is still a proposed activity.
- Week 6 has no Blackboard item for the M&M sampling-distribution activity (kept on the map as proposed).
- Week 7 has no Interactive Lecture items for 3.2 and 3.3 (the maps follow Blackboard and omit them).
- Week 15 has no 9.1 items and Week 16 holds only the Final Exam (no Review slides); the maps list them by convention.
- START HERE now also has "Course Evaluation" (listed in Week 15) and "Learn more about your course materials".
- Naming leftovers: Week 2 "1.3 Experiments and Observational Studies" and Week 3 "2.1 Categorical Variables"
  e-text items lack the "e-Text:" prefix; the three Week 11 items for 6.1 are spelled "eText:" (no hyphen).
- Week 5: the 2.5 lecture videos are "Interactive Lecture: Section 2.5 ... (Part 1)" and "(Part 2)".
  There is no Interactive Lecture for 2.4 (intentional).
- Week 10 homework 4.4 is split into "(a)" and "(b)".
- Weeks 1-15 contain "Week N Course Map" items; these are the maps themselves and are not listed on the maps.
