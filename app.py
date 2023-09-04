#!pip install gradio
#!pip install ibm-watson

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, EntitiesOptions, KeywordsOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


api_key = 'lAeHLWD1plIe_CgKsEeAHoLOQwz7KMNIet-RxrJWaVF_'
service_url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/1483f893-9885-4ad7-9a42-f5bbf7ef5964'
version = '2021-08-01' 

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
    #nlu = NaturalLanguageUnderstandingV1('https://api.us-south.natural-language-understanding.ibmcloud.com', api_key='PZ8sVI4DUjfwikksw96KvyUd7GJRFBLMNqFPTVvQAP7x')
    nluVar = nlu

    # Analyze the input text to identify the user's intent
    #1 response = nlu.analyze(text=input_text, features=Features(emotion=EmotionOptions(targets=["happy"]))).get_result()
    #2 response = nluVar.analyze(text=input_text, features={'sentiment': {}, 'entities': {}}).get_result()
    ''' response = nlu.analyze(
              text=input_text,
              features=Features(emotion=EmotionOptions(targets=["happy"]))).get_result() 
    '''
    

    response = nluVar.analyze(text=input_text, features=Features(entities=EntitiesOptions(),sentiment=SentimentOptions(),keywords=KeywordsOptions())).get_result()
    '''
    # Extract relevant information from the response
    entities = response.result['entities']
    keywords = response.result['keywords']

    # Print the detected entities and keywords
    print("Entities:")
    for entity in entities:
      print(f"{entity['type']} : {entity['text']}")

    print("\nKeywords:")
    for keyword in keywords:
      print(keyword['text'])
    '''

    
    sentimentOutput = response["sentiment"]
    documentOutput = sentimentOutput["document"]
    labelOutput = documentOutput["label"]
    finalAns = "You show signs of " + str.upper(labelOutput) + " mental health"

    # Print the formatted JSON
    formatted_response = json.dumps(response, indent=4)
    #a = print(formatted_response)
    print(formatted_response)
    return(finalAns)
    

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
    # buttons=["Seeking Support", "Feeling Overwhelmed"],
    # button_styles={"background-color": ["#4CAF50", "#F8E231"]}
)

interface.launch()