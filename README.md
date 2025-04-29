# AI-Powered Quiz App

This is an AI-powered quiz application developed using **Streamlit**, **Pydantic AI agents**, and **Pydantic**. The app dynamically generates questions based on a given quiz text and evaluates user answers in real-time. The answers are compared using AI-powered agents that provide feedback and scoring.

![](readme_sources/projectvideo.gif)

## Features

- **Dynamic Question Generation**: AI agents generate questions from a given text (e.g., a PDF). The questions include multiple-choice, fill-in-the-blank, and classic question types.

- **AI-Powered Scoring**: The user's answers are evaluated using **Pydantic AI agents**, which compare the user's response to the correct answer and provide a score out of 10. The comparison allows partial credit for close answers, especially for non-numeric or non-factual responses.

- **Real-Time Feedback**: Immediate feedback is provided after the user submits each answer, showing whether the answer is correct or incorrect along with the corresponding score.

- **Flexible Question Types**: The app supports three types of questions:
  - **Multiple-Choice (MCQ)**
  - **Fill-in-the-Blank (FITB)**
  - **Classic (Open-ended) Questions**

- **Customizable Number of Questions**: The user can specify how many questions they want to answer, and the app will generate and display questions accordingly.

- **Session Management**: Tracks the user’s progress throughout the quiz and shows the cumulative score as they answer each question.

## Technologies Used

- **Streamlit**: A framework for building interactive web applications.
- **Pydantic**: For data validation and structuring user inputs and outputs.
- **Pydantic AI Agents**: For generating dynamic questions and comparing answers.
- **Python 3.8+**: The programming language used for the development.
- **Dotenv**: For managing environment variables, such as API keys for external services like OpenAI.

## Installation

### Prerequisites
Ensure that Python 3.8 or higher is installed on your system. You will also need `pip` to install the dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/cakiryusuff/AI-Powered-Quiz-App.git
cd quiz-app
```
### Step 2: Set Up the Virtual Environment (optional but recommended)

Create a virtual environment to isolate project dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

Install the required dependencies:
```bash
pip install -r requirements.txt
```
### Step 4: Set Up Environment Variables

```bash
OPENAI_API_KEY=your-api-key-here
```
### Step 5: Run the Application
First you should run generate_questions for questions

```bash
python generate_questions.py
```

after that,

```bash
streamlit run app.py
```
