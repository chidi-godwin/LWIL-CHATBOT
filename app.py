from flask import Flask, request, make_response, jsonify
import json
import os
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>hello world</h1>"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    action = req.setdefault('queryResult', {'acion': 'form'}).get('action')
    print(action)
    if action == "form":
        return make_response(form_response())
    

@app.route('/location', methods=['POST'])
def location():
    req = request.get_json(silent=True, force=True)
    with open('data.json', 'w') as data:
        json.dump(req, data)
    return

def form_response():
    with open('data.json') as f:
        form_data = json.loads(f.read())
    date, time = form_data.get('Date').split('T')
    form_data['Date'] = date
    form_data['Time'] = time
    data = {
        "fulfillmentText": """{} your appointment has been set for {} at {}, you'll recieve a call on {} to remind you ahead of time""".\
                        format(form_data['Name'], form_data['Date'], 
                        form_data['Time'], form_data['Phone'])
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()