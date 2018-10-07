"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6
For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import time


# --------------- Helpers that build all of the responses ----------------------python

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    if title != None:
        return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': "Focus Timer",
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
    else:
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    speech_output = "Okay." \
                    " Please tell me how long you would like to focus."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me how long you would like to focus, " \
                    " You can say, help me focus for thirty minutes."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        None, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        None, speech_output, None, should_end_session))


def create_duration_timer_attributes(duration_timer):
    return {"durationTimer": duration_timer}
    




def timer_session(intent, session):
    if 'duration' in intent['slots']:
        #Creating the duration_timer in ISO 6801 format
        duration_timer = intent['slots']['duration']['value']
        session_attributes = create_duration_timer_attributes(duration_timer)
    
        speech_output = "You have set your focus timer for " + duration_timer + \
        ". Say start focus timer to begin."
        
    should_end_session = False    
    return build_response(session_attributes, build_speechlet_response(
        "Set Timer", speech_output, None, should_end_session))
     
     
     
        
def begin_timer(intent, session):
    
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if session.get('attributes', {}) and "durationTimer" in session.get('attributes', {}):
        duration_timer = session['attributes']['durationTimer']
        
    t = str(duration_timer)
    #t = "PT30S"
    index = -1
    # hold values for time amount
    total = 0
    # get start and end of int
    time_dict = {"H" : 3600, "M" : 60, "S" : 1}
    for i in range(len(t)):
        try:
            int(t[i])
            if index == -1:
                index = i
                continue    
        except:
            if index != -1:
                total += int(t[index:i]) * time_dict[t[i]]
                index = -1
    
    now = 0
    future = now + total
    while now < future:
        now = now + 1
        time.sleep(1)
    
    speech_output = "Time's up! Good job at staying focused."
    session_attributes = {}
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        None, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MyColorIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyColorIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "FocusDurationIntent":
        return timer_session(intent, session)
    elif intent_name == "BeginTimerIntent":
        return begin_timer(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])