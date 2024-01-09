from fastapi import FastAPI
from langchain.prompts.chat import ChatPromptTemplate
from typing import Optional

from langchain.schema import BaseOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

class CodeParser(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split("'''")

app = FastAPI()
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
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

Based on the following user instructions, walk me through a list of steps to follow the instructions in english. Then, return python code that will execute these commands. Make sure to use the format: \'\'\' to begin the code and \'\'\' to end it.


For example, here is a user input:

Drive for 10 seconds.

And here is what you output:

Sure, you can do that based on the robot commands:
1. Turn on the motors (we will use the default speed of 20)
2. Wait 10 seconds
3. Stop the robot. 

Now, we can generate code:

\'\'\'
bot.move(20)
bot.wait(10)
bot.stop()
\'\'\'
'''
    
human_template = "User instructions: {text}"
prompt = ChatPromptTemplate.from_messages([
    ('system', template),
    ('human', human_template)
])

model = ChatOpenAI(model = 'gpt-3.5-turbo', openai_api_key = api_key)

@app.get("/get_instructions")
async def get_instructions(user_instr: Optional[str] = None):
    if prompt:
        contains_code = True
        print(user_instr)
        messages = prompt.format_messages(text=user_instr)
        result = model.invoke(messages)
        parsed = CodeParser().parse(result.content)
        try:
            reason, code, garbage = parsed
            return {"reason": reason, "code" : code, "contains_code":contains_code }
        except:
            contains_code = False
            return {"text": parsed[0], "contains_code":contains_code }
            
        
        
    else:
        return {"message": "No prompt provided"}
