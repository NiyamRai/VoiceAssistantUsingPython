import datetime
import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
# import os
import webbrowser
import smtplib
from AppOpener import open, close

n=0

listener=sr.Recognizer()

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

engine.setProperty('rate',170)

#for openning an app
def opapp(inp):
         if "close " in inp:
             app_name = inp.replace("close ","").strip()
             speak("Closing"+app_name)
             close(app_name, match_closest=True, output=False) 

         if "open " in inp:
             app_name = inp.replace("open ","")
             speak('opening '+app_name)
             open(app_name, match_closest=True) 

# Speak out 
def speak(txt):
    engine.say(txt)
    engine.runAndWait()
#By niyam rai and team

def pause():
    global n
    n=0
    print('Paused')
    try:
        with sr.Microphone() as source:
            listener.energy_threshold=400
            voice=listener.listen(source)
            command=listener.recognize_google(voice)
            command=command.lower()
            if 'buddy' in command:
                speak('How may i help you sir')
                run_alexa()

    except Exception as e:
        pause()


def take_command():
    global n
    try:
        with sr.Microphone() as source:
            print('listening....')
            listener.energy_threshold=200
            voice=listener.listen(source)
            print('Recognizing...')
            command=listener.recognize_google(voice)
            command=command.lower()
            print(command)
        return command
           
    except Exception as e: 
        speak("Say that again please...")  
        
        n=n+1
        if n<3:
            return "None"
        else:#S2N2 group
            pause()

# send email 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('example@gmail.com', 'abcd')
    server.sendmail('netra@eastpoint.ac.in', to, content)
    server.close()

def greet():
    hour=int(datetime.datetime.now().hour)
    if hour<12 and hour>=0:
        speak("good morning ")
    elif hour==12:      #Niyam Rai and Team
        speak("good afternoon ")
    else:
        speak("good evening ")
    speak('how may i help you')


def run_alexa():
    command=take_command()
    
    if 'play' in command:
        song=command.replace('play','')
        speak('playing'+song)
        pywhatkit.playonyt(song)
        pause()
    
    elif "buddy" in command:
        greet()


    elif 'time' in command:
        time=datetime.datetime.now()
        time=time.strftime("%H:%M:%S") 
        speak('current time is'+time)
        pause()

    elif 'pause' in command or 'wait' in command or 'stop' in command:
        pause()

    elif ' wikipedia' in command:
        try:
            speak('Searching Wikipedia...')
            command = command.replace(" wikipedia", "")
            results = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except Exception as e:
            speak('Not available')
            pass
        pause()

    elif 'search' in command or "what is" in command:
        if 'search' in command :
            command=command.replace('search','')
        elif "what is" in command:
            command=command.replace('what is ','')
        results=pywhatkit.info(command, lines = 2,return_value=True)
        speak(results)
        pause()

    elif 'open ' in command or 'close' in command:
        opapp(command)
        pause()

    elif 'browse ' in command:
        chrmdir='C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\chrome.exe %s'
        chromedir= 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe %s'
        command=command.replace('browse ','')
        command=command.replace(' ','')
        durl='https://www.example.com/'
        speak('opening')
        url=durl.replace('example',command)
        webbrowser.open_new(url)
        pause()
    # Tell joke
    elif 'joke' in command:
        speak(pyjokes.get_joke())

         
    # Send email to someone
    elif "mail to netra ma'am" in command:
        try:
            speak("What should I send?")
            content = take_command()
            to = "example@gmail.com"    
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry sir, I am not able to send this email") 
        pause()

    elif 'team' in command:
        speak("This code is genetated by S2N2 Group ")
    elif 'creator' in command:
        speak("Niyam")            
    elif 'quit' in command or 'exit' in command or 'bye' in command:

        speak('Thank you maam have a good day ')
        exit()

while True:
    run_alexa()



