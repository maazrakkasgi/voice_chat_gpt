import openai
import requests

openai.api_key = "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"


def speech_to_text(audio_binary):
    base_url = "http://speech-to-text.17x15dhl20r7.svc.cluster.local"
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    # Set up parameters for our HTTP reqeust
    params = {
        'model': 'en-US_Multimedia',
    }
    # Set up the body of our HTTP request
    body = audio_binary
    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()
    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text
    return None


def text_to_speech(text, voice=""):
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    # Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    # Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }
    # Send a HTTP Post reqeust to Watson Text to Speech Service
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content
    return None


def openai_process_message(user_message):
    prompt = "\"Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations. " + user_message + "\""
    # Call the OpenAI Api to process our prompt
    openai_response = openai.Completion.create(model="text-davinci-003", prompt=prompt,max_tokens=4000)
    print("openai response:", openai_response)
    # Parse the response to get the response text for our prompt
    response_text = openai_response.choices[0].text
    return response_text
    
