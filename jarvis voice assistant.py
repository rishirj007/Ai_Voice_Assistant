import pyttsx3 as pstt
import pyautogui
import speech_recognition as sr
import datetime
import time
import os
import cv2
import random
import requests
from requests import get
import pywhatkit as pwk
import pyjokes
import webbrowser
import wikipedia
import smtplib
import sys
import pyowm

jarvis_engine = pstt.init('sapi5')    #setting up text to speech and voices using python text to speech
voices = jarvis_engine.getProperty('voices')
jarvis_engine.setProperty('voices',voices[0].id)    #taking male iddavid

#jarvis text to speech
def speak(voice):
    jarvis_engine.say(voice)
    print(voice)
    jarvis_engine.runAndWait()

#func. for voice to text
def take_command(ask=False):
    listener = sr.Recognizer()

    with sr.Microphone() as source:    # using microphone as source to listen
        print('listening...')
        #listener.pause_threshold = 1
        #listener.energy_threshold = 200
        if ask:
            speak(ask)

        voice = listener.listen(source)  # calling sr to listen to source

        command = ''
        try:
            print('Recognizing...')
            # recognizing and converting speech to text using google api
            command = listener.recognize_google(voice,language='en-in')
            print(f'user said: {command}')

        except Exception as e:
            speak('Say that again please')
            return "None"

        return command

#wishes user
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak('Good Morning!')

    elif hour>=12 and hour<18:
        speak('Good Afternoon!')

    else:
        speak('Good Evening!')

    speak('I am Jarvis Sir Please Tell Me How May I Help You?')

#using smtp module to send email from gmail
def send_email(to,content):
    server = smtplib.SMTP('smtp.gmail.com',port = 587)
    server.ehlo()
    server.starttls()    #to start server
    server.login('useremail@email.com','your password')
    server.sendmail('useremail@email.com',to,content)
    server.close()


#command giving till user says no
if __name__ == "__main__":
    wish_me()
    while True:

        command = take_command().lower()

        #logic buiding for tasks
        if 'hello jarvis' in command:
            speak('Hey there ,Tell me what i can do for you?')

        elif 'what is your name' in command:
            speak('My Name Is Jarvis')

        elif 'how are you' in command:
            speak("I'm very well, thanks for asking ")

        elif 'time' in command:  # 1
            time = datetime.datetime.now().strftime('%I %M %p')
            print(time)
            speak('current time is ' + time)

        elif 'date' in command:  # 2
            today = datetime.date.today().strftime('%B %d %Y')
            print(today)
            speak("today is " + today)

        elif 'news' in command:
            webbrowser.open("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")

        elif 'search' in command:  # 3
            search = take_command('what do you want to search for?')
            search_url = 'https://google.com/search?q=' + search         # searching in the google using web browser
            webbrowser.get().open(search_url)
            speak('Here is what i found for ' + search)

        elif 'open instagram' in command:
            webbrowser.open("https://www.instagram.com/")

        elif 'open youtube' in command:  # 4
            webbrowser.open("youtube.com")

        elif 'open facebook' in command:  # 5
            webbrowser.open("facebook.com")

        elif 'open google' in command:  # 6
            speak('what should i search on google?')
            cmnd = take_command().lower()
            webbrowser.open(f"{cmnd}")

        elif 'open stack overflow' in command:  # 7
            webbrowser.open("https://stackoverflow.com/")

        elif 'find my current location' in command or 'where am i' in command:     #8
            speak('Wait sir,let me check')
            try:
                ip = requests.get('https://api.ipify.org').text
                #print(ip)
                url = 'https://get.geojs.io/v1/ip/geo/'+ip+'.json'
                geo_requests =  requests.get(url)
                geo_data = geo_requests.json()
                #print(geo_data)

                city = geo_data['city']
                region = geo_data['region']
                country = geo_data['country']
                speak(f'Sir I am Not Sure,but i think we are in {city} in {region} in {country}')

            except Exception as e:
                speak('sorry sir due to network issue not able to fetch your location')
                pass

        elif 'find location' in command:  # 8
            location = take_command('what is the location?')
            search_url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(search_url)
            speak('Here is the location of' + location)


        elif 'take a screenshot' in command or 'take screenshot' in command:
            speak("Please tell me the filename")
            filename = take_command().lower()
            speak('please hold am taking screenshot')
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{filename}.png")
            speak("It's Done Sir, Screenshot is saved in our main folder")

        elif 'wikipedia' in command:  # 9
            speak('searching wikipedia...')
            extract_info = command.replace('tell me about', '')
            result = wikipedia.summary(extract_info, sentences=1)
            #print(result)
            speak('According To Wikipdeia' + result)

        elif 'open notepad' in command:       #10
            n_path = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(n_path)

        elif 'close notepad' in command:
            speak('okay sir,closing notepad')
            os.system("taskkill /f /im notepad.exe")


        elif 'open adobe reader' in command:    #11
            code_path = "C:\Program Files (x86)\Adobe\Reader 8.0\Reader\\AcroRd32.exe"
            os.startfile(code_path)

        elif 'open command prompt' in command:   #12
            os.system('start cmd')

        elif 'send a whatsapp message' in command:        #13
            speak("Please provide number of reciever")
            contact = (input("Enter Number:"))
            speak('what should i say?')
            message = take_command().lower()
            speak("enter time when you want to send message?")
            hour = int(input("Hour:"))
            minutes = int(input("MIN:"))
            pwk.sendwhatmsg("+91"+contact,message,hour,minutes)

        elif 'open camera' in command:      #14
            capture = cv2.VideoCapture(0)
            while True:
                ret,img = capture.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)       #waitKey waits for a key event infinitely or for delay milliseconds, when it is positive.
                if k==27:
                    break;
            capture.release()          #Closes video file or capturing device.
            cv2.destroyAllWindows()    #Destroys all of the HighGUI windows.

        elif 'play music' in command:   #15
            music_dir = 'D:\\Songs'
            songs = os.listdir(music_dir)
            print(songs)
            random_song = random.choice(songs)
            #if mp3 song use endswith(.mp3)
            os.startfile(os.path.join(music_dir,random_song))

        elif 'ip address' in command:     #16
            ip = get('https://api.ipify.org').text
            speak(f'Your IP Address is {ip}')

        elif 'joke' in command:  # 18
            speak(pyjokes.get_joke())

        elif 'send email to name' in command:  # 19
            try:
                speak('what should i write?')
                content = take_command()
                to = "useremail@email.com"
                send_email(to, content)
                speak('Email has been sent')

            except Exception as e:
                print(e)
                speak('Sorry Not able to send this email!')

        elif 'are you single' in command:
            speak('I Am in relation with your wifi!')

        elif 'shut down the system' in command:
            os.system("shutdown /s /t 5")

        elif 'restart the system' in command:
            os.system("shutdown /r /t 5")

        elif 'make system sleep' in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'no thanks' in command:
            speak('Thanks for using me sir,Have a good day!')
            sys.exit()

        speak('Anything else sir that i can do for you?')



