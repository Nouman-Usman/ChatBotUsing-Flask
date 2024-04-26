import subprocess
import os
import speech_recognition as sr
from flask import logging, Flask, render_template, request, flash
import google.generativeai as palm
import re

app = Flask(__name__)
app.secret_key = "Nouman"
API_KEY = 'AIzaSyDzj8yESjjCS6vWNIFAAnjaKVtjGTNsl8g'
palm.configure(api_key=API_KEY)


@app.route('/')
def index():
    # flash(" Welcome to AssistBot site")
    return render_template('index.html')


@app.route('/video_play/')
def video_play():
    # flash("Press Tab to Start Video")
    return render_template('videoFile.html')


@app.route('/audio_to_text/')
def audio_to_text():
    # flash(" Press Start to start recording audio and press Stop to end recording audio")
    return render_template('audio_to_text.html')


@app.route('/audio', methods=['POST'])
def audio():
    first_transcript = ""
    model_id = "models/text-bison-001"
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)

    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='en-IN', show_all=True)
        print(text)
        first_transcript = ""
        first_transcript = text.get('alternative', [])[0].get('transcript', '') if text.get('alternative') else ''

        prompt = first_transcript
        completion = palm.generate_text(
            model=model_id,
            prompt=prompt,
            temperature=0.99,
            max_output_tokens=800
        )
        completion.result = re.sub(r'\b\d+\.\b', '\n', completion.result)
        print(completion.result)
        try:
            for num, texts in enumerate(text['alternative']):
                return_text += str(num+1) +") " + texts['transcript']  + " <br> "
        except:
            return_text = " Sorry!!!! Voice not Detected "
        os.remove('upload/audio.wav')
        completion.result = completion.result.replace("*", "")
        completion.result = completion.result.replace("", "")
        # subprocess.call(['say', completion.result])
    return str(completion.result)



