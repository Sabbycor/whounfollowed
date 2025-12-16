"""
requests - get
mandare la request, mi serve l'url
gestione eccezioni
voglio ottenere tutto il contenuto della pagina
salva in un file (open("nome file", "w"))
"""
from requests import get
import re

BASE_URL: str = "https://github.com/emanuelegurini?"
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
    controller: bool = True
    counter: int = 1
    print("Start del programma")
    
    
    while controller:
        url = f"{BASE_URL}page={counter}&{END_URL}"
        try:
            response = get(url) # response è un oggetto
            
            with open(f"/home/sabri/whounfollowed/tmp/pagina-{counter}.txt", "w") as f:
                f.write(response.text)
                controller = is_next_botton(response.text)
                counter = counter + 1
                print("File salvato")
                
        except Exception as e:
            print(f"Errore: {e}")
    print("Fine while e perchè i dati sono tutti scaricati")

if __name__ == "__main__":
    main()