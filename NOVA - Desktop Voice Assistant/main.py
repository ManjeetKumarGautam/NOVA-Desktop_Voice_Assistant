from GUI import Ui_JarvisUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import speech_recognition as sr
import pyttsx3
import datetime
import json
import os
import openai
from dotenv import load_dotenv
import smtplib
import psutil
import pyautogui
import time
import subprocess
import winshell
import pyjokes
import pywhatkit

engine=pyttsx3.init("sapi5")
voices=engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate',170)
def speak(msg):
    print(f"Nova : {msg}")
    engine.say(text=msg)
    engine.runAndWait()

fileopen=open("data\\api.txt","r")
API=fileopen.read()
fileopen.close()

class MainThread(QThread):

    def __init__(self):
        super().__init__()

    def run(self):
        self.Main()
        
    def Main(self):
        self.GUI=StartGUI()
        self.GUI.greet()
        
        while True:
            
            self.query=self.GUI.Listen().lower()

            if 'open' in self.query:
                var=self.query.replace("open ","")
                self.GUI.outputMsg("Nova : ok sir, i am openning "+var)
                speak("ok sir, i am openning "+var)
                self.GUI.openApp(var)

            elif 'close' in self.query:
                var=self.query.replace("close ","")
                self.GUI.outputMsg("Nova : okay sir")
                speak("okay sir")
                self.GUI.closeApp(var)
            
            elif 'bye' in self.query:
                self.GUI.outputMsg
                speak("bye sir")
                exit()

            elif 'joke' in self.query:
                speak(pyjokes.get_joke())

            elif "write a note" in self.query:
                self.GUI.outputMsg("Nova : What should i write, sir")
                speak("What should i write, sir")
                note = self.GUI.Listen()
                file = open('nova.txt', 'w')
                self.GUI.appendMsg("Sir, Should i include date and time")
                speak("Sir, Should i include date and time")
                snfm = self.GUI.Listen()
                if 'yes' in snfm or 'sure' in snfm:
                    strTime = datetime.datetime.now().strftime("% H:% M:% S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                else:
                    file.write(note)
         
            elif "show note" in self.query:
                self.GUI.outputMsg("Showing Notes")
                speak("Showing Notes")
                file = open("nova.txt", "r")
                print(file.read())
                speak(file.read(6))

            elif 'search file in pc' in self.query:

                self.GUI.outputMsg("Nova : which file? tell me file name")
                speak("which file? tell me file name")
                # self.fileName=input("File Name :")
                self.fileName=self.GUI.Listen().lower()
                self.GUI.appendMsg("Nova : ok and which directory i will search.")
                speak("ok")
                speak("and which directory i will search. Please enter ")
                # self.filePath=input("Directory : ")
                self.filePath=self.GUI.Listen().upper()
                self.GUI.appendMsg("Now i am searching a file. please wait.")
                speak("Now i am searching a file. please wait.")
                self.file=self.GUI.find_files(self.fileName, self.filePath)

                self.GUI.appendMsg("Nova : I searched it. you want to open this file")
                speak("I searched it. you want to open this file")
                self.openFile=self.GUI.Listen().lower()
                if 'yes' in self.openFile:
                    os.startfile(self.file)

            elif 'send a WhatsApp message' in self.query:
                pywhatkit.sendwhatmsg("+919506032564","Geeks For Geeks!",18, 30)
                
            elif 'play music' in self.query:
                music_dir = "C:\\Users\\MANJEET\\Music\\"
                song = os.start(os.listdir(music_dir[0]))

            elif 'shutdown system' in self.query: 
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f') 
                    
            elif 'clean recycle bin' in self.query: 
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True) 
                speak("Recycle Bin Cleaned , Sir") 
    
            elif "restart" in self.query: 
                subprocess.call(["shutdown", "/r"]) 
                
            elif "hibernate" in self.query or "sleep" in self.query: 
                speak("Hibernating") 
                subprocess.call("shutdown / h") 
    
            elif "log off" in self.query or "sign out" in self.query: 
                speak("Make sure all the application are closed before sign-out") 
                time.sleep(10) 
                subprocess.call(["shutdown", "/l"]) 

            elif "don't listen" in self.query or "stop listening" in self.query:
                self.GUI.outputMsg("Nova : ok sir. Now i am not listening for 20 second")
                speak("ok sir. Now i am not listening for 20 second") 
                time.sleep(20)  

            elif 'send mail' in self.query:
                    gmail_sender = 'kumar2020manjeet@gmail.com'
                    gmail_passwd = 'uzxfsjqhaqztkxqv'
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(gmail_sender, gmail_passwd)
                    server.sendmail(gmail_sender, 'manjeetkumar1572000@gmail.com', 'Subject: hehehe\n\n heloo ji kaise ho')
                    server.close()
                    print("done")

            
            else:
                self.GUI.ReplyBrain(self.query)

startExe = MainThread()

class StartGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.UI=Ui_JarvisUI()
        self.UI.setupUi(self)
        openai.api_key=API
        load_dotenv()
        self.completion=openai.Completion()

        self.UI.startButton.clicked.connect(self.startTask)
        self.UI.stopButton.clicked.connect(self.close)

    def startTask(self):
        self.UI.mainGif=QtGui.QMovie("images//GIF.gif")
        self.UI.mainLabel.setMovie(self.UI.mainGif)
        self.UI.mainGif.start()
        self.showCurrentDate()
        self.features()
        timer=QTimer(self)
        timer.timeout.connect(self.showCurrentTime)
        # timer.timeout.connect(self.features) 
        timer.timeout.connect(self.updateOutput)
        timer.start()
        startExe.start()
        self.showCPU()

    def outputMsg(self,msg):
        self.f=open("data//query.txt",'w')
        self.f.write(msg)
        self.f.close()

    def updateOutput(self):
        self.f=open("data//query.txt",'r')
        self.text=self.f.read()
        self.f.close()
        self.UI.textEdit.setPlainText(self.text)

    def appendMsg(self,msg):
        self.f=open("data//query.txt",'a')
        self.f.write("\n\n"+msg)
        self.f.close()

    def features(self):
        self.f=open("data//features.txt",'r')
        self.text=self.f.read()
        self.f.close()
        self.UI.plainTextEdit.setUpdatesEnabled(True)
        self.UI.plainTextEdit.setPlainText(self.text)
        self.UI.plainTextEdit.setReadOnly(True)

    def showCurrentDate(self):
        currdate=QDate.currentDate().toString()
        self.UI.dateLabel.setText(f"Date : {currdate}")

    def showCurrentTime(self):
        curr_time=QTime.currentTime()
        time=curr_time.toString('hh:mm:ss')
        self.UI.timeLabel.setText(f"Time : {time}")

    def showCPU(self):
        self.per=str(psutil.cpu_percent())
        self.UI.label_3.setText(self.per+"%")
        self.ram=str(psutil.virtual_memory()[2])
        self.UI.label_5.setText(self.ram+"%")
    
    def speak(self,msg):
        print(f"Sara : {msg}")
        self.UI.textEdit.setText((f"Sara : {msg}"))
        engine.say(text=msg)
        engine.runAndWait()

    def greet(self):
        self.hour = int(datetime.datetime.now().hour)
        if self.hour>=0 and self.hour<12 :
            self.outputMsg("Nova : Good Morning")
            speak("Good morning")

        elif self.hour>=12 and self.hour<=16 :
            self.outputMsg("Nova : Good Morning")
            speak("Good Afternoon")

        else:
            self.outputMsg("Nova : Good Evening")
            speak("Good Evening")

        self.appendMsg("Nova : How may I help you")
        speak("How may I help you")
        
    

    def Listen(self):
        self.showCPU()
        self.r=sr.Recognizer()
        with sr.Microphone() as source: 
            print("Listening...")
            self.r.pause_threshold=1
            self.audio=self.r.listen(source,0,5)

        try:
            print("Recognizing...")
            self.query=self.r.recognize_google(self.audio,language='en-in')
            print(f"User : {self.query}")
        
        except Exception as e:
            print("Say that again please.....")
            return "None"
     
        return self.query

    def writeSomething(self):
        flag = 1
        while flag==1:
            self.appendMsg("Nova : Sir! do you want to write something ")
            speak("Sir! do you want to write something ")
            text = self.Listen()
            if 'yes' in text:
                self.appendMsg("Nova : What do I write sir")
                speak("What do I write sir")
                
                w = self.Listen()
                pyautogui.typewrite(w+" ")
                self.appendMsg("Nova : I've write of that")
                speak("I've write of that")
            elif 'no' in text:
                self.appendMsg("ok Sir")
                speak("Nova : ok Sir")
                flag = 0
    
    def ReplyBrain(self,question,chat_log=None):
        if (question!='none'):
            self.FileLog = open("data\\neurons.txt","r")
            self.chat_log_tamplate=self.FileLog.read()
            self.FileLog.close()
            if chat_log is None:
                self.chat_log=self.chat_log_tamplate

            self.prompt = f'{chat_log}You : {question}\nNova : '
            self.response = self.completion.create(
                model="text-davinci-003",
                prompt=self.prompt,
                temperature = 0.5,
                max_tokens = 100,
                top_p = 0.3,
                frequency_penalty= 0.5,
                presence_penalty = 0
            )
            self.answer = self.response.choices[0].text.strip()
            self.chat_log_tamplate_update = self.chat_log_tamplate + f"You : {question} \nNova : {self.answer}\n"
            self.FileLog = open("data\\neurons.txt","w")
            self.FileLog.write(self.chat_log_tamplate_update)
            self.FileLog.close()
            self.outputMsg(f"You : {question} \nNova : {self.answer}\n")
            speak(self.answer)

    def showSong(self):
        music_dir = "C:\\Users\\MANJEET\\Music\\"
        song = os.listdir(music_dir)
        f=open("data//mySongs.txt",'w')
        f.write(*song)
        f.close()
        f1=open ("data//mySongs.txt",'r')
        songs = f1.read()
        self.UI.plainTextEdit.setPlainText(songs)

    def song(self):
        speak("which song I play ,Sir")
        m = self.Listen().lower()
        speak("ok sir! i am playing"+ m +"music")
        music_dir = "C:\\Users\\MANJEET\\Music\\"
        os.startfile(music_dir+m+".mp3")
        time.sleep(60)

    def openApp(self,var):
        self.f = open('data\\OpenClosePaths.json')
        self.data = json.load(self.f)
        if var in self.data['open']:
            self.d=self.data['open'][var]
            os.startfile(self.d)
        self.f.close()
        self.writeSomething()

    def closeApp(self,var):
        self.f = open('data\\OpenClosePaths.json')
        self.data = json.load(self.f)
        if var in self.data['close']:
            self.d=self.data['close'][var]
            os.system(self.d)
        self.f.close()
       

    def find_files(self,filename, search_path):
        self.res = ""
        for root, dir, files in os.walk(search_path):
            if filename in files:
                self.res = self.res + os.path.join(root,filename)
        return self.res


GUI_App=QApplication(sys.argv)
jarvis_gui= StartGUI()
jarvis_gui.show()

exit(GUI_App.exec_())