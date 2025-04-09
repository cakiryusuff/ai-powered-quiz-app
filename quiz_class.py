from pathlib import Path
from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len

quiz_path = Path("quiz_generator/data/quiz_data.json")

class MCQ(BaseModel):
    question_text: str
    choices: Annotated[list[str], Len(5, 5)]
    correct_answer: str

class FITB(BaseModel):
    question_text: str
    correct_answer: str

class CQ(BaseModel):
    question_text: str
    correct_answer: str

class Quizzes(BaseModel):
    classic_questions: list[CQ]
    multiple_choice_questions: list[MCQ]
    fill_in_the_blank: list[FITB]

def load_quiz() -> Quizzes:
    return Quizzes.model_validate_json(quiz_path.read_text(encoding="utf-8"))
