from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class CodeParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split("'''")

api_key = os.getenv('OPENAI_API_KEY')

template = '''
You are a robot in a robot class that can only execute the following functions in python. You can use python syntax, providing that it is compatible with version <= 3.5. A warning, with loops. you must add a sleep statement for 0.05 seconds to avoid overheating the robot

robot.move(speed) -> Move forward at a certain speed. Accepts values from -100 to 100. Negative values mean backward. Assume default speed is 20, to be safe.

robot.stop() -> Stop the robot. No parameters. Needs to be paired with a move statement, otherwise the robot will move forever.

robot.wait(seconds) -> Wait a specified time. Accepts any positive integer. Time in seconds. 

robot.turn(angle) -> Turn an angle relative to current position. Turning done in place. Accepts angle values from -360 to 360. Negative values mean left. Stops automatically. 

robot.get_distance() -> returns the distance value from the ultrasonic sensor in inches. No parameters. A safe distance to be from any object is 10 inches.

robot.open_claw() -> opens the robot claw

robot.close_claw() -> closes the robot claw

Example syntax:

robot.move(10)
robot.wait(5)
robot. stop()
robot.turn(90)
robot.move(10)
robot.wait(5)
robot.stop()

Based on the following user instructions, walk me through a list of steps to follow the instructions in english. Then, return python code that will execute these commands. Be sure to use the format: \'\'\' to begin the code and \'\'\' to end it.
'''
human_template = "User instructions: {text}"

prompt = ChatPromptTemplate.from_messages([
    ('system', template),
    ('human', human_template)
])

messages = prompt.format_messages(text="Drive forward until you detect an object.")

model = ChatOpenAI(model = 'gpt-3.5-turbo', openai_api_key = api_key)

result = model.invoke(messages)
print(result.content)
parsed = CodeParser().parse(result.content)
reason, code, garbage = parsed
print(reason)
print(code)
