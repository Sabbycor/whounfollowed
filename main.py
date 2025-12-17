"""
requests - get
mandare la request, mi serve l'url
gestione eccezioni
voglio ottenere tutto il contenuto della pagina
salva in un file (open("nome file", "w"))
"""
""" 
- Input: dobbiamo impostare un input nel nostro programma, per prendere il valore dall'utente
- controllare che il valore inserito esista o no
    - se il nome esiste, continuiamo con lo scraping
    - se il nome non esiste mostriamo un messaggio che dice che il profilo non esiste
"""
from requests import get
import re

BASE_URL: str = "https://github.com"
END_URL: str = "tab=followers"

PATTERN = r'<a\s+[^>]*href="https://github\.com/([^/]+)\?page=(\d+)&amp;tab=followers"[^>]*>Next</a>'
"""
1. Leggere file
2. Verificare che sia presente il bottone Next
3. Se è presente, prendere l'url
4. Lanciare una nuova get e salvare il contenuto
"""

def is_next_botton(text: str) -> bool:
    if not text:
        raise ValueError("La stringa non può essere vuota!")
    return bool(re.search(PATTERN, text))


def main() -> None:
    
    controller: bool = False 
    print("Start del programma")
    
    while True:
        try:
            nome_utente: str = input("Inserisci lo username del profilo Github che vuoi analizzare: ")
            if not nome_utente:
                raise ValueError("Il nome non può essere vuoto")
            #TODO:il nome exit esiste già come profilo
            if nome_utente.strip().lower() == "exit":
                break
        
            print(f"Stai cercando: {nome_utente}")


            response = get(f"{BASE_URL}/{nome_utente}")
            
            if response.status_code == 404:
                print("Il profilo non esiste")
            else:
                print(f"Profilo {nome_utente} trovato")
                controller = True
                break
        except Exception as e:
                print(f"Qualcosa è andato storto. Messaggio: {e}")
    

    counter: int = 1
    
    
    while controller:
        url = f"{BASE_URL}/{nome_utente}?page={counter}&{END_URL}"
        try:
            response = get(url) # response è un oggetto
            print(response.status_code)
            
            with open(f"/home/sabri/whounfollowed/tmp/pagina-{counter}.txt", "w") as f:
                f.write(response.text)
                controller = is_next_botton(response.text)
                if controller:
                    counter += 1
                print("File salvato")
                
        except Exception as e:
            print(f"Errore: {e}")
    print("Fine programma, arrivederci")

if __name__ == "__main__":
    main()