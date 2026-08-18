# rag.py
#---------------------------------------------------------------------------------
import os 
from langchain_openai import OpenAIEmbeddings as Embed
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as Split
#---------------------------------------------------------------------------------

def load_pdf(path: str):                                                            # lädt dokument basierend auf pfad
    path = path.lower()                                                             # pfad in kleinbuchstaben
    if path.endswith(".pdf"): return PyPDFLoader(path)                              # falls pdf, lade pdf

def set_vec(path, size=500, overlap=50):                                            # erstellt vektorstore
    data = load_pdf(path).load()                                                    # lade dokument
    chunks = Split(chunk_size=size, chunk_overlap=overlap).split_documents(data)    # splitte text in chunks
    store = FAISS.from_documents(chunks, Embed())                                   # erstelle faiss store mit embeddings
    store.save_local(f"vecstore/{path}")                                            # speichere lokal
    return store                                                                    # gib store zurück

def get_vec(path, allow=False):                                                     # lädt bestehenden store
    vpath = f"vecstore/{path}"                                                      # pfad zum store
    if not os.path.exists(vpath): set_vec(path)                                     # erstelle store falls nicht vorhanden
    try: return FAISS.load_local(vpath, Embed(), "index", allow_dangerous_deserialization=allow)  # lade faiss store
    except Exception as e: print(e)                                                 # fehler ausgabe

def search_vec(path: str, context: str, top_k: int = 3):                            # suche ähnliche dokumente
    store: FAISS = get_vec(path, True)                                              # lade store intern
    data = store.similarity_search(str(context), top_k)                             # führe ähnlichkeitssuche aus
    return " ... ".join([d.page_content for d in data])                             # kombiniere ergebnisse als string

#---------------------------------------------------------------------------------
# HINWEISE: ...
#---------------------------------------------------------------------------------
# ZU FAISS (pickle files und allow_dangerous_deserialization)
# Vektorisiert man nur eigene Dateien, dann kein Risiko
# Würde man Daten die User senden vektorisieren, sollte man:
# - z.B. ChromaDB oder LanceDB statt FAISS nutzen (sicherer aber langsamer), oder
# - schon in 'set_vecstore()' checks durchführen ob Inhalte schadhaft sein könnten
#---------------------------------------------------------------------------------