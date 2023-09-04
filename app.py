import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


api_key = 'API_KEY'
service_url = 'URL'
version = 'DATE' 

# Initialize the IAM authenticator
authenticator = IAMAuthenticator(api_key)

# Initialize the NLU service with the authenticator
nlu = NaturalLanguageUnderstandingV1(
    version=version,
    authenticator=authenticator
)

# Set the service URL (this is the correct way to set the URL)
nlu.set_service_url(service_url)


import gradio as gr

def chatbot(input_text):
    # Initialize the Natural Language Understanding API
    nluVar = nlu

    # Analyze the input text to identify the user's intent
    response = nluVar.analyze(text=input_text, features=Features(entities=EntitiesOptions(),sentiment=SentimentOptions(),keywords=KeywordsOptions())).get_result()
       
    sentimentOutput = response["sentiment"]
    documentOutput = sentimentOutput["document"]
    labelOutput = documentOutput["label"]
    finalAns = "You show signs of " + str.upper(labelOutput) + " mental health"

    # Print the formatted JSON
    formatted_response = json.dumps(response, indent=4)
    #a = print(formatted_response)
    print(formatted_response)
    return(finalAns)   # output of this chatbot function

    # I DID NOT EXECUTE THE FOLLOWING INTENT CODE AS THE ABOVE FUNCTION COULD NOT FIND ENTITIES FOR EACH PROMPT/INPUT
    intent = response['entities'][0]['entity']
    # Determine the appropriate response based on the user's intent
    if intent == 'SeekingSupport':
        return "I'm here to listen and offer support. Would you like to talk about what's been going on?"
    elif intent == 'FeelingOverwhelmed':
        return "It sounds like you're feeling really overwhelmed right now. Have you considered reaching out to a therapist or counselor for help?"
    else:
        return "I didn't understand your message. Can you please rephrase or provide more context?"

#input_text = input()
#chatbot(input_text)

# Define the interface
interface = gr.Interface(
    fn=chatbot,
    inputs="text", 
    outputs="text",
    title="Mental Health Chatbot",
    description="A chatbot designed to provide support and resources for people struggling with mental health issues. It tells if you are showing Positive or Negative mental health signs",
)

interface.launch()
