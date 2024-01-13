from flask import Flask, render_template, request, jsonify
import os
import http.client
import json
from robot import Robot

#bot = Robot()
app = Flask(__name__)

def add_br_tags(input_string):
    lines = input_string.split('\n')

    lines_with_br = [line + "<br>" for line in lines]

    return '\n'.join(lines_with_br)

def get_completion(prompt):
    conn = http.client.HTTPConnection("127.0.0.1", 8000)
    #conn = http.client.HTTPConnection("192.168.68.64", 8000)

    headersList = {}
    payload = ""

    prompt_adj = prompt.replace(" ", "%20")
    request = "/get_instructions?user_instr=" + prompt_adj
    conn.request("GET", request, payload, headersList)
    response = conn.getresponse()
    result = response.read().decode('utf-8')
    
    response_dict = json.loads(result)
    print(response_dict)
    if response_dict['contains_code']:
        print(add_br_tags(response_dict['code'].replace('    ', '&emsp;')))
        return add_br_tags(response_dict['reason']) + add_br_tags(response_dict['code'].strip().replace('    ', '&emsp;'))
    else:
        return response_dict['text']

@app.route("/", methods=['POST', 'GET'])
def query_view():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = get_completion(prompt)
        return jsonify({'response': response})
    return render_template('index.html')

# if __name__ == "__main__":
#     app.run(host='192.168.68.53', port=5000 )
    
if __name__ == "__main__":
    app.run(port=5000 )
