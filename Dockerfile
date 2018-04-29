FROM ubuntu:latest

# Update Ubuntu et installation python3
RUN apt-get update -y
RUN apt-get install python3
RUN apt-get install python3-pip

# Copie de tous les fichiers dans le conteneur
COPY . .

# Installation de l'environnement virtuel python3
RUN apt-get install virtualenv
# On se place dans l'environnement virtuel
RUN python3 -m virtualenv venv
RUN source venv/bin/activate

# Installation des paquets python3 utiles à l'application
RUN pip3 install -r requirements.txt

# Demarrage du service mongo + scrapping
RUN service mongod
RUN scrapy crawl orpi

# On lance l'application
RUN python3 run.py