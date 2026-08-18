# context.py
#-----------------------------------------------------------------------------------
from langchain_openai import ChatOpenAI as Chat                                     # importiert chat-klasse
from dotenv import load_dotenv                                                      # lädt .env dateien
import os                                                                           # zugriff auf os funktionen
#-----------------------------------------------------------------------------------
E = Exception                                                                       # kürzel für exception class erstellen
load_dotenv()                                                                       # lädt environment variablen aus .env
#-----------------------------------------------------------------------------------
TESTMODE = True                                                                     # modus
TESTMAIL = os.getenv("TESTER_ADDRESS").lower()                                      # email addresse des test versenders aus env
#-----------------------------------------------------------------------------------
USER, PW = os.getenv("GMAIL_ADDRESS").lower(), os.getenv("GMAIL_APP_PASSWORD")      # benutzer-email und app-passwort aus env
#-----------------------------------------------------------------------------------
cats = ["sales", "marketing", "general", "support", "privacy", "invoice", "spam"]   # kategorie-liste (beispiele)
CATS = ["sales"]                                                                    # aktive kategorien zu denen reply prompt existiert
#-----------------------------------------------------------------------------------
classify = Chat(model="gpt-5.6-terra")                                              # chat-instanz für klassifikation (smaller model)
response = Chat(model="gpt-5.6-sol")                                                # chat-instanz für antworten (flagship model)
#-----------------------------------------------------------------------------------
# Für ältere Modelle Temperature nutzen, z.B:
#-----------------------------------------------------------------------------------
# classify = Chat(model="gpt-5-mini", temperature=0)                                # chat-instanz für klassifikation (smaller model)
# response = Chat(model="gpt-5", temperature=0.3)                                   # chat-instanz für antworten (flagship model)
#-----------------------------------------------------------------------------------