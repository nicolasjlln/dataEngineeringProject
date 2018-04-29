FROM ubuntu:latest

# Update Ubuntu et installation python3
RUN apt-get update -y
RUN apt-get install python3
RUN apt-get install python3-pip

# Installation de l'environnement virtuel python3
RUN apt-get install virtualenv
# On se place dans l'environnement virtuel
RUN virtualenv venv
RUN . venv/bin/activate

# Copie de tous les fichiers dans le conteneur
COPY . .

# Installation des paquets python3 utiles à l'application
RUN pip3 install -r requirements.txt

# Demarrage du service mongo + scrapping
RUN sudo service mongod
RUN scrapy crawl orpi

# On lance l'application
RUN python run.py