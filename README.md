# 📧 simple-mail-agent

Ein minimalistischer, vollständig codezeilenweise kommentierter E-Mail-Agent auf Basis von **LangGraph**, **IMAP/SMTP** und **RAG**.
Er liest ungelesene Mails, klassifiziert sie per LLM, erzeugt eine passende Antwort und versendet sie.
Gedacht als verständlicher Einstieg und als Grundgerüst, auf dem sich aufbauen lässt.

## Grundlegendes

<details><summary>&nbsp;<h2><b>⭐ LangChain / LangGraph / LangSmith</b></h2></summary><h4>

```
Industry Leading & State-of-the-Art Framework für: 
- Cross LLM Orchestration
- Tailored Asynchronous Agentic Workflows
- Agent Tracing & Cost Monitoring (LangSmith)
- RAG & Context Management
- u.v.m.
- Dickes Plus im Lebenslauf!
```

#### Website: [https://www.langchain.com/](https://www.langchain.com/)

</h4></details>
<details><summary>&nbsp;<h2><b>🤖 Was der Agent macht</b></h2></summary><h4>

```
Der Workflow besteht aus vier Nodes, die als Graph hintereinandergeschaltet sind:

Node      Aufgabe
-------   -----------------------------------------------------------------------
m_read    Ungelesene Mail per IMAP abrufen, dekodieren, als gelesen markieren
m_class   Mail per LLM einer Kategorie zuordnen (sales, support, spam etc)
m_reply   Antwort generieren (sales, support, general: mit RAG-Kontext aus PDF)
m_send    Antwort als HTML-Mail per SMTP senden (spam / noreply: übersprungen)
```
```
- Der Loop prüft alle 10 Sekunden auf neue Mails
- Jeder Durchlauf ist in LangSmith nachvollziehbar
```

</h4></details>
<details><summary>&nbsp;<h2><b>❓ Warum IMAP/SMTP statt MCP Connector</b></h2></summary><h4>

```
- Fertige Mail-Connectoren und MCP-Integrationen sind bequem
- Unterliegen aber je nach Anbieter und Scope Einschränkungen
- z.B. beim Zugriff auf sicherheitsrelevante Nachrichten
  - wie Tokens bei Verifizierung nach SignUps oder Password-Resets, etc.
- Für Automationen, die genau solche Mails brauchen, bleiben IMAP/SMTP relevant
- Zudem funktionieren sie praktisch mit nahezu allen Mailservern (migrateable)
```

</h4></details>
<details><summary>&nbsp;<h2><b>✅ Voraussetzungen</b></h2></summary><h4>

```
- Python 3.13
- Google-Konto mit aktivierter 2FA und Google App-Passwort
- OpenAI API Key (andere LLMs mit Code-Anpassung integrierbar)
- LangSmith Account (kostenlos)
- Zweites Mailkonto zum Senden der Test-E-Mails
```

</h4></details>

---

## Anleitung

<details><summary>&nbsp;<h2><b>1️⃣ GOOGLE APP PASSWORT</b></h2></summary><h4>

#### Schritt-für-Schritt Anleitung: [HIER](https://github.com/pawgrams/google-app-pw-guide/tree/main)

```
- Verwende ein neues separates Google Konto, dass Du für keine anderen Zwecke einsetzt
- Mehrere Email-Konten pro Telefonnummer sind möglich
- Das Kontingent ist evtl. größer, wenn Du per Smart Phone ein neues Konto zu dem bestehenden hinzufügst
- Das Basis-Konto zur Telefonnummer sollte möglichst schon eine Weile organisch genutzt worden sein
- Sonst kann das neue Konto als suspicious geflaggt und eingefroren werden
```

</h4></details>
<details><summary>&nbsp;<h2><b>2️⃣ PROJECT INIT</b></h2></summary><h4>

#### Variante A: Repository klonen

```
git clone https://github.com/cimdatapaw/simple-mail-agent.git
```

#### Variante B: Komplettpaket als ZIP: [HIER](https://drive.google.com/file/d/1BcmOknjy0vLmCFlSyqNR4ft0RafyL9Cm/view?usp=sharing)

```
- ZIP herunterladen und entpacken
- Dann den entpackten `simple-email-agent` Ordner als root in VS Code öffnen
```

#### Zum Senden der Test-E-Mails, Proton-Mail Account einrichten: [HIER](https://proton.me/)

</h4></details>
<details><summary>&nbsp;<h2><b>3️⃣ SECRETS (.env)</b></h2></summary><h4>

#### a) LangSmith Projekt anlegen

```
- BESUCHE DAFÜR: https://smith.langchain.com
- NICHT FOLGENDE URL: https://eu.smith.langchain.com/
  -> Achte darauf, dass Du keinen EU-Account erstellst (sonst Probleme)
- Wähle "US" und registriere Dich mit Deinem neu erstellten Gmail Account
- Wähle: 'Technical', dann 'LangSmith Observability (Code first experience)'
- Dann in LangSmith oben links direkt unter 'Application' das Dropdown-Menu aufklicken
- Im Dropdown auf Plus ('+') klicken
- Projektname: 'test_email_agent' eingeben, dann mit `Create Application` Button bestätigen
- Dann Projektnamen 'test_email_agent' in Deiner '.env' bei 'LANGCHAIN_PROJECT=' reinkopieren 
```

#### b) Langsmith API Key

```
- Zurück in LangChain unten links 'Settings' (Zahnrad-Symbol) klicken
- Dann oben rechts auf '+API KEY' klicken
- Bei Description 'test_email_agent' eintragen, dann mit 'Create API Key' Button bestätigen 
- API Key sofort kopieren und in Deiner '.env' bei 'LANGCHAIN_API_KEY=' reinkopieren
```

#### c) Übrige Secrets

```
- In '.env' die 'LANGCHAIN_TRACING_V2=true' setzen
- Bei 'GMAIL_APP_PASSWORD=' Dein Google App Passwort aus Schritt 1 eintragen (inkl. Leerzeichen)
- Und Deine neue GMail Addresse bei `GMAIL_ADDRESS=` eintragen
- Bei 'TESTER_ADDRESS=' Email Addresse eintragen von der Du Test-Emails sendest (nicht gleiche wie GMAIL_ADDRESS)
- Bei 'OPENAI_API_KEY=' Deinen OpenAI API Key eintragen
```

#### ‼️ Falls Du das Projekt selbst wieder hochlädst

```
- Die '.env' liegt hier bewusst mit Platzhaltern im Repo, damit der Einstieg einfach ist
- Sie ist daher von Git getrackt und wird NICHT von einer '.gitignore' erfasst
- Sobald Du Deine echten Keys eingetragen hast, gilt daher als TODO:
  1. '.env' in die '.gitignore' eintragen
  2. Aus dem Tracking nehmen:   git rm --cached .env
- Sonst landen Deine Keys beim nächsten 'git add . && git push' öffentlich im Netz
```

</h4></details>
<details><summary>&nbsp;<h2><b>4️⃣ INSTALLS</b></h2></summary><h4>

```
- Öffne das Terminal in VS Code und führe folgende Commands aus:
  - Windows:   .\installs\installs.bat
  - Mac:        chmod +x installs/installs.sh && ./installs/installs.sh
- Geduld: Kann ein paar Minuten in Anspruch nehmen.
- Warte bis "Installation fertig!" in Konsole erscheint.
```
  
<details><summary>&nbsp;<h3><b>Zur Kenntnis</b></h3></summary><h6>
  
```
Die Datei führt automatisch folgende Commands aus:
- py -3.13 -m venv venv (windows)  python3.13 -m venv venv  (mac)
- venv\Scripts\activate (windows)  source venv/bin/activate (mac)
- Sowie folgende (bei windows ohne die `3`):
python3 -m pip install --upgrade pip
python3 -m pip install openai
python3 -m pip install python-dotenv
python3 -m pip install pydantic
python3 -m pip install langchain_text_splitters
python3 -m pip install langchain_openai
python3 -m pip install langchain_community
python3 -m pip install jinja2
python3 -m pip install pypdf
python3 -m pip install faiss-cpu
python3 -m pip install langgraph
python3 -m pip install -U "langgraph-cli[inmem]"
python3 -m pip install pipreqs
```
```
- Dabei werden auch Abhängigkeiten einzelner Packages installiert.
- Virtual Environment (venv) wird automatisch erstellt.
- Dort liegen alle Packages lokal in isolierter Umgebung für Python3.13 
  -> venv/Lib/site-packages/...
- Sind daher nur für den Projektordner installiert und verfügbar.
```

</h6></details>
</h4></details>
<details><summary>&nbsp;<h2><b>5️⃣ STARTEN</b></h2></summary><h4>

```
- Windows:   python workflow.py
- Mac:       python3 workflow.py
```
```
- Sende eine Test-E-Mail von Deiner 'TESTER_ADDRESS' an Deine 'GMAIL_ADDRESS'
- Im Terminal lässt sich jeder Schritt mitverfolgen
- Beispiel-Mails zum Kopieren liegen im Ordner 'testmails'
```
```
- Der lokale LangGraph-Dev-Server (Port 2024) startet nicht auf jedem System zuverlässig
- Die Traces sind davon unabhängig einsehbar:
  -> Dafür das Projekt 'test_email_agent' in LangSmith manuell öffnen
```

</h4></details>

---

## Weiteres

<details><summary>&nbsp;<h2><b>📂 Projektstruktur</b></h2></summary><h4>

```
simple-mail-agent/
├── info/
│   ├── company.json
│   ├── details.md
│   └── details.pdf
│
├── installs/
│   ├── installs.bat
│   └── installs.sh
│
├── prompts/
│   ├── classify.md
│   ├── general.md
│   ├── invoice.md
│   ├── marketing.md
│   ├── privacy.md
│   ├── sales.md
│   └── support.md
│
├── templates/
│   └── email.html
│
├── testmails/
│   ├── general_01.txt
│   ├── invoice_01.txt
│   ├── marketing_01.txt
│   ├── privacy_01.txt
│   ├── sales_01.txt
│   ├── sales_02.txt
│   ├── sales_03.txt
│   ├── spam_01.txt
│   ├── spam_02.txt
│   └── support_01.txt
│
├── .env
├── context.py
├── langgraph.json
├── nodes.py
├── rag.py
├── README.md
├── utils.py
└── workflow.py
```
```
Zur Runtime werden automatisch weitere Ordner erstellt: 
  '__pycache__', 'langchain-api', 'vecstore'
```
```
Zur Info: 
- Eine 'requirements.txt' liegt nicht bei, lässt sich aber jederzeit erzeugen.
- Dafür muss venv im Terminal aktiv sein
- Also im Zweifel nochmal: 
     Windows: venv\Scripts\activate
     Mac:     source venv/bin/activate
- Dann 'requirements.txt' mit folgendem Command erstellen: 
     Windows:    python -m pipreqs.pipreqs . --force --encoding=utf-8
     Mac:        python3 -m pipreqs.pipreqs . --force --encoding=utf-8
```

</h4></details>
<details><summary>&nbsp;<h2><b>ℹ️ Gmail via SimpleMail</b></h2></summary><h4>

```
- Für Gmail gibt es noch eine sicherere Variante:
  - Ist beim Einrichten aufwendiger, aber im Code simpler
  - https://github.com/jeremyephron/simplegmail)
  - https://console.cloud.google.com)
  - 'token.json', und 'credentials.json' 
```

</h4></details>

