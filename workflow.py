# workflow.py
#-----------------------------------------------------------------------------------
from os import environ                                                              # zugriff auf environment variablen
from nodes import *                                                                 # alle node-definitionen
from langgraph.graph import StateGraph, END                                         # workflow graph und end-state
from langgraph.graph.state import CompiledStateGraph                                # kompilierte graphklasse
from socket import socket as sc, AF_INET as I, SOCK_STREAM as S                     # socket für verbindungstest
from logging import getLogger as log, WARNING                                       # logger und warn-level
from subprocess import Popen, DEVNULL as DN                                         # subprocess für prozess-start
from sys import executable as exec                                                  # python ausführbares programm
from time import sleep                                                              # sleep-funktion
from utils import get_new_mail_ids                                                  # für quick-check ob unread mails
from traceback import print_exc
#-----------------------------------------------------------------------------------
def langsmith():                                                                    # startet lokale dev-instanz falls nötig
    for p in ("watchfiles", "langgraph"): log(p).setLevel(WARNING)                  # setzt log-level der modules auf warning
    environ["LANGGRAPH_SDK_LOG_LEVEL"] = "error"                                    # setzt env log-level auf error
    if sc(I,S).connect_ex(('127.0.0.1', 2024)) != 0:                                # prüft ob lokaler server läuft
        Popen([exec, "-m", "langgraph_cli", "dev"], stdout=DN, stderr=DN)           # startet langgraph dev-server

#-----------------------------------------------------------------------------------
def build_workflow(nodes: tuple):                                                   # baut workflow aus node-namen
    wf = StateGraph(AgentState)                                                     # erstellt neuen stategraph
    for i, nd in enumerate(nodes):                                                  # durchläuft alle nodes
        wf.add_node(nd, globals()[nd])                                              # fügt node dynamisch aus globals hinzu
        if i < len(nodes)-1: wf.add_edge(nd, nodes[i+1])                            # verbindet node mit nächster node
        else: wf.add_edge(nd, END)                                                  # letzte node → end
    wf.set_entry_point(nodes[0])                                                    # setzt start-node
    return wf.compile()                                                             # kompiliert workflow

#-----------------------------------------------------------------------------------
langsmith()                                                                         # stellt sicher, dass dev-server läuft
nodes = ("m_read", "m_class", "m_reply", "m_send")                                  # definiert workflow nodes
workflow: CompiledStateGraph = build_workflow(nodes)                                # erstellt workflow
print("\033c")                                                                      # steuerzeichen um console zu clearen
while True:                                                                         # endlosschleife
    try: workflow.invoke({}) if get_new_mail_ids() else print("📭 NO NEW MAILS")    # workflow ausführen wenn neue mails
    except: print_exc()                                                             # zeigt und fängt fehler ab 
    print("-"*100); print("next query in 10 secs ..."); sleep(10)                   # trennlinie, pause info + pause 
    
#-----------------------------------------------------------------------------------