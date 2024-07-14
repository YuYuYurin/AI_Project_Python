## Features 
- User-Input in Telegram und Integration OpenAI API
- reine OpenAI API Anfrage (openAI_request.py) -> die eingekauften Waren und Preise auf einem Quittung-Bild können gelesen werden
- Datenverarbeitung durch Funktionen brauchen noch Anpassungen:
    - input == text -> funktioniert
    - input == image -> man bekommt von determine_and_ask_openAI() nur "Case 03" zurückgegeben
    - Dadurch dass man nicht testen konnte, was man bei "Case 02" zurückbekommt, konnte man die Funktionen in excel_data_processing.py nicht anpassen.
    - excel_data_processing.py funktioniert aber unabhängig.


## TODO
- Man soll analysieren, warum man kein "Case 02" zurückbekommt
- Clean Code: Aktuell try_openAI-vision_02 ist nicht übersichtlich. Man soll überlegen, wie man die Funktionen besser strukturieren kann.
- Anpassung des Funktionskopf (excel_data_processing.py), je nach dem was man von openAI API zurückbekommen kann. 
- Try-Except-block einbauen

## Nice to have
- Datenbank implementierung

## Overview
Project/Concept_Step1.png
Project/Concept_Step2.png