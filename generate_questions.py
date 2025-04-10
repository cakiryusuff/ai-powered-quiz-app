from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents.base import Document
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext, ModelRetry
from dataclasses import dataclass
from pydantic import Field
from pathlib import Path
from quiz_class import Quizzes
from rich.prompt import Prompt

load_dotenv()

def main():
    document_loader = PyPDFDirectoryLoader("data")
    text = document_loader.load()
    
    if not text:
        raise ValueError('The text must not be empty!')
    
    answer = int(Prompt.ask('How many questions would you like?'))
    
    @dataclass
    class GenerateQuizDeps:
        text: list[Document] = Field(..., description="Content of Documents")
        count_of_questions: int = Field(..., description="Number of Questions to be generated")

    agent = Agent(
        'gpt-4o-mini',
        deps_type=GenerateQuizDeps,
        retries=5,
        result_type=Quizzes,
        system_prompt=(
            "You are an expert quiz generator. Your task is to carefully read and analyze the given document and generate high-quality quiz questions based strictly on the main content of the text."
            "Do not include questions about metadata such as the author, publication date, or formatting details. Focus only on the meaningful content—such as concepts, explanations, facts, and definitions."
            "The total number of questions will be provided. Distribute them as evenly as possible across the following three types."
            "If the total number is not divisible by 3, make the distribution as balanced as possible (e.g., 13 → 4, 4, 5)."
            "Ensure the questions vary in difficulty and accurately test comprehension of the material."
            "Generate as many questions as the number entered by the user"
            "Use only the English language."
        )
    )

    @agent.system_prompt
    async def add_content(ctx: RunContext[GenerateQuizDeps]) -> str:
        return f"The given text is '{ctx.deps.text}'. The number of questions requested by the user is {ctx.deps.count_of_questions}. "
    
    @agent.result_validator
    async def validate_result(ctx: RunContext[GenerateQuizDeps], final_response: Quizzes):
        count_of_gen_questions = len(final_response.classic_questions) + len(final_response.fill_in_the_blank) + len(final_response.multiple_choice_questions)
        if(count_of_gen_questions) != ctx.deps.count_of_questions:
            raise ModelRetry(f"Expected {ctx.deps.count_of_questions} questions but got {count_of_gen_questions}. Please regenerate the questions.")
        return final_response

    deps = GenerateQuizDeps(text=text, count_of_questions=answer)
    result = agent.run_sync('Generate questions about given text', deps=deps)

    quiz_path = Path("data/quiz_data.json")
    quiz_path.write_text(result.data.model_dump_json(indent=4), encoding="utf-8")

    print(f"Quiz has been generated and saved to {quiz_path}")

if __name__ == "__main__":
    main()
