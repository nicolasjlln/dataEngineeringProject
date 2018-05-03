FROM ubuntu:latest

# Update Ubuntu et installation python3
RUN apt-get update -y && apt-get install -y python3 && apt-get install -y python3-pip

# Copie de tous les fichiers dans le conteneur
COPY . .

# Installation de l'environnement virtuel python3
RUN apt-get install -y python3-venv
# On créé et on se place dans l'environnement virtuel
RUN python3 -m venv venv
RUN . venv/bin/activate

# Installation des paquets python3 utiles à l'application
RUN pip3 install -r requirements.txt

# Installation et demarrage du service mongo
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN apt-get update -y

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install -y mongodb-org

RUN service mongod start

# Demarrage scrapping
# RUN scrapy crawl orpi

# On lance l'application
# RUN python3 run.py
