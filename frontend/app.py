from flask import Flask, render_template, request, jsonify 
from openai import OpenAI


import os
from dotenv import load_dotenv
  

load_dotenv()
  
  
app = Flask(__name__) 

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')) 
  
# OpenAI API Key 
  
def get_completion(prompt): 
    print(prompt) 
    query = client.chat.completions.create(
        model = 'gpt-3.5-turbo', 
        messages= [
            {
                "role" : "system",
                "content": '''
                You are a helpful AI assistant! Just note, your result is being returned in html, so for new lines, you need to add a <br>, especially when writing code.
                '''
            },
            {
                "role" : "user",
                "content": prompt
            }
        ], 
        
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        n=1
        
        )
  
    response = query.choices[0].message.content
    return response 
  
@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
    if request.method == 'POST': 
        print('step1') 
        prompt = request.form['prompt'] 
        response = get_completion(prompt) 
        print(response) 
  
        return {'response': response}
    return render_template('index.html') 
  
  
if __name__ == "__main__": 
    app.run(debug=True) 