## Wichtige Hinweise

Die requirements.txt aktuell halten (Ihr könnt euch die aktuelle installieren Module über den Befehl pip freeze ausgeben lassen)

## Zugriff auf die DB über:
Zugriffsdaten:

Nutzer: root
Passwort: hbX1AoLSjhdnznc


## Docker

Hinweis: Die Installation ist auf Windows ein bisschen komplex

Eine gute Anleitung dazu bietet https://docs.docker.com/desktop/install/windows-install/


Um mit VS Code eine gute Docker Integration zu erreichen sind die Extension sinnvoll:

ms-vscode-remote.remote-containers
ms-azuretools.vscode-docker

Mit diesen Extensions kann über die Option Attach Visual Studio Code im Context Menü direkt auf das Dateiverzeichnis in einem Docker Container zugegriffen werden.
Folgende Befehle werden zur Administration der Container benötigt:

Starte und BAUEN alle Container:
docker compose up --build -d

Stoppe und ENTFERNE alle Container:
docker compose down

Stoppe alle Container:
docker compose stop

Starte alle Container neu:
docker compose start

Liste von alle Containern (mit -a auch gestoppte):
docker ps -a



## Nutzung ohne Docker
Sollte aus irgendwelchen Gründen eine Umstellung von Docker zurück zu einem non-containerized System notwendig sein, müssten folgende Anpassungen getätigt werden:
(Ich kann mir keinen Grund vorstellen, warum das jemals nötig sein sollte)

### MongoDB Installieren (Am besten auch einen MongoDB Viewer z.B. MongoDB Compass)
Die MongoDB URI im DataStore anpassen (Von db zu localhost standartmäßig mongodb://localhost:27017)
Manuelle die dependencies für unser Script (requirements.txt) installieren. (pip install --no-cache-dir -r requirements.txt)