MATH 1342 Weekly Course Maps – Spring 2027, Sections 029 and 017 (MW, in person, RRC Room 8210)
  Section 029  Synonym 46254  MW 9:00–10:20 AM   syllabus: cjschan.github.io/courses/math_1342/spring2027_mw_029.html
  Section 017  Synonym 50626  MW 7:30–8:50 PM    syllabus: cjschan.github.io/courses/math_1342/spring2027_mw_017.html
Generated Oct 28, 2026 from the Fall 2026 RRC maps (Math1342_CourseMaps_RRC), regrouped for the Spring 2027 ACC
calendar (Jan 19 – May 16, 2027; Spring Break Mar 15–19; last day to withdraw Mon Apr 26). Both sections share one
calendar, so one data file builds both sets; the pages differ only in the term line under "Week N".
Layout follows the Apodaca/Forsythe "Map Your Way to a Quality Course" handout.

CHANGES FROM FALL 2026
  - 10 take-home quizzes instead of 8 (quizzes_spring2027/). Every section is on a quiz, and every quiz has StatKey
    problems; students include a screenshot of their StatKey output.
  - 2.5 is taught over two days (Part 1 Wed Feb 17, Part 2 Mon Feb 22), matching the two 2.5 Interactive Lectures.
  - 4.4 and 4.5 are on separate days. Review: Putting It All Together is Mon May 10; the final is Wed May 12 – Fri May 14.
  - Test 3 opens Fri Apr 30, after the withdrawal deadline (Mon Apr 26).
  See Math1342_CourseMap_Gaps.docx for which Fall 2026 gaps are fixed and which are still open.

FILES
  Sec029/, Sec017/               Week01.pdf … Week16.pdf, Math1342_CourseMap_All.pdf, Math1342_Weekly_ToDo.docx
  Math1342_CourseMap_Gaps.docx   Fall 2026 gaps and their Spring 2027 status, quiz coverage, section-by-section check
  source/course_map_data.py      ALL content: CLOs, one row per section (ROWS), the week grouping (WEEKS), quiz and
                                 test dates, and the two sections' term lines (SECTIONS). Edit this file.
  source/build_course_maps.py    renders HTML and prints PDFs with Google Chrome (headless), once per section
  source/build_weekly_todo.py    writes each section's Math1342_Weekly_ToDo.docx
  source/html/SecNNN/            the generated HTML pages

HOW TO REBUILD AFTER EDITING
  cd /Users/cjschan/dev/cjschan.github.io/courses/math_1342/Math1342_CourseMaps_Spring2027/source
  python3 build_course_maps.py
  /usr/bin/python3 build_weekly_todo.py      (python-docx is installed there, not in anaconda)
(The script picks the largest font size that fits every week on one page; Week 10 only fits below 9pt, so it gets
 its own smaller size. Requires Google Chrome in /Applications and pdfinfo from poppler.)

HOW TO READ A PAGE (same template as the Fall 2026 RRC/DIL maps)
  Rows                     one row per section (2.5 has one row per day), with the materials, activities and
                           assessments that align to that row.
  Take-Home Quizzes        listed in every row the quiz covers. Every quiz is due on a Monday and covers only sections
                           finished by the Wednesday before (Quizzes 3, 6 and 9 come the Monday after a test).
  Tests                    Test N, Test N Study Guide and Practice Test N are listed in every row the test covers
                           (Test 1: Intro–2.5, Test 2: P.1–4.3, Test 3: 4.4–6.5). Every test window falls in a week
                           whose rows it covers, so no test sitting is on an "Also this week" line.
  "Also this week"         retakes, Spring Break, the withdrawal deadline and the course evaluation.

WEEK GROUPING
  W1 Intro (Wed only) | W2 1.1, 1.2 | W3 1.3, 2.1 | W4 2.2, 2.3 | W5 2.4, 2.5 Part 1 | W6 2.5 Part 2, P.1
  W7 3.1, 3.2 | W8 3.3, 3.4 | Spring Break | W9 4.1, 4.2 | W10 4.3, 4.4 | W11 4.5, 5.1 | W12 6.1, 6.3
  W13 6.2, 6.4 | W14 6.5, 7.2 | W15 8.1, 9.1 | W16 Review (Mon May 10), Final Exam Wed May 12 – Fri May 14

NOTES
  - Online Homework 4.1 and 4.2 are due Sun Mar 28 (Easter; the college is closed). Move them in WEEKS if you prefer.
  - The Spring Blackboard courses aren't built yet; item names follow the Fall RRC convention, and Participation
    names marked as proposed in Fall stay proposed.
