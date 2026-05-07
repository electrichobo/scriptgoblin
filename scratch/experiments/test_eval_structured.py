"""
Scratch test: validate StoryEval structured output with the verifier model.

Run from project root:
    python scratch/experiments/test_eval_structured.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import VERIFIER_MODEL
from app.llm.ollama_client import get_client
from app.state.models import StoryEval

SAMPLE_DRAFT = """\
FADE IN:

INT. HOSPITAL WAITING ROOM - DAY

Fluorescent lights. Plastic chairs. MARCUS (40s, still in work clothes) sits
alone, staring at nothing.

A NURSE crosses to him.

                    NURSE
          Mr. Reyes? The doctor will see you now.

Marcus doesn't move.

                    MARCUS
          Is she—

                    NURSE
          Please come with me.

He stands slowly.

CUT TO:

INT. HOSPITAL CORRIDOR - CONTINUOUS

Marcus follows the nurse. Every door looks the same.

                    MARCUS
                (quietly)
          I should have been there.

The nurse says nothing.

FADE OUT.
"""

SYSTEM = "You are a story editor evaluating a screenplay draft. Return strict JSON only."

HUMAN = f"""Evaluate the following screenplay excerpt.

{SAMPLE_DRAFT}

Criteria:
- score (1-10): overall craft quality
- feedback: one paragraph of honest editorial notes
- should_rewrite: true if score is below 7 or there are structural problems
- notes: 1-3 specific, actionable notes
"""


def main():
    print(f"Model:  {VERIFIER_MODEL}")
    print(f"Schema: StoryEval")
    print("-" * 50)

    llm = get_client(VERIFIER_MODEL)
    structured = llm.with_structured_output(StoryEval)

    try:
        result = structured.invoke([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=HUMAN),
        ])
        print("PASS — structured output returned cleanly\n")
        print(f"  score:          {result.score}")
        print(f"  should_rewrite: {result.should_rewrite}")
        print(f"  feedback:       {result.feedback}")
        print(f"  notes:")
        for n in result.notes:
            print(f"    - {n}")
    except Exception as e:
        print(f"FAIL — {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
