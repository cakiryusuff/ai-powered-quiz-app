from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents.base import Document
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from pydantic import Field
from pathlib import Path
from quiz_class import Quizzes
from rich.prompt import Prompt

load_dotenv()

def main():
    document_loader = PyPDFDirectoryLoader("data")
    text = document_loader.load()

    @dataclass
    class GenerateQuizDeps:
        text: list[Document] = Field(..., description="Content of Documents")
        count_of_questions: int = Field(..., description="Number of Questions to be generated")

    agent = Agent(
        'gpt-4o-mini',
        deps_type=GenerateQuizDeps,
        result_type=Quizzes,
        system_prompt=(
            "You are an expert quiz generator. Your task is to read and analyze the given document "
            "and generate high-quality quiz questions strictly based on the **main content** of the text. "
            "Avoid asking about metadata such as the author, publication date, or formatting. Focus only on the meaningful content, "
            "such as concepts, explanations, facts, and definitions presented in the document. "
            "The total number of questions will be specified. Distribute the number of questions as evenly as possible among the three types. "
            "Ensure the questions test comprehension of the material and vary in difficulty. "
            "Use only the English Language"
        )
    )

    @agent.system_prompt
    async def add_content(ctx: RunContext[GenerateQuizDeps]) -> str:
        return f"The given text is '{ctx.deps.text}'. Generate {ctx.deps.count_of_questions} questions from given text."

    answer = int(Prompt.ask('How many questions would you like?'))

    deps = GenerateQuizDeps(text=text, count_of_questions=answer)
    result = agent.run_sync('Generate questions about given text', deps=deps)

    quiz_path = Path("data/quiz_data.json")
    quiz_path.write_text(result.data.model_dump_json(indent=4), encoding="utf-8")

    print(f"Quiz has been generated and saved to {quiz_path}")

if __name__ == "__main__":
    main()
