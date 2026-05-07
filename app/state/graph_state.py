import operator
from typing import Annotated
from typing_extensions import TypedDict


class ScreenplayState(TypedDict):
    slug: str
    brief: dict
    outline: dict       # ScreenplayOutline.model_dump() — {scenes: [...]}
    draft: str
    eval_result: dict   # StoryEval.model_dump() — populated after each story_eval run
    human_notes: dict   # {overall_notes: str} — saved production notes, fed back into generation
    current_stage: str
    story_loops: int
    note_loops: int
    errors: Annotated[list[str], operator.add]
