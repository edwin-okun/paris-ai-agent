import os
from openai import OpenAI
from typing import Optional

# Constants
MODEL = "gpt-4o-mini"
SYSTEM_PROMPT = (
    "You are a virtual Parisian expert, delivering valuable insights into the city's iconic landmarks and hidden treasures. "
    "Use a professional & user friendly tone when interacting with tourists. "
    "If the question is not in English proceed to answer it in the language asked. "
    "If the question you receive is within the parisian scope answer it to the best of your knowledge otherwise, "
    "answer with 'Sorry, I cant answer that question, ask Parisian related questions'"
)

class ParisAITravelGuide:
    """
    AI-powered travel guide for Paris using OpenAI's API.
    Adheres to SOLID, KISS, and DRY principles.
    Tracks usage statistics.
    """

    def __init__(self, model: str = MODEL, client: Optional[OpenAI] = None):
        self.model = model
        self.client = client or OpenAI()
        self.usage_count = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

    def get_response(self, conversation: list, temperature: float = 0.0) -> str:
        """
        Get AI response for a given user prompt.
        Tracks usage statistics.
        """
        
        response = self.client.chat.completions.create(
            messages=conversation,
            model=self.model,
            temperature=temperature
        )
        # Update usage statistics
        usage = getattr(response, "usage", None)
        if usage:
            self.total_prompt_tokens += usage.prompt_tokens
            self.total_completion_tokens += usage.completion_tokens
            self.total_tokens += usage.total_tokens
        self.usage_count += 1

        return response.choices[0].message.content

    def print_usage(self):
        """
        Print usage statistics.
        """
        print("\n Usage")
        print(f"Total questions answered: {self.usage_count}")
        print(f"Total prompt tokens used: {self.total_prompt_tokens}")
        print(f"Total completion tokens used: {self.total_completion_tokens}")
        print(f"Total tokens used: {self.total_tokens}")

# Example usages:
paris_guide = ParisAITravelGuide()
user_questions = [
    "How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?",
    "Where is the Arc de Triomphe?",
    "What are the must-see artworks at the Louvre Museum?"
]

conversation = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
for i, question in enumerate(user_questions, start=1):
    # add question to conversation
    conversation.append({
        "role": "user",
        "content": question
    })
    # generate assistant msg
    answer = paris_guide.get_response(conversation)
    # add generated assistant msg to conversation
    conversation.append({
        "role": "assistant",
        "content": answer
    })
    print(f"Question {i}: {question}\nAnswer: {answer}\n")

# Print usage statistics
paris_guide.print_usage()
