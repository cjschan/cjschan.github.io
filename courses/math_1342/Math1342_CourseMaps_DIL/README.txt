MATH 1342 Weekly Course Maps – Fall 2026, Section 036 (TTh)
Generated Oct 1, 2026 from the syllabus (cjschan.github.io/courses/math_1342/fall2026_tth.html),
the lecture slides (cjschan.github.io/courses/math_1342/lecture_notes), and the Blackboard course
outline. Layout follows the Apodaca/Forsythe "Map Your Way to a Quality Course" handout.

Updated Oct 3, 2026 to match the revised syllabus: Week 10 covers all of 4.4 (was 4.4(a)); Week 15 adds
9.1 Inference for Slope and Correlation; Week 16 is the Putting It All Together review (Tue Dec 8) and the
final exam, with no separate catch-up day. Blackboard has no 9.1 items yet; the maps list them by convention.

FILES
  Week01.pdf … Week16.pdf        one landscape page per week
  Math1342_CourseMap_All.pdf     all 16 weeks in one file
  source/course_map_data.py      ALL content (Course Level Objectives, module objectives, materials,
                                 activities, assessments, MO codes, notes). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless)
  source/html/                   the generated HTML pages (handy for quick tweaks/preview)

HOW TO REBUILD AFTER EDITING
  cd ~/Desktop/Math1342_CourseMaps_DIL/source
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
                           Interactive Lecture -> WileyPLUS + StatKey; Slides -> course website; quizzes -> Assignment Tool in Blackboard;
                           tests -> Assessment Tool in Blackboard + Respondus; Kahoot!, StatKey; other
                           Participation -> LIVE_TOOL in course_map_data.py.

CONVENTIONS USED FOR RESOURCE NAMES (RRC convention, applied to every week)
  e-Text: x.x Title | Interactive Lecture: x.x Title | Slides: x.x Title | Online Homework: x.x Title
  Participation: Topic (Kahoots named by topic, e.g. "Variables in Statistics (Kahoot!)")
  Take-Home Quiz N (Tuesday due dates) | Practice Test N, Test N, Test N Retake, Final Exam
Weeks 1-6 in Blackboard were renamed to this convention on Oct 1, 2026; Weeks 7-16 follow the syllabus calendar.

Blackboard vs. syllabus discrepancies found on Oct 1, 2026 (while reading the course outline):
- Weeks 1-6 were renamed to the RRC convention on Oct 1, 2026 (e-Text: / Interactive Lecture: / Slides: /
  Online Homework: + section number and title; "Participation: Topic"; Kahoots named by topic).
- Weeks 7-16 are hidden and still use the old naming ("Online Homework x.x - MATH 1342", extra
  "Interactive Lecture: Section x.x: Student PowerPoint" items); the maps use the new convention for them too.
  No Participation items exist yet in Weeks 7-16.
- Week 7 contains a duplicate of 3.1 (already in Week 6). 5.1 sits in Week 10 (syllabus: Week 11).
  6.3 sits in Week 11 (syllabus: Week 12).
- Quiz due dates in the hidden weeks fall on Mondays (10/5, 10/12, 10/26, 11/2, 11/16, 11/23);
  the syllabus says Tuesdays. Quiz 1 is 9/9 (syllabus 9/8); Quiz 3 is 10/5 (syllabus Tue 9/29).
- Test 1 Retake, Test 2 and Test 3 have 90-minute limits; the syllabus says 2 hours per test.
- Final Exam due 12/9 in Blackboard; syllabus says Thu Dec 10. Homework 7.2 due 12/6 (expected Sun 11/29).
- The review slide deck still says the final exam is "Thursday, August 6" (summer carry-over).
