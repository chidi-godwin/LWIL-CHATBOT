from flask import Flask, request, make_response, jsonify
import json
import os
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    date, time = req.get('queryResult').get('parameters').values()
    date, time = formatTimeAndDate(time, date)
    data = {
        "fulfillmentText": "Your appointment has been set for {} at {}".\
                        format(date, time)
    }
    return make_response(jsonify(data))

def formatTimeAndDate(time, date):
    """
        format dates and time parameter from dialogflow to a
        option.
    """
    date = date.split('T')[0]
    hours, mins = time.split('T')[1].split('+')[0].split(':')[:2]
    period = ' am' if int(hours) < 12 else ' pm'
    hours = hours if int(hours) < 12 else str(int(hours)-12)
    time = hours + ':' + mins + period
    return (date, time)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0')