Dokumentation gymnasieatbete
====

Deltagare i gruppen
----

* Folke Ishii - Jag kommer utveckla denna produkt helt själv och jag ansvarar för bland annat programmeringen, designutvecklingen och 3d-modelleringen

Frågeställning
----

Min produkt ska kunna svara på / vara lösningen till dessa frågor och problem

1. Hur kan man öka produktiviteten när man sitter vid datorn?
2. Hur ska man snabbt och smidigt få reda på information gällande ens dator och omgivning när man är upptagen med annat på datorn?
3. Vad krävs för att förbättra ens upplevelse med datorn?
4. Hur gör man när ett eller flera program tar upp all yta på skärmen (eller flera) och man vill kolla något snabbt som till exempel tiden utan att kolla på mobilen och/eller stänga ner programmen?

Vad handlar mitt gymnasieprojekt om?
----

Mitt projekt är en "Informative dashboard and app launcher" / "Interaktiv informationspanel samt applikationsstartare för en dator" vilket menas att det är en digital instrumentbräda för datorn som kan ansvara för framvisandet av information gällande systemet och omgivningen samt kunna snabbt och smidigt starta applikationer som finns på datorn. Denna instrumentbräda kommer visas på en skärm som ska sitta mellan ens tagnentbord och datorskärm. Projektet kommer omfatta skapandet av ett stöd för skärmen och datorprogrammet.

Metod
----

Jag kommer använda mig av mina erfarenheter gällande mobilstället för att kunna 3d-modellera och utveckla ett ställ för skärmen. Processen kommer vara rätt så lik CDIO-processen men eftersom den är enbart för mig, kommer jag hoppa över vissa steg såsom målgruppsundersökningen. När stället är gjort så kommer programeringsprocessen. Det är då som programmet och all dess logik ska skapas. När programmet fungerar så kommer gränssnittsdelen, då jag ska skapa ett gränssnitt åt produkten. Detta kommer inte ske i ordning utan dessa tre processer kommer utfärdas samtidigt. Det är svårt att beskriva metoden tidigt eftersom den kommer definivt att ändra sig genom arbetet då jag kommer troligtsvis lära mig nya saker. 

Kravspecifikation - mjukvara
----

#### Krav

* Programmet ska inte ta fokus när kommandon utförts. Med andra ord ska man kunna fortsätta skriva i samma textruta efter att ett kommando har utförts. 
* Andra programm (och eventuellt muspekaren) ska inte kunna hamna på den skärmen med programmet. (http://dualmonitortool.sourceforge.net/)
* Programmet ska styras med tagnetbordet och andra tagnetkombinationer som ska uppstå ska förtryckas.
* Det ska vara lätt att lägga till / ta bort program.
* Programmet ska starta med operativsystemet.
* Programmet ska fungera på både Windows och Linux

#### Önskemål

* Det ska fungera på flera storlekar

Kravespecifikation - hårdvara (Ställ)
----

#### Krav

* Kabeln till tangentbordet ska åka under stativet
* Skydda PCB:en från damm etc.

#### Önskemål

* Justebar för vinkel

Planering
---- 

| Datum | Vad som gjordes | Tills nästa lektion |
| :---- | :-------------- | :------------------ |
| 28 Aug 2020 - 02 Sep 2020 | Skapade applikationsfönstret och lade till en klocka som visar vecka, datum och tid. Lade till ett schema för tagnentskombinationer och förtryckte de vanliga. | Skapa dokumentationsdokument |
| 03 Sep 2020 | Skapade ett dokument för dokumentationen. | Skapa grunden för applikationen |
| 04 Sep 2020 | Började på integration med Spotify för att visa låt. | Få det att fungera. |
| 05 Sep 2020 | Började på implementation för olika sidor och hur alla sidor komminucerar med varandra. | Gör systemet bättre och mer flexibelt - Gör första prototyp för gränssnittet |

Idéer för olika sidor
----

1. VLC Kontroller
2. Kolla väder
3. Progression för min 3D-printer
4. Discord (Den kommer bli jobbig)
5. Youtube + Youtube kontroller
6. App launcher + Subfolders för varje emulator etc
7. Mappar
8. Systeminformation såsom RAM/CPU/GPU
9. Mail
10. Eventuella appar som används ofta
11. Lägga till / ta bort

#### Annat som ska visas alltid

1. Tid + datum
2. Spotify-information
3. Scrollbar
4. Mic på/mutad
5. Om extra plats på höger sida: något med Discord?


Hur ska man kunna lägga till / ta bort sidor?
----

Att helt kunna lägga till en sida kommer man inte kunna göra via panelen, men den kommer generera koden för en mall. Vad som krävs är:

* Lägga till en mapp i /app/widgets
* Generera python koden för sidan
* Generera .ui koden för sidan
* Lägga till en platshållare fil för ikonen
* Ändra på /app/widgets/__init__.py
* Omstart krävs - ett måste

Sedan kan vissa sidor ha sina egna sätt att lägga till / ta bort saker. Som till exempel kan appstartaren kunna lägga till / ta bort applikationer enbart från panelen.

Annat att tänka på:
----

Skärmen är 8.8cm * 15.6cm om man sitter 50-60 cm ifrån den. Alla typsnitt ska vara mono-spaced
