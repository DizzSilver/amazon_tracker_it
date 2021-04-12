#   File:           tracker.py
#   Autore:         Dennis Benco
#   Data:           12/04/2021
#
#   Requisiti:      beautifulsoup4, pandas, requests.
#
#   Descrizione:    Questo semplice script tiene traccia del prezzo di un prodotto Amazon a scelta.
#                   *Funziona solo con la versione italiana di Amazon* per il modo in cui il prezzo viene
#                   formattato. (es. nella versione spagnola ci sono separatori diversi, 
#                   nella versione inglese cambiano sia i separatori che il simbolo ecc.).
#                    
#                   Il vantaggio di questo script è che a differenza di altri permette di visualizzare, 
#                   copiare o anche modificare il file .csv mentre il programma è in esecuzione, 
#                   *tranne quando sta eseguendo il salvataggio (circa 3 secondi ogni 6 ore di default).*
#
#   Istruzioni:     Non c'è bisogno di creare e configurare nessun database, tutti i dati verrano salvati
#                   all'interno del file con estensione .csv all'interno della cartella "dati", 
#                   quindi facilmente importabile su excel per creare grafici o altro.
#
#                   Avviare con "python3 main.py" e tenere il programma aperto (preferibilmente su un server, 
#                   o anche più comodamente su un Raspberry Pi perciò che sia sempre in esecuzione) e aspettare.
#
#                   *ATTENZIONE*: Dare un occhiata al codice perché ci sono varie cose da modificare
#                   per adattare lo script alle proprie esigenze ma soprattutto per farlo funzionare, 
#                   ho lasciato un po' di spiegazioni in giro per facilitare.

import requests
from bs4 import BeautifulSoup
import random
import sys
import pandas as pd
from datetime import datetime
from time import sleep

# Contatore dei cicli compiuti (1 ciclo = 1 nuova riga di dati), non modificare
contatore = 1

# Prezzo sotto il quale scatta la notifica, modificare a piacimento
soglia = 0.0

# Numero di secondi che passano tra ogni scan (21600 = 6 ore), modificare a piacimento
intervallo = 21600

# Modificare a piacimento
URL = "URL DEL PRODOTTO DA TRACCIARE"


# Funzione che utilizza un bot telegram per inviare una notifica quando il prezzo scende sotto una certa soglia (è necessario prima creare un bot telegram)
def telegram_bot(messaggio_bot):
    bot_token = "INSERISCI IL TOKEN DEL BOT TELEGRAM (OPZIONALE)"
    bot_chatID = "INSERISCI IL CHATID DEL BOT TELEGRAM (OPZIONALE)"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + messaggio_bot
    response = requests.get(send_text)
    return response.json()


# Funzione che appende ogni nuova riga in fondo al file .csv
def append_df(path_file, df):   
    with open(path_file, 'a+') as f:
        df.to_csv(f, header=f.tell() == 0, encoding='utf-8', index=False, sep=';', decimal=',')


# Funzione che accorcia l'URL passato come argomento
def extract_url(url):   
    if url.find("www.amazon.it") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.it" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.it" + url[index:index2]
            else:
                url = None

    else:
        url = None
    return url


# Funzione che converte il prezzo in un formato leggibile
def get_converted_price(price):
    stripped_price = price.strip("€ ,")
    replaced_price = stripped_price.replace(",", ".")
    converted_price = float(replaced_price)
    return converted_price


# Funzione principale che ottiene le informazioni per poi inserirle nel file .csv
def get_product_details(url):
    
    seedValue = random.randrange(sys.maxsize)
    random.seed(seedValue)

    useragent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Datanyze; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.24 Safari/537.36",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"
    ]
    
    # Scelta casuale di un "user agent" presente nella lista in alto
    useragent = random.choice(useragent_list)   

    secfetchsite_list = [
        "none",
        "same-origin"
    ]

    # Scelta casuale di un "secfetchsite" tra i due presenti nella lista in alto
    secfetchsite = random.choice(secfetchsite_list) 

    acceptlang_list = [
        "it-IT,it;q=0.9",
        "en-US.en;q=0.8",
        "zh-TW,zh;q=0.4",
        "zh-CN,zh;q=0.8"
    ]

    # Scelta casuale di un "acceptlang" presente nella lista in alto
    acceptlang = random.choice(acceptlang_list) 

    # Creazione degli headers della richiesta automatica, molto dettagliata per simulare quella di un browser reale e quindi evitare di venire bloccati.
    HEADERS = {     
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": useragent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": secfetchsite,
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Refer": "https://www.google.com/",
        "Accept-Language": acceptlang,
        "Accept-Encoding": "gzip, deflate, br",
    }

    giorno = datetime.now()
    data = giorno.strftime("%d/%m/%Y %H:%M")

    # Struttura del file .csv contenente i dati finali
    details = {"N°": [contatore], "Data": [data], "Nome": [""], "Prezzo": [0.00], "Sconto": [True], "URL": [""]}    

    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["Sconto"] = False
        if title is not None and price is not None:
            
            details["Nome"] = title.get_text().strip()
            # Se il nome di default è troppo lungo basta sostituire tutto destra dell'uguale con un nome a piacere tra virgolette
            
            details["Prezzo"] = get_converted_price(price.get_text())
            details["URL"] = _url
        else:
            return None

    #if details["Prezzo"] < soglia:
        #telegram_bot("L'articolo [INSERIRE NOME PRODOTTO] è sceso sotto i " + str(soglia) + "€")
        
        # ATTENZIONE: Togliere i due commenti precedenti per abilitare la ricezione di una notifica quando il prezzo scende sotto la soglia

    df = pd.DataFrame(details)
    append_df('./dati/prodotto.csv', df)


# Ciclo infinito che esegue la funzione, tiene conto del numero di cicli eseguiti e aspetta tot secondi al prossimo ciclo
while True: 
    print("inizio ciclo n°: " + str(contatore))
    get_product_details(URL)
    print("finito il ciclo n°: " + str(contatore) + "\n")
    contatore = contatore + 1
    sleep(intervallo)
