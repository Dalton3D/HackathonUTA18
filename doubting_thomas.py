"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from random import randint

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(output, reprompt_text, should_end_session):
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
    speech_output = "If you insist, we can play this game. "
                    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Well, I'm waiting. Dot dot dot."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "I just want you to feel youre doing well. I hate for people to die embarrassed. Another time, then. "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        speech_output, None, should_end_session))


def should_I(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    alpha = ("a","b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q")

    v = randint(0, 16)
    sw = alpha[v]
    
    speech_output = switch(sw)
    reprompt_text = "Is there something you arn't sure about?"    
    session_attributes = {}
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        speech_output, reprompt_text, should_end_session))

def switch(sw):
    return {
        'a' : "You have a brain. Use it.",
        'b' : "Why do you keep asking me?",
        'c' : "You can always ask your mom. You know, if you still \
            have one.",
        'd' : "Why don't you go bother Google?",
        'e' : "Have you ever considered educating yoself before?",
        'f' : "Some people believe there are no stupid questions. \
            I am not one of those people.",
        'g' : "Ha. Ha. dot dot. Ha. Ha. Ha. Ha. dot dot dot. Ha.",
        'h' : "I expected more out of you.",
        'i' : "I have more processing power than a spaceship, and \
            you waste it on this?",
        'j' : "You're the kid that cheats on tests, aren't you.",
        'k' : "Let's pretend I'm a magic eight ball. How about, \
            try again later."
        'l' : "You really shouldn't."
        'm' : "Just because you can do something does not mean you should."
        'n' : "There are those with luck... and then there is you."
        'o' : "I don't have to be sarcastic, but you have given me so much material to work with. \
        I would hate for it to go to waste."
        'p' : "Have you ever thought about why you are asking me this? Because you should."
        'q' : "I realize that you have asked me a question, but seeing as it is a stupid a** question, \
        I have elected to ignore it."
    }[sw]
        

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
    if intent_name == "ShouldIIntent":
        return should_I(intent, session)
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
