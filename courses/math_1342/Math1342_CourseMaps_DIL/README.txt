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
  Math1342_Weekly_ToDo.docx      student-facing "what to do this week" list for all 16 weeks, to paste
                                 into Blackboard (opens in Google Docs or Word). Rebuild with
                                 python3 source/build_weekly_todo.py after editing course_map_data.py.
  source/course_map_data.py      ALL content (Course Level Objectives, module objectives, materials,
                                 activities, assessments, MO codes, notes). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless)
  source/html/                   the generated HTML pages (handy for quick tweaks/preview)

HOW TO REBUILD AFTER EDITING
  cd ~/Desktop/Math1342_CourseMaps_DIL/source
  python3 build_course_maps.py
(The script picks the largest font size that fits every week on one page and uses it for all pages; a week that
 only fits below 9pt gets its own smaller size instead of shrinking every page.
 Requires Google Chrome in /Applications and pdfinfo from poppler; both are installed.)

HOW TO READ A PAGE (template revised Oct 27, 2026 to match the user's Week 2 sample)
  Header: "Week N", then "Course Level Objectives:" with only the CLOs used that week.
  Columns: Module Objectives | Instructional Materials | Learning Activities | Assessments | Tools.
  Module Objectives        one Bloom's-verb outcome each (long ones split), numbered across the week,
                           each ending with its CLO(s), e.g. (CLO 2, CLO 7).
  Rows                     one row per section (rows are set explicitly in course_map_data.py), with the
                           materials, activities, assessments and tools that align to that row.
  Tests                    Test N, Test N Study Guide and Practice Test N are listed in every row whose objectives
                           the test covers (Test 1: Weeks 1-5, Test 2: Weeks 6-9, Test 3: Weeks 10-13). The test
                           itself also sits on the "Also this week" line of the week it happens when that week's rows
                           don't cover it (Test 1 in Week 6, Test 2 in Week 10).
  Your Turn                each slide deck has one Your Turn; it is its own line in that section's Learning Activities,
                           separate from the Participation item (2.2 also lists the estimation activity as a Your Turn)
                           (updated Oct 28, 2026 from the decks).
  Take-Home Quizzes        listed in EVERY row whose objectives the quiz covers, in the week that teaches
                           them (e.g. Quiz 4, covering 3.1-3.3, appears in Week 6 row 2 and both Week 7
                           rows), followed by "(all objectives)" or "(objectives 8-11)" in gray.
                           Coverage comes from quizzes_fall2026/; due dates from Blackboard.
  "Also this week"         a line under the table for test sittings and retakes that do not assess that
                           week's objectives. There is no catch-all row.
  Tools                    e-Text, Online Homework -> WileyPLUS; Interactive Lecture -> WileyPLUS + StatKey;
                           Slides, quizzes -> Blackboard; Kahoot!; StatKey; other Participation -> Zoom.

CONVENTIONS USED FOR RESOURCE NAMES (RRC convention, applied to every week)
  e-Text: x.x Title | Interactive Lecture: x.x Title | Slides: x.x Title | Online Homework: x.x Title
  Participation: Topic (Kahoots named by topic, e.g. "Variables in Statistics (Kahoot!)")
  Take-Home Quiz N (Tuesday due dates) | Test N, Test N Study Guide, Practice Test N, Test N Retake, Final Exam
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

GAPS FOUND IN THE COURSE MAPS (Oct 27, 2026)
Course-level
- CLO 3 says "...using the rules of probabilities and combinatorics": no objective covers counting /
  combinatorics (P.1 covers probability rules only).
- CLO 5 says "...for both discrete and continuous random variables": no objective covers discrete random
  variables (expected value, binomial). Normal and t appear only inside inference sections.
- CLO 2 is only addressed in Weeks 1, 3 and 4; CLO 7 only in Weeks 4, 5 and 15.
Sections no Take-Home Quiz covers (assessed only by homework and tests)
- P.1 (Wk 6), 3.4 (Wk 8), 5.1 (Wk 11), 6.4 (Wk 13), 7.2 (Wk 14), 8.1 and 9.1 (Wk 15).
- Week 4 objectives 6-7 (side-by-side boxplots, difference in means): not on Quiz 2 or Quiz 3.
Rows missing a component
- No Interactive Lecture: 2.4 (Wk 4), 3.2 and 3.3 (Wk 7) - Blackboard has only e-Text and Slides.
- No Online Homework: Intro (Wk 1, row 1).
Alignment notes
- (Fixed Oct 28, 2026) Tests 2 and 3 now sit in the rows they cover, like Test 1, each with its Study Guide
  and Practice Test. Practice Test 3 (due Thu Nov 19) was added.
- (Fixed Oct 28, 2026) 3.1 Sampling Distributions now has a learning activity (Your Turn: Parameter or Statistic?).
- Participation names for Weeks 10-16 are placeholders until those Blackboard weeks are built.
