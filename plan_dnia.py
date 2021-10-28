import speech_recognition as sr
import pyttsx3
import time
import csv
import datetime

engine = pyttsx3.init()
engine.setProperty('volume',1)
engine.setProperty('rate',150)
weekdays={0:'monday',1:'tuesday',2:'wednesday',
          3:'thursday',4:'friday',5:'saturday',6:'sunday'}
weekdays2={0:'poniedzialek',1:'wtorek',2:'środa',
          3:'czwartek',4:'piątek',5:'sobota',6:'niedziela'}
dane=[]
komunikaty=[]

def recognise(msg="Powiedz: okey"):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print(msg)
        audio = r.listen(source)
        try:
            recognized_text = r.recognize_google(audio, language="pl-PL")
            print("Powiedziałeś: " + recognized_text)
            return recognized_text.lower()
        except sr.UnknownValueError:
            print("Nie rozumiem")
            #engine.say("Nie rozumiem")
            #engine.runAndWait()
        except sr.RequestError as e:
            print("Error: ", e)
def load_data():
    global weekdays, dane, komunikaty
    try:
        day_num = datetime.datetime.today().weekday()
        with open('plan_dnia_' + str(day_num+1) + '_' + weekdays[day_num] +'.txt', newline='',encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar=None)
            dane=list(csv_reader)
    except Exception as e:
        print("Error: ", e)
        return False
    with open('settings.txt', encoding='utf-8') as settings:
        komunikaty = settings.read().split('\n')
        #print('settings.txt (komunikaty): ', komunikaty)
        if not (len(komunikaty)>1 and komunikaty[0] and komunikaty[1]):
            input('Plik settings.txt powinien zawierać 2 linijki')
            return False
    return True

while True:
    if not load_data():
        break
    app_start_time = time.strftime("%H:%M", time.localtime())
    print(weekdays2[datetime.datetime.today().weekday()] + ' ' + app_start_time)
    engine.say('jest ' + weekdays2[datetime.datetime.today().weekday()] + ', godzina ' + app_start_time + ', test dźwięku')
    engine.runAndWait()
    while dane[len(dane)-1][0] < time.strftime("%H:%M", time.localtime()):
        time.sleep(60)
    if not load_data():
        break
    app_start_time = time.strftime("%H:%M", time.localtime())
    print(weekdays2[datetime.datetime.today().weekday()] + ' ' + app_start_time)
    for row in dane:
        print(row)
        if row[0]<app_start_time:
            continue
        not_yet = True
        while not_yet:
            if row[0]<=time.strftime("%H:%M", time.localtime()):
                #text = ""
                #while text!="okej":
                engine.say(row[0] + ' ' + komunikaty[0] + ', ' + row[1])
                engine.runAndWait()
                #    text = recognise()
                #    if not text:
                #        continue
                not_yet = False
                #engine.say('spoko')
                #engine.runAndWait()
            else:
                time.sleep(30)


    engine.say(komunikaty[1])
    engine.runAndWait()
    time.sleep(120)


        
    
              
