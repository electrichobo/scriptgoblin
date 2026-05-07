import operator
from typing import Annotated
from typing_extensions import TypedDict


class ScreenplayState(TypedDict):
    slug: str
    brief: dict
    outline: dict   # ScreenplayOutline.model_dump() — {scenes: [...]}
    draft: str
    current_stage: str
    story_loops: int
    note_loops: int
    errors: Annotated[list[str], operator.add]
