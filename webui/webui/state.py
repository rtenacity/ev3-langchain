import os
import requests
import json
import reflex as rx
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from typing import Optional

from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
load_dotenv()


api_key = os.getenv('OPENAI_API_KEY')

class CodeParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split("```")
    
    
def format_history(chats):
    formatted_messages = []
    for chat in chats:
        question = "User: " + str(chat.question)
        answer = "Assistant: " + str(chat.answer)
        formatted_messages.extend((question, answer))
    return formatted_messages

template = '''
You are a robot in a bot class that can only execute the following functions in python. You can use python syntax, providing that it is compatible with version <= 3.5. A warning, with loops. you must add a sleep statement for 0.05 seconds to avoid overheating the robot

bot.move(speed) -> Move forward at a certain speed. Accepts values from -100 to 100. Negative values mean backward. Assume default speed is 20, to be safe.

bot.stop() -> Stop the robot. No parameters. Needs to be paired with a move statement, otherwise the robot will move forever.

bot.wait(seconds) -> Wait a specified time. Accepts any positive integer. Time in seconds. 

bot.turn(angle) -> Turn an angle relative to current position. Turning done in place. Accepts angle values from -360 to 360. Negative values mean left. Stops automatically. 

bot.get_distance() -> returns the distance value from the ultrasonic sensor in inches. No parameters. A safe distance to be from any object is 10 inches.

bot.open_claw() -> opens the robot claw

bot.close_claw() -> closes the robot claw

Example syntax:

bot.move(10)
bot.wait(5)
bot.stop()
bot.turn(90)
bot.move(10)
bot.wait(5)
bot.stop()

Based on the following user instructions, walk me through a list of steps to follow the instructions in english. Then, return python code that will execute these commands. Make sure to use the format: ``` to begin the code and ``` to end it.


For example, here is a user input:

Drive for 10 seconds.

And here is what you output:

Sure, you can do that based on the robot commands:
1. Turn on the motors (we will use the default speed of 20)
2. Wait 10 seconds
3. Stop the robot. 

Now, we can generate code:

```
bot.move(20)
bot.wait(10)
bot.stop()
```
'''

human_template = "User instructions: {text}"

model = ChatOpenAI(model = 'gpt-3.5-turbo', openai_api_key = api_key)


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Demo": [],
}


def add_br_tags(input_string):
    lines = input_string.split('\n')

    lines_with_br = [line + "<br>" for line in lines]

    return '\n'.join(lines_with_br)



class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Demo"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False
    
    modal_open:bool  = False



    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        
        model = self.openai_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        
        print(self.chats[self.current_chat])
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        
        #print(type(qa.question))
        
        #print(qa.answer)
        
        history_messages = format_history(self.chats[self.current_chat])
        
        final_template = history_messages
        
        final_template.insert(0, ('system', template))
        
        final_template.append(('human', human_template))
        
        print(final_template)

        prompt = ChatPromptTemplate.from_messages(final_template)
        
        # prompt = ChatPromptTemplate.from_messages([
        #     ('system', template),  # 'template' should be a string.
            
        #     ('human', human_template)  # 'human_template' should be a string.
        # ])

        messages = prompt.format_messages(text=question)

        # Start a new session to answer the question.
        
        result = model.invoke(messages)
        
        #print(result)
        parsed = CodeParser().parse(result.content)
        
        
        #print(parsed)
        
        reason, code, garbage = parsed 

        answer_text = add_br_tags(reason)
        
        self.chats[self.current_chat][-1].answer += answer_text
        self.chats = self.chats
        
        answer_text = rf"""
```python3
{code}
```
"""     

        #print(self.chats[self.current_chat])
        
        self.chats[self.current_chat][-1].answer += answer_text
        self.chats = self.chats

        # Toggle the processing flag.
        self.processing = False

