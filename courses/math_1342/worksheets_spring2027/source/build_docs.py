"""Build every Spring 2027 Math 1342 handout in the shared look.

    python3 build_docs.py        (needs python-docx; pandoc on PATH)

Outputs (in ../):
  W##_<name>.docx / W##_<name>_Key.docx     8 participation worksheets + answer keys
  Practice_Test_N.docx                       Practice Tests 1-3 (no keys)
  Test_N_Study_Guide.docx                    Study Guides 1-3
  Test_N_Study_Guide_Solutions.docx          full worked solutions to the guides' practice problems
  Final_Exam_Study_Guide[_Solutions].docx    final exam guide + worked solutions (final_guide.py)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from wslib import Doc                      # noqa: E402
from worksheets import WORKSHEETS          # noqa: E402
from solutions import SOLUTIONS            # noqa: E402
import convert                             # noqa: E402

OUT = HERE.parent
ORIG = OUT / "originals"
MEDIA = HERE / "media"

COVERS = {1: "Covers Sections 1.1 – 2.5",
          2: "Covers Sections P.1, 3.1 – 3.4, and 4.1 – 4.3",
          3: "Covers Sections 4.4, 4.5, 5.1, and 6.1 – 6.5"}


def build_worksheets():
    for stem, title, sub, fn in WORKSHEETS:
        for key in (False, True):
            d = Doc("Answer Key" if key else "Participation Worksheet", title, sub, key=key)
            fn(d)
            d.save(OUT / f"{stem}{'_Key' if key else ''}.docx")


def build_tests_and_guides():
    for n in (1, 2, 3):
        d = Doc("Practice Test", f"Practice Test {n}", COVERS[n])
        convert.practice_test(d, ORIG / f"Practice_Test_{n}.docx", MEDIA / f"pt{n}")
        d.save(OUT / f"Practice_Test_{n}.docx")

        d = Doc("Study Guide", f"Test {n} Study Guide", COVERS[n], name_line=False)
        convert.study_guide(d, ORIG / f"Test_{n}_Study_Guide.docx", MEDIA / f"sg{n}", n)
        d.save(OUT / f"Test_{n}_Study_Guide.docx")

        d = Doc("Solutions", f"Test {n} Study Guide: Solutions", COVERS[n] + "  ·  Full worked solutions", name_line=False)
        d.para(f"These are complete solutions to the Practice Problems in the **Test {n} Study Guide**. "
               "Try each problem on your own first, then compare your work step by step.", italic=False)
        for k, (q, sol) in enumerate(SOLUTIONS[n], 1):
            d.problem(f"Problem {k}")
            d.para(q)
            d.d.paragraphs[-1].paragraph_format.keep_with_next = True
            d.key = True
            d.answer(sol, indent=0)
            d.key = False
        d.end("End of solutions")
        d.save(OUT / f"Test_{n}_Study_Guide_Solutions.docx")


if __name__ == "__main__":
    build_worksheets()
    build_tests_and_guides()
    import final_guide                     # needs matplotlib + scipy
    final_guide.build(OUT)
    print("built", len(list(OUT.glob("*.docx"))), "documents in", OUT)
