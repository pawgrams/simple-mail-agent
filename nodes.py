# nodes.py
#-----------------------------------------------------------------------------------
from rag import *                                                                   # vektor- und embeddings funktionen
from utils import *                                                                 # hilfsfunktionen
from pydantic import BaseModel                                                      # paket für strict typing
from context import *                                                               # projekt-kontext
#-----------------------------------------------------------------------------------
class AgentState(BaseModel):                                                        # type für agentenstatus
    mail:   dict = {}                                                               # mail daten (hier: flexible keys)
    cat:    str  = ""                                                               # mail kategorie name
    reply:  str  = ""                                                               # antwort text
    status: str  = ""                                                               # status kennzeichen

#-----------------------------------------------------------------------------------
def m_read(state:AgentState):                                                       # NEUE EMAILS LESEN
    st = sub = sndr = body = "";                                                    # init: status und basic mail data
    ms = imap_login()                                                               # mailserver instanz und login
    try:                                                                            # evtl. errors handlen
        sub, sndr, body = get_latest_unread_mail(ms)                                # neuste ungeleseene email holen
        if not sndr or not_tester(sndr) or is_noreply(sndr): st = "skip"            # skip: noreply + echte addressaten in testmode
        print(f"📬 NEW MAIL: {sndr}: {sub}")                                        # status ausgabe
    except E as e: state.status = f"error"; raise E(f"❌ {e}")                      # bei error: erst AgentState updaten 
    finally: imap_logout(ms)                                                        # mail-cache cleanup, disconnect und logout
    return {"mail": {"sub": sub, "from": sndr.lower(), "body": body}, "status": st} # AgentState updaten

#-----------------------------------------------------------------------------------
def m_class(state:AgentState):                                                      # EMAIL KLASSIFIZIEREN
    st, m, tmpl = "", state.mail, read_file("prompts/classify.md")                  # status init, maildata kürzel, prompt template laden
    prompt = fill(tmpl, {"comp": read_file("info/company.json"), "mail": m})        # alle placeholder in prompt template befüllen 
    c = classify.invoke(prompt).content.strip().lower()                             # kategorie per KI ermitteln
    if not c in cats: c = "general"                                                 # fallback auf general wenn cat invalid
    if not c in CATS: st = "skip"                                                   # skip flag wenn cat inaktiv
    print(f"🏷️ CATEGORY: {c}"); return {"cat": c, "status": st}                     # cat printen und AgentState updaten

#-----------------------------------------------------------------------------------
def m_reply(state:AgentState):                                                      # ANTWORT PER KI GENERIEREN
    if state.status == "skip": return {}                                            # node überspringen, wenn skip flag
    tmpl = read_file(f"prompts/{state.cat}.md")                                     # lade template für kategorie
    pmap = {"comp": read_file("info/company.json"), "mail": state.mail}             # placeholder mapping bauen
    data = search_vec("info/details.pdf", state.mail) or ""                         # suche relevante info
    rag_ix = f"- Where suitable, consider following info for your reply: '{data}'"  # agent instruction für RAG daten  
    pmap["data"] = "" if not data else rag_ix                                       # data placeholder leer wenn keine RAG daten
    prompt = fill(tmpl, pmap)                                                       # alle placeholder in prompt template befüllen 
    reply = response.invoke(prompt).content                                         # email antwort mit KI generieren
    print(f"🤖 AGENT REPLY: {reply[:40]}..."); return {"reply": reply}              # AgentState updaten + printen

#-----------------------------------------------------------------------------------
def m_send(state:AgentState):                                                       # EMAIL VERSENDEN
    if state.status == "skip": return {}                                            # node überspringen, wenn skip flag
    msg = prepare_mail(USER, state.mail["from"], state.mail["sub"], state.reply)    # email vorbereiten
    try:                                                                            # evtl. errors handlen   
        send_mail(USER, PW, msg)                                                    # email versenden
        print(f"✅ MAIL SENT"); return {"status": "ok"}                             # AgentState updaten + printen
    except E as e: state.status = f"error"; raise E(f"❌ {e}")                      # bei error: erst AgentState updaten 
        
#-----------------------------------------------------------------------------------
