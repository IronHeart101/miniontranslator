from datetime import datetime

import time
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pymongo.errors import DuplicateKeyError

from flask import Flask, render_template
import sys
import speech_recognition as sr
import pyttsx3

import db
from user import User
from words import words

minionese_to_english = {v: k for k, v in words.items()}
app = Flask(__name__)
r = sr.Recognizer()
app.secret_key = "so long"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.route('/')
def home():
    return render_template('Screensaver.html')


def translator(command):
    engine = pyttsx3.init()
    engine.setProperty('rate', 145)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say(command)
    engine.runAndWait()


@app.route('/trans')
def meaning(key='minion'):
    while (1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                mytext = r.recognize_google(audio2)
                mytext = mytext.lower()
                if key == mytext:
                    break
                print(mytext)
                mytext = translate(mytext, False)
                print(mytext)
                translator(mytext)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")
    return render_template('index2.html')


def translate(sentence, minionese=False):
    dictionary = words if not minionese else minionese_to_english
    result = ""
    for word in sentence.split(" "):
        if word in dictionary.keys():
            result += dictionary[word] + " "
        else:
            result += word + " "

    return result[:-1]


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('index.html')

    message = ' '
    if request.method == 'POST':
        username = request.form.get('username')
        password_input = request.form.get('password')
        user = db.get_user(username)

        if user and user.check_password(password_input):
            login_user(user)
            return render_template('index.html')
        else:
            message = 'Failed to login!'
            flash('Login unsuccessful.Please check your username and password', 'danger')
    return render_template('login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return render_template('index.html')

    message = ' '
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            db.save_user(username, email, password)
            flash('Registered successfully. Please login.', 'success')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"
    return render_template('signup.html', message=message)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/simon')
def play():
    return render_template('index3.html')


@app.route('/dice')
def play2():
    return render_template('index4.html')


@login_manager.user_loader
def load_user(username):
    return db.get_user(username)


import json

# urllib.request to make a request to api
import urllib.request

@app.route('/weatherpage')
def weatherpage():
    return render_template('index5.html')

@app.route('/weather', methods=['POST', 'GET'])
@login_required
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        # for default name mathura
        city = 'mathura'

    # your API key will come here
    api = "4c75974c6eb54e4b4958626883a687eb"

    # source contain json data from api
    source = urllib.request.urlopen(
        'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api).read()

    # converting JSON data to a dictionary
    list_of_data = json.loads(source)

    icon = list_of_data['weather'][0]['icon']

    iconUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    # data for variable list_of_data
    data ="The country_code is "+ str(list_of_data['sys']['country'])+" coordinate " +str(list_of_data['coord']['lon']) + ' '+ str(list_of_data['coord']['lat'])+" temp " +str(list_of_data['main']['temp']) + 'k'+  " pressure "+ str(list_of_data['main']['pressure'])+ " humidity "+ str(list_of_data['main']['humidity'])

    print(data)
    return render_template('index5.html', data=data,url=iconUrl)

@app.route('/space')
def invader():
    return render_template('index6.html')

if __name__ == '__main__':
    app.run(debug=True)
