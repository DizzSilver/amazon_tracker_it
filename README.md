# amazon_tracker_it
Un semplice script che permette di tenere traccia del prezzo di uno o più prodotti Amazon, per poi creare grafici e/o venire notificati della scesa di un prezzo.

Requisiti:      beautifulsoup4, pandas, requests.

Descrizione:    Questo semplice script tiene traccia del prezzo di un prodotto Amazon a scelta.
                *Funziona solo con la versione italiana di Amazon* per il modo in cui il prezzo viene
                formattato. (es. nella versione spagnola ci sono separatori diversi, 
                nella versione inglese cambiano sia i separatori che il simbolo ecc.).
                   
Il vantaggio di questo script è che a differenza di altri permette di visualizzare, 
copiare o anche modificare il file .csv mentre il programma è in esecuzione, 
*tranne quando sta eseguendo il salvataggio (circa 3 secondi ogni 6 ore di default).*

Istruzioni:     Non c'è bisogno di creare e configurare nessun database, tutti i dati verrano salvati
                all'interno del file con estensione .csv all'interno della cartella "dati", 
                quindi facilmente importabile su excel per creare grafici o altro.

Avviare con "python3 main.py" e tenere il programma aperto (preferibilmente su un server, 
o anche più comodamente su un Raspberry Pi perciò che sia sempre in esecuzione) e aspettare.
                 
*ATTENZIONE*:   Dare un occhiata al codice perché ci sono varie cose da modificare
                per adattare lo script alle proprie esigenze ma soprattutto per farlo funzionare, 
                ho lasciato un po' di spiegazioni in giro per facilitare.
