# utils.py
#-----------------------------------------------------------------------------------
from json import load                                                               # lädt json aus datei
from re import findall                                                              # sucht alle muster im text mit regex
from context import TESTMODE, TESTMAIL, USER, PW                                    # branded email template und credentials
from email.message import EmailMessage                                              # email message klasse
from email import message_from_bytes as get_msg                                     # wandelt rohe mail-bytes in objekt
from email.header import make_header, decode_header                                 # dekodiert mime-header
from email.utils import parseaddr                                                   # nur address aus from/to extrahieren
from imaplib import IMAP4_SSL                                                       # imap ssl client (mails lesen)
from smtplib import SMTP_SSL                                                        # smtp ssl client (mails senden)
from jinja2 import Environment as Jinv, FileSystemLoader as FSL                     # importiert jinja2 template engine
#-----------------------------------------------------------------------------------
# BASIC HELPERS
#-----------------------------------------------------------------------------------

def read_file(p:str):                                                               # liest datei ein
    with open(p, "r", encoding="utf-8") as f:                                       # öffnet datei utf-8
        return load(f) if p.endswith(".json") else f.read()                         # json → dict sonst text

def fill(tmp:str, ph:dict):                                                         # ersetzt platzhalter im template
    for p in findall(r"__(.*?)__", tmp):                                            # findet alle __platzhalter__
        tmp = tmp.replace(f"__{p}__", str(ph.get(p) or ""))                         # ersetzt platzhalter mit wert oder leer
    return tmp                                                                      # gibt fertigen text zurück

def not_tester(sender:str):                                                         # checken ob echter absender in testmode
    if TESTMODE and sender.lower() != TESTMAIL.lower(): return True                 # wenn testmode und sender nicht tester

def is_noreply(sender:str):                                                         # checken ob noreply case
    nore = ["noreply", "no.reply", "no-reply", "no_reply"]                          # noreply cases
    return any(x in sender.lower() for x in [*nore, USER])                          # wenn user oder noreply case in sender address

#-----------------------------------------------------------------------------------
# MAIL READ HELPERS
#-----------------------------------------------------------------------------------

def imap_login(ms=None):                                                            # mailserver login um emails zu lesen
    if not isinstance(ms, IMAP4_SSL):                                               # wenn keine mailserver instanz übergeben
        ms = IMAP4_SSL("imap.gmail.com")                                            # dann mailserver instanz erstellen
    ms.login(USER, PW)                                                              # mailserver login
    return ms                                                                       # mailserver instanz returnen

def imap_logout(ms:IMAP4_SSL, clear=True):                                          # logout von mailserver
    if clear: ms.expunge()                                                          # mail-cache cleanup für UI wenn True 
    ms.close(); ms.logout()                                                         # mailbox schließen und server logout   

def get_new_mail_ids(ms:IMAP4_SSL=None, logout=True, clear=True):                   # ids ungelesener mails holen
    if not isinstance(ms, IMAP4_SSL):                                               # wenn keine mailserver instanz übergeben
        ms = imap_login(ms)                                                         # einloggen (optional)
    ms.select("inbox", readonly=False)                                              # inbox wählen
    _, data = ms.uid('search', None, 'UNSEEN')                                      # ungelesene mails suchen
    if logout: imap_logout(ms, clear)                                               # ausloggen (optional)
    return data[0].split() if data[0] else []                                       # ids extrahieren

def decode_mail(msg_data:list):                                                     # dekodiert mailteile
    for part in msg_data:                                                           # durchläuft jede mail-part
        if not isinstance(part, tuple): continue                                    # ignoriert nicht-tuple einträge
        msg = get_msg(part[1]); sender = parseaddr(msg.get("From"))[1]              # parst mail-bytes und holt absender
        subj = str(make_header(decode_header(msg["Subject"]))) or "Re: "            # dekodiert betreff
        if msg.is_multipart():                                                      # prüft ob multipart
            body = msg.get_payload(0).get_payload(decode=True).decode()             # dekodiert body der multipart mail
        else: body = msg.get_payload(decode=True).decode()                          # dekodiert einfachen body
    return subj, sender.lower(), body                                               # gibt betreff, absender, text zurück

def get_latest_unread_mail(ms:IMAP4_SSL=None, logout=False):                        # neuste ungeleseene email holen
    ids = get_new_mail_ids(ms, logout)                                              # ids ungelesener mails holen
    if not ids: return "", "", ""                                                   # empty: subject, sender, body 
    if ids:                                                                         # wenn ungeleseen mails vorhanden
        _, msg_data = ms.uid('fetch', ids[-1], "(RFC822)")                          # neuste ungelesene mail laden
        ms.uid('store', ids[-1], '+FLAGS', '\\Seen')                                # mail als gelesen markieren (inkl. UI)
        return decode_mail(msg_data)                                                # mail dekodieren (vereinfacht)

#-----------------------------------------------------------------------------------
# MAIL SEND HELPERS
#-----------------------------------------------------------------------------------

def get_mail_tmpl():                                                                # branded email templaten laden
    jinv = Jinv(loader=FSL('.'), autoescape=True)                                   # jinja environment object instanz
    return jinv.get_template("templates/email.html")                                # email template laden

def subject(subj:str):                                                              # bereitet betreff vor
    s = str(subj) or "Re: Your Message"                                             # generischer betreff, fall leer
    return s if s.lower().startswith("re:") else f"Re: {s}"                         # Re: falls nicht schon vorhanden

def prepare_mail(sender:str, to:str, subj:str, reply:str):                          # email für versand vorbereiten
    msg = EmailMessage()                                                            # message object instanz erstellen
    body = get_mail_tmpl().render(agent=reply, mailaddress=USER)                    # html body render und placeholder ersetzen
    msg['From'], msg['To'], msg['Subject'] = sender, to, subject(subj)              # email header setzen
    msg.set_content(body, subtype='html')                                           # email body setzen
    return msg                                                                      # message object returnen

def send_mail(user:str, pw:str, msg:EmailMessage):                                  # email versenden
    with SMTP_SSL("smtp.gmail.com", 465) as ms:                                     # mailserver instanz (context manager mit logout)
        ms.login(user, pw); ms.send_message(msg)                                    # smtp mailserver login und mail send

#-----------------------------------------------------------------------------------
# ‼️ GRUNDLEGENDE HINWEISE:
#-----------------------------------------------------------------------------------
    # Versch. Mailserver handhaben versch. Commands evtl. unterschiedlich.
    # Die Email-Verarbeitung hier ist ein Minimalst-Beispiel.
    # Reicht für unser Test-Beispiel gerade soeben aus.
    # So aber i.d.R. NICHT geeignet für Produktivnahme!
    # Für maximale Konfidenz bzgl. Klassifizierungs und Antwortkonsitenz sind:
    # -> weitaus mehr Test-Emails nötig (und. evtl. Promptanpassungen)
    # -> die viel schwieriger zu klassifizieren sind 
    # -> und inhaltlich zahlreiche Edge-Cases abdecken
#-----------------------------------------------------------------------------------
# ⚠️ WAS NOCH NÖTIG WÄRE (besonders wenn anderer Provider als GMail):
#-----------------------------------------------------------------------------------
    # Um jegliche Art von E-Mails wirklich sicher & dynamisch zu verarbeiten.
    # bedarf es weitaus mehr code.
    # Denn viele aspekte spielen eine rolle:
        # threading / mail history / cc / bcc / fwd
        # sender validierung: SPF, DKIM und DMARC
        # unzustellbarkeit handlen (Null-Sender, Error-Codes)
        # self-rate-limiting: zu viele abrufe -> imap sperre 
        # idempotenz -> doppelt verarbeitung verhindern
        # read/unread/move/delete management
        # html content vs. plain content
        # versch. anhänge (MIME-types)
        # inline-images mit Content-ID: cid
        # steuerzeichen in header verhindern
        # Outlook-Kompatibität: MSO / TNEF / winmail.dat (zu prüfen)
        # Virencanner wie ClamAV, insbesondere bei spam
        # Cross-Site Scripting (XSS) verhindern: 
        # -> stripping von <script>, <iframe>, onmouseover
        # versch. header standards, 
        # versch. subject kodierungen
        # versch. codierungen/alphabete
        # timezone handling
        # large payloads: größe mails können RAM memory überlasten
        # msg.walk(um durch ebenen zu iterieren
    # gilt auch für: utils.decode()
    # Gmail übernimmt aber einige Aspekte
#-----------------------------------------------------------------------------------
# 💵 UM KOSTEN ZU SPAREN kann z.B. in Erwägung gezogen werden:
#-----------------------------------------------------------------------------------
    # Prompt Caching beim LLM Provider
    # Erweiterung der noreply Kriterien
    # Begrenzung der Mail-Historie in Mail-Thread (wenn thread implementiert)
    # RAG nicht auf Mail-Historie des Threads anwenden
    # Similarity Threshold für RAG
    # SimHash / Hamming-Distance / Jaccard-Similarity (schneller als Cosine Sim)
    # Abschnittbasierte chunk sizes im RAG per Regex oder LLM 
    # Output (dynamisch) via max_tokens oder max_output_tokens begrenzen
    # Batch API-Calls an das LLM
    # lokales Model einzusetzen 
    # Reasoning Classifier Node mit Small Model für Reply Model Selection
    # Speichern von häufigen sehr ähnichen Eingangsmails und passenden Antworten
    # -> Recognition via Cosine Similarity (und threshold)
#-----------------------------------------------------------------------------------