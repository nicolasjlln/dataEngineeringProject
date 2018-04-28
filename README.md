# Data Engineering Project
Scrapping et stockage sur base MongoDB d'un site de vente immobilière

The Data Engineering project is a school project done during the 4th year of engineering school at ESIEE Paris.</br>
The aim of this project is to scrap and store data from a website. Then, the goal is to permit the data access trough a local web portal. In this project, we had to scrap, store and make accecible data from a real estate website, called [ORPI](https://www.orpi.com/?utm_source=bing&utm_medium=cpc&msclkid=26b36418dde91e469c873efcb7e2f34b&gclid=CMnUhJn93NoCFUbNGQodJqcEVA&gclsrc=ds "ORPI website").

## Getting Started

The project is runnable via a docker container.</br>
That's all.

The instructions below are destined to a Linux based usage. This doesn't mean the project won't work on another environment, but the instructions to do so aren't displayed here.

### Prerequisites

* This library is __built with Python 3__.

> If you do not have Python 3 on your computer, to install it with linux is :
```
$ sudo apt-get update
$ sudo apt-get install python3.6
```
(or follow this [link](http://docs.python-guide.org/en/latest/starting/install3/linux/ "Python 3 installation"))

* Make sure you have __docker__ on your computer.

> To install Docker with pip (Python 3) :
```
$ pip3 install docker
```

### Installing

* You must clone the git dir or download it on your computer.
```
$ git clone https://gitlab.com/charleswit/GuessMyAddress.git
```

* Using Docker, you have to build the Docker image with :
```
$ docker build -t [name of the image] .
$ docker run -it [name of the image]
```
> **If you need a Docker tutorial and/or explore its possibilities, go to [this link](https://docker-curriculum.com/ "Docker tutorial")

* Once you are in the docker image with the '**docker run**' command, the required libraries should have been installed and our application is ready to be used !
To access the web portal, you will have to open a browser, and go to this link :
```
http://127.0.0.1:5000
```

## How it works

The basic use of GuessMyAddress lies in building the GuessMyAddress object with a Python dictionary.
This dictionary contains information about a property advertisement.

The informations give by the ad can be collected by scrapping. The following dictionary is an example of the informations that are required :
```
ADD_DICT = {
    'city': 'Paris',
    'cp': 75010,
    'desc': "A l'angle de la Rue des Vinaigriers et du Faubourg Saint-Martin Paris Immobilier vous propose un espace de "
            "122m2 donnant sur rue et cour. Parquet au sol, fenêtre double vitrage , chauffage électrique, coin cuisine "
            "et toilettes séparés."
            "La partie habitation correspond a peu près à 50% de l'espace."
            "Beau volume. Bureaux en très bon état."
            "Gros Travaux de copropriété Votés (ravalement de la cour, toiture et pignons) Le ravalement rue est récent.",
    'prix': 965000.00,
    'etage': None,
    'pieces': 2,
    'dep': 75,
    'surface': 122
}
```

Once the dictionary is built, create the GuessMyAddress project with it !
```
>>> from GuessMyAddress import GuessMyAddress

>>> gma = GuessMyAddress(ADD_DICT)
```

### Main use

To run the prediction and get the potential candidate addresses, simply use *.predict()* method as following :
```
>>> gma.predict()
```

### Side functions

If you want to decompose the algorithm, you can use the different object methods :

* To check if there is a valid address in the ad. This method returns the eventual valid addresses as a Pandas dataframe :
```
>>> gma.addresses()
```

* To check if there are points of interest in the ad's description. The detected PoI's are returned as a list of dictionaries :
```
>>> gma.get_pois()
```

* To geocode and identify potential addresses according to PoI's isochrone perimeters :
```
>>> gma.candidates_poi()
```

* To check if there are features (like floor number, presence of a lift, a parking...) in the ad's description. They are returned as dictionary :
```
>>> gma.get_features()
```

* To try to score a probability for each candidate address depending on it's features
```
>>> gma.score()
```

## Built With

* [Shapely](http://toblerity.org/shapely/manual.html) - The library for geometry
* [GDAL](https://trac.osgeo.org/gdal/wiki/GdalOgrInPython) - Help to handle huge geojsons
* [SpaCy](https://spacy.io/) - Natural language processing library
* [Folium](https://github.com/python-visualization/folium) - Used to generate maps
* [Geocoder](https://geocoder.readthedocs.io/) - Google geocoder for reverse-geocoding
* [Pymysql](https://github.com/PyMySQL/PyMySQL) - Used to connect databases
* [NLTK](http://www.nltk.org/) - Natural language toolkit

## Authors

* **Nicolas JULLIEN** - [nicouilla](https://gitlab.com/nicouilla)
* **Salahedin ABDELKRIM** - [salah7594](https://gitlab.com/salah7594)
* **Vincent DECKER** - [VincentDecker](https://gitlab.com/VincentDecker)
* **Monica KOY** - [Koy](https://gitlab.com/Koy)
* **Morgan COURIVAUD** - [courivam](https://gitlab.com/courivam)
* **Charles MAUPOU** - [charleswit](https://gitlab.com/charleswit)

See also the list of [contributors](https://gitlab.com/charleswit/GuessMyAddress/contributors) who participated in this project.

## License

This project is licensed under the ESIEE Paris License.

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
