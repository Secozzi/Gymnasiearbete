Gymnasiearbete
====

Installation
----

1. Se till att Python 3.7 - 3.8.6 är installerat
2. Ladda ned projektet från Github.
3. Kör kommandot `pip install -r requirements.txt` i Gymnasiearbete mappen
4. I VLC, aktivera Telnet och sätt ett lösenord för Lua Telnet
5. I mappen "app", skapa filen "credentials.cfg" och sätt följande variabler:
````
[SPOTIPY]
CLIENT_ID = 
CLIENT_SECRET = 
REDIRECT_URI = 

[VLC]
PASSWORD = 
````

Där Spotipy är dina Spotify variabler (se [Spotify](https://developer.spotify.com/dashboard/applications) och [Spotipy](https://spotipy.readthedocs.io/en/2.16.0/)) och VLC password är lösenordet som angavs i steg 4.

6. Ange konstanter i koden. Dessa är:
* Koordinater i `/app/widgets/smhi/data_thread.py` rad 46-47
* Path till steam.exe i `/app/widgets/launcher/launcher.py` rad 55
7. Skapa en genväg av app/app.pyw och lägg den i autostart-mappen (Win+r och shell:startup)