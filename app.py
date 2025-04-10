import streamlit as st
from pydantic import BaseModel, Field
from quiz_class import load_quiz
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from dotenv import load_dotenv
import time

load_dotenv()

@st.cache_data
def get_quiz():
    return load_quiz()

quiz = get_quiz()

all_questions = (
    [("classic", q) for q in quiz.classic_questions] +
    [("mcq", q) for q in quiz.multiple_choice_questions] +
    [("fitb", q) for q in quiz.fill_in_the_blank]
)

@st.cache_data
def calculate_scores(num_questions = len(all_questions)):
    base_score = 100 // num_questions
    remainder = 100 % num_questions
    
    scores = [base_score] * num_questions
    
    for i in range(remainder):
        scores[i] += 1
    
    return scores

score_list = calculate_scores()

@dataclass
class ComparisonDependencies:
    question: str
    correct_answer: str
    user_answer: str
    score_limit: int

class ComparisonResults(BaseModel):
    description: str = Field(description="Description of comparison")
    # score: Annotated[int, Ge(0), Le(10)] = Field(description="Score of comparison")
    score: int = Field(description="Score of comparison")

@st.cache_resource
def get_comparison_agent():
    agent = Agent(
        "gpt-4o-mini",
        deps_type=ComparisonDependencies,
        result_type=ComparisonResults,
        system_prompt=(
            "Compare the correct answer with the user's answeer for th given question."
            "If the user's answer is a close variation of the correct answer (e.g., partial name like 'Donald' instead of 'Donald Vergil'), give partial credit. "
            "However, if the correct answer is a specific number or date (e.g., '1256') and the user's answer is incorrect (e.g., '1257'), do not give any points. "
            "Be strict when evaluating factual or numeric answers. "
            "Perform the comparison, return the result along with a comparison score."
        )
    )

    @agent.system_prompt
    async def dynamic_prompt(ctx: RunContext[ComparisonDependencies]) -> str:
        text = f"The question is: {ctx.deps.question}. Correct answer is: {ctx.deps.correct_answer}. User's answer is: {ctx.deps.user_answer}. \
        Compare the correct answer with the user's answer for the given question and score it out of {ctx.deps.score_limit}. "
        return text

    return agent

comparison_agent = get_comparison_agent()

if "index" not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0

if st.session_state.index >= len(all_questions):
    st.success(f"🎉 Quiz finished! Your score: {st.session_state.score}")
    if st.button("Restart"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.rerun()
    st.stop()

q_type, q = all_questions[st.session_state.index]
st.subheader(f"Question {st.session_state.index + 1}:")
st.write(q.question_text)

user_answer = (
    st.radio("Choose an answer:", q.choices, key=f"answer_{st.session_state.index}")
    if q_type == "mcq" else
    st.text_input("Your Answer:", key=f"answer_{st.session_state.index}")
)

if st.button("Submit") and user_answer:
    correct = q.correct_answer.strip().lower()
    user = user_answer.strip().lower()

    if q_type in ["classic", "fitb"]:
        deps = ComparisonDependencies(question=q.question_text, correct_answer=correct, user_answer=user, score_limit=score_list[st.session_state.index])
        result = comparison_agent.run_sync("Compare correct and user answers", deps=deps)
        score_to_add = result.data.score

        if score_to_add >= ((score_list[st.session_state.index]//2) + 1):
            st.success(f"✅ Correct! {result.data.description} (Score: {score_to_add})")
        else:
            st.error(f"❌ Incorrect! {result.data.description} (Score: {score_to_add})")

        time.sleep(4)

    else:  # mcq
        is_correct = user == correct
        score_to_add = score_list[st.session_state.index] if is_correct else 0
        if is_correct:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! Correct answer: {correct}")

        time.sleep(3)

    st.session_state.score += score_to_add
    st.session_state.index += 1
    st.rerun()