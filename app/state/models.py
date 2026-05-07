from pydantic import BaseModel


class SceneOutlineItem(BaseModel):
    number: int
    location: str
    time_of_day: str
    purpose: str
    objective: str
    turning_point: str
    beats: list[str]


class ScreenplayOutline(BaseModel):
    scenes: list[SceneOutlineItem]


class StoryEval(BaseModel):
    score: int
    feedback: str
    should_rewrite: bool
    notes: list[str]


class SceneTag(BaseModel):
    scene_number: int
    location: str
    time_of_day: str
    characters: list[str]
    summary: str


class SceneTags(BaseModel):
    scenes: list[SceneTag]


class VerifyReport(BaseModel):
    notes_applied: list[str]
    notes_missing: list[str]
    passed: bool
