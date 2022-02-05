import logging
import os
import serial
from twilio.rest import Client

from flask import Flask
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

# Twilio Credentials
account_sid = 'ACdaeeb95cef452cff95c81234757f1b95'
auth_token = '5ce4496a55b7ca3770ec4a731aca88ce'

client = Client(account_sid, auth_token)

# Twilio Functions
def bad_message():
        client.messages.create(
            to='whatsapp:+917827794110',
            from_='whatsapp:+17752568757',
            body="Hey, looks like it's a bad idea to go to Campus Point today. In case you decide to go, take proper precautions!")

def good_message():
        client.messages.create(
            to='whatsapp:+917827794110',
            from_='whatsapp:+17752568757',
            body="The weather and waves at Campus Point are looking good! If you're planning on going, you'll have a great time!")

@ask.launch
def launch():
    speech_text = 'Welcome to Sand Pie.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('BeachIntent')
def Beach_Intent():
    ser = serial.Serial('/dev/ttyACM1', 9600)
    ser_data = ser.readline().decode('utf-8').rstrip()

    if int(ser_data) < 350:
        bad_message()
        return statement('Be careful, the weather and waves at Campus Point look concerning.')

    elif int(ser_data) > 350:
        good_message()
        return statement('Weather and waves at Campus Point are looking good!')
        
    else:
        return statement('Sorry, data could not be processed.')

@ask.intent('StatusIntent')
def Status_Intent():
    speech_text = 'The hardware is healthy and fully functional.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me about the weather at Campus Point or the status of the apparatus!'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    speech_text = 'Goodbye!'
    return statement(speech_text).simple_card(speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    speech_text = 'Goodbye!'
    return statement(speech_text).simple_card(speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
