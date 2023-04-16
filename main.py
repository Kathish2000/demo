import os
import time
import webbrowser
import wikipedia
import datetime
import threading
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Bundle = autoclass('android.os.Bundle')
NotificationManager = autoclass('android.app.NotificationManager')
Context = autoclass('android.content.Context')

def send_notification(message):
    notif = autoclass('android.app.Notification')()
    notif.icon = 'icon.png'
    notif.tickerText = 'Notification'
    notif.flags |= NotificationManager.FLAG_AUTO_CANCEL
    context = PythonActivity.mActivity.getApplicationContext()
    notif.setLatestEventInfo(context, 'Notification', message, None)
    autoclass('android.app.NotificationManager') \
        .mNotificationManager.notify(0, notif)

def speak(message):
    tts = TextToSpeech(PythonActivity.mActivity, None)
    tts.speak(message, TextToSpeech.QUEUE_FLUSH, Bundle.EMPTY, 'tts1')
    while tts.isSpeaking():
        time.sleep(0.1)
    tts.shutdown()

def get_time_greeting():
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        return 'Good morning!'
    elif current_time.hour < 18:
        return 'Good afternoon!'
    else:
        return 'Good evening!'

def main():
    while True:
        command = input('Speak: ').lower()
        if 'open' in command:
            url = command.replace('open', '').strip()
            webbrowser.open(url)
            speak(f"Opening {url}")
        elif 'search' in command:
            query = command.replace('search', '').strip()
            url = f'https://www.google.com/search?q={query}'
            webbrowser.open(url)
            speak(f"Here are the search results for {query}")
        elif 'wikipedia' in command:
            query = command.replace('wikipedia', '').strip()
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        elif 'time' in command:
            speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")
        elif 'date' in command:
            speak(f"Today is {datetime.date.today().strftime('%B %d, %Y')}")
        elif 'greeting' in command:
            speak(get_time_greeting())
        elif 'call me' in command:
            name = command.replace('call me', '').strip()
            send_notification(f"You want me to call you {name}!")
            speak(f"Sure, I'll call you {name} from now on!")
        elif 'message' in command:
            message = command.replace('message', '').strip()
            send_notification(f"You want me to remember the message: {message}!")
            speak(f"Okay, I'll remember that for you!")
        elif 'exit' in command or 'close' in command:
            os._exit(0)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        label = MDLabel(text='Click the button to start the voice recognition',
                        halign='center', font_style='H5')
        button = MDFlatButton(text='Start', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button.bind(on_press=self.start_listening)
        layout.add_widget(label)
        layout.add_widget(button)
        return layout

    def start_listening(self, instance):
        thread = threading.Thread(target=main)
        thread.daemon = True
        thread.start()
