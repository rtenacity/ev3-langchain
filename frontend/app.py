from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import markdown  # Import markdown module

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_completion(prompt):
    print(prompt)
    query = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": '''You are a helpful AI assistant!'''},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        n=1
    )

    response = query.choices[0].message.content
    
    # response = '''How are you!'''
    # Convert Markdown to HTML
    # html_response = markdown.markdown(response)
    return response

@app.route("/", methods=['POST', 'GET'])
def query_view():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = get_completion(prompt)
        return {'response': response}
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
