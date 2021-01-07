import os
import pickle
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<17:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")  
    speak("How may I help you.") 

def voiceinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")   

    except Exception as e:
        print(e)
        speak('I did not quiet get that. Please Say that Again')                    
        print("Say that again please...")
        return "None"
    return query

class SearchEngine:
    ''' Create a search engine object '''

    def __init__(self):
        self.file_index = [] # directory listing returned by os.walk()
        self.results = [] # search results returned from search method
        self.matches = 0 # count of records matched
        self.records = 0 # count of records searched


    def create_new_index(self, root_path):
        ''' Create a new file index of the root; then save to self.file_index and to pickle file '''
        
        self.file_index = [(root, files) for root, dirs, files in os.walk(root_path) if files]

        # save index to file
        with open('file_index.pkl','wb') as f:
            pickle.dump(self.file_index, f)


    def load_existing_index(self):
        ''' Load an existing file index into the program '''
        try:
            with open('file_index.pkl','rb') as f:
                self.file_index = pickle.load(f)
        except:
            self.file_index = []


    def search(self, term, search_type = 'contains'):
        ''' Search for the term based on the type in the index; the types of search
            include: contains, startswith, endswith; save the results to file '''
        self.results.clear()
        self.matches = 0
        self.records = 0
        

        # search for matches and count results
        for path, files in self.file_index:
            for file in files:
                self.records +=1
                if (search_type == 'contains' and term.lower() in file.lower() or 
                    search_type == 'startswith' and file.lower().startswith(term.lower()) or 
                    search_type == 'endswith' and file.lower().endswith(term.lower())):

                    result = path.replace('\\','/') + '/' + file
                    self.results.append(result)
                    self.matches +=1
                else:
                    continue 
        
        # save results to file
        with open('search_results.txt','w') as f:
            for row in self.results:
                f.write(row + '\n')

def test1():
    query =  voiceinput().lower()
    print(query)
    s = SearchEngine()
    s.create_new_index('C:\\New folder\\aabbccddee')
    s.search(query)
    for match in s.results:
        print(match)
        speak(match)
        os.startfile(os.path.join(match, aabbccddee[0]))

      

if __name__ == "__main__":
    greetings()
    while True:
        query = voiceinput().lower()

        if  'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia","")
            print(query)
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Its {strTime}")   
        
        elif 'news' in query:
            speak("Top stories on Google News")
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            a = 0
            # Print news title and publish date
            for news in news_list:
                print(news.title.text)
                print(news.pubDate.text)
                print("-"*60)
                speak(news.title.text)
                a = a+1
                if a>4:
                    speak("do you want me to continue?")
                    query = voiceinput().lower()
                    if 'no' in query:
                        break

        elif 'help' in query:
            speak("I can help you get information through wikipedia, news, tell the time, open webpages and play music and I am currently in process of preparing to help you with more stuf!")


        elif 'play music' in query:
            speak('Please tell which song you want me to play or should I shuffle them.')
            test1()
            
        elif "kill the process" in query:
            break
        elif "open webpage" in query:
            query = query.replace("open webpage ","")
            print(query)
            webbrowser.open(query)

        elif '.com' or '.in' or '.co' or '.biz' in query:
            if 'open' in query:
                query = query.replace("open ","")
            print(query)
            webbrowser.open(query)
                
