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
"""
Prendere la lista degli utenti dalle pagine che abbiamo scaricato:
- devo cercare in ogni pagina che ho scaricato
- dalla pagina html individuo il pattern: <span class="Link--secondary">GiuliaF96</span>
- controllo di questa combinazione: r'<span class="Link--secondary(?: pl-1)?">([^<]+)</span>'
- se viene identificato il pattern metto tutto in una lista
"""


from requests import get
import re
import uuid
import datetime
import json

BASE_URL: str = "https://github.com"
END_URL: str = "tab=followers"

PATTERN = r'<a\s+[^>]*href="https://github\.com/([^/]+)\?page=(\d+)&amp;tab=followers"[^>]*>Next</a>'
PATTERN_USER = r'<span class="Link--secondary(?: pl-1)?">([^<]+)</span>'


"""
1. Leggere file
2. Verificare che sia presente il bottone Next
3. Se è presente, prendere l'url
4. Lanciare una nuova get e salvare il contenuto
"""
"""
ci serve un dizionario per salvare la lista:
conterrà una lista di dizionari 
[
    {
        id: "str di valori univoci uuid4.",
        createdAt: YYYY/MM/DD hh:mm:ss,
        users: [],
        numbersOfUsers
    }
]

1. ho bisogno di una funzione di modellazione della lista
2. apro il mio db con open, estraggo il contenuto - che è una lista
3. faccio append del nuovo elemento sulla lista che ho appena preso dal db
4. sovracrivo il vecchio db con il dato aggiornato
"""

def save(db_name: str, new_value: dict[str, str]) -> bool:
    db: list[str] = []
    with open(f"db/{db_name}", "r") as f:
        db.extend(json.load(f))
    db.append(new_value)
    with open(f"db/{db_name}", "w", encoding='utf-8') as f:
        json.dump(db, f, indent=4, ensure_ascii=False)
    return bool

def create_record_object(user_list: list[str]) -> dict[str, str]:
    if not user_list:
        return None
    
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    clean_date = now_utc.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    return {
        'id': str(uuid.uuid4()),  
        'createdAt': clean_date,  
        'users': user_list,
        'numberOfUsers': len(user_list)
    }

def is_next_botton(text: str) -> bool:
    if not text:
        raise ValueError("La stringa non può essere vuota!")
    return bool(re.search(PATTERN, text))


def main() -> None:
    
    controller: bool = True
    counter: int = 0  
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
    

  
    
    while controller:
        counter += 1
        url = f"{BASE_URL}/{nome_utente}?page={counter}&{END_URL}"
        try:
            response = get(url) # response è un oggetto
            print(response.status_code)
            
            with open(f"/home/sabri/whounfollowed/tmp/pagina-{counter}.txt", "w") as f:
                f.write(response.text)
                controller = is_next_botton(response.text)
                print("File salvato")
                
        except Exception as e:
            print(f"Errore: {e}")
    
    lista_utenti: list[str] = []
     
    for i in range(counter):
        print(f"Counter: {i + 1}")
        with open(f"tmp/pagina-{i+1}.txt", "r") as f:
            text = f.read()
            lista_utenti.extend(re.findall(PATTERN_USER, text))
    
    save("db.json", create_record_object(lista_utenti))
    print("Fine programma, arrivederci")

if __name__ == "__main__":
    main()