import random
from flask import Flask, request
from pymessenger.bot import Bot
from decouple import config
import sys

app = Flask(__name__)       # Initializing our Flask application

# this is a test

ACCESS_TOKEN = config('TOKEN_A')
VERIFY_TOKEN = config('TOKEN_V')

bot = Bot(ACCESS_TOKEN)

# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():

    inputToState = {
        "vic":"vic", "victoria":"vic", "qld":"qld", "queensland":"qld", "act":"act",
        "wa":"wa", "western australia":"wa", "sa":"sa", "south australia":"sa", "northern territory":"nt", "nt":"nt", "tasmania":"tas", "tas":"tas"
    }

    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        text = message['message'].get('text')
                        text = text.lower()
                        if text == "hi":
                            response_sent_text = "Hi! So you wanna go outside... First I gotta ask, have you been out of NSW in the last 2 weeks?"
                            send_message(recipient_id, response_sent_text) 
                        elif text == "yes":
                            response_sent_text = check_visited(text)
                            send_message(recipient_id, response_sent_text)
                        elif text == "no":
                            response_sent_text = check_visited(text)
                            send_message(recipient_id, response_sent_text)
                        elif text in inputToState:
                            state = inputToState[text]
                            response_sent_text = check_states(state)
                            send_message(recipient_id, response_sent_text)
                            if state == 'vic':
                                response_sent_text = 'For self iso tips, check out https://www.nsw.gov.au/covid-19/self-isolation'
                                send_message(recipient_id, response_sent_text) 
                            else:
                                response_sent_text = 'Where are you planning on going today?'
                                send_message(recipient_id, response_sent_text) 
                        else:
                            response_sent_text = check_restricted_activities(text)
                            send_message(recipient_id, response_sent_text)

                    # if user send us a GIF, photo, video or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_text = get_message()

                        send_message(recipient_id, response_sent_text)
                   
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by Facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message():
    sample_responses = ["yo", "hi"]
    # return selected item to the user
    return random.choice(sample_responses)


# Uses PyMessenger to send response to the user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

def check_visited(message):
    message = message.lower()
    if message == "no":
        response = "Yay! So where are you planning on going today?"
    elif message == "yes":
        response = "Cool! Which state did you come from?"
    else:
        response = "Please send yes or no"
    return response

def check_states(message):
    
    stateToResponse = {
        "vic":"Oh no! You gotta stay at home for 14 days from when you left victoria. Stay strong fam 🤩",
        "unknown":"Ooh that's exciting, I don't know where that is! Check here for more details: https://www.nsw.gov.au/covid-19/self-isolation",
        "qld":"All good, no self isolation for you 😁",
        "act":"All good, no self isolation for you 😁",
        "wa": "All good, no self isolation for you 😁",
        "sa": "All good, no self isolation for you 😁",
        "nt": "All good, no self isolation for you 😁",
        "tas": "All good, no self isolation for you 😁"
    }
    message = message.lower()
    return stateToResponse[message]
    

def check_restricted_activities(message):
    closed_activities = ['night club', 'music festival']

    restricted_activities = {
        
        "pub": "10 or less friends per table/booking + alcohol can only be consumed by seated customers. Got it?",
        "visit family and friends at home": "20 visitors MAX unless you want to be FINED :(",
        "park": "20 people gatherings MAX. (You can have 20+ dogs tho 🐕).",
        "gym": "Only 20 people per class so make sure you BOOK before going in 💪."
    }

    message = message.lower()

    if message in restricted_activities:
        condition = restricted_activities.get(message)
        response = f"{message.upper()}? {condition}"
    elif message in closed_activities:
        response = f"Sorry {message}s are CLOSED! You can't go."
    else:
        response = "1.5M DISTANCE BETWEEN PEOPLE PLEASE.\nThere's also restricted numbers for people in indoor places at a time btw. (4 metre square rule)."

    return response


# Add description here about this if statement.
if __name__ == "__main__":
    app.run()
