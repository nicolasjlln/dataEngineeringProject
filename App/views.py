from flask import render_template, redirect, request
from App.forms import SearchForm
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['orpi']

def getListAgencies():
    return db.agence.distinct('name_agence')

def getInfoAgence(name_agence):
    return db.agence.findOne({'name_agence': name_agence})

def getListAnnonces(nameAgence):
    return db.annonce.distinct('title_annonce',{'agence_annonce': 'www.orpi.com/gambetta/'})

def getInfoAnnonces(nameAnnonce):
    db.annonce.findOne({'title_annonce': nameAnnonce})

def Main_views(app):
    @app.route('/')
    def welcome():
        return render_template('welcome.html')


    @app.route('/app', methods=['GET', 'POST'])
    def app_run():
        print(request.method)
        if request.method == 'POST':
            form = SearchForm(request.form)
            if form.validate_on_submit():
                if (0 < form.price_low.data < form.price_high.data)\
                        and (0 < form.area_low.data < form.area_high.data)\
                        and (form.room_number.data > 0)\
                        and (form.type.data == 'a' or form.type.data == 'm') :
                    return redirect('/app/result/pl={}&ph={}&sl={}&sh={}&rn={}&ty={}'.format(form.price_low.data,
                                                                                       form.price_high.data,
                                                                                       form.area_low.data,
                                                                                       form.area_high.data,
                                                                                       form.room_number.data,
                                                                                       form.type.data))
                else:
                    return render_template('app_form.html', form=form, error=True)
            else:
                return render_template('app_form.html', form=form, error=False)
        else:
            agences_list = getListAgencies()
            return render_template('show_results.html', agences=agences_list)


    @app.route('/app/result/pl=<int:price_low>&ph=<int:price_high>&sl=<int:surface_low>&sh=<int:surface_high>&rn=<int:room_num>&ty=<string:type>')
    def success(price_low=None, price_high=None, surface_low=None, surface_high=None, room_num=None, type=None):
        print("{} {} {} {} {} {}".format(price_low, price_high, surface_low, surface_high, room_num, type))
        annonces = ["une annonce", "deux annonces", "trois annonces"]
        return render_template('form_result.html', annonces=annonces)

    @app.route('/app/annonce/<string:annonce>')
    def disp_annonce_infos(annonce: str=None):
        annonce = getInfoAnnonces(annonce)
        return render_template('show_annonce.html', annonce=annonce)

    @app.route('/app/agence/annonces/<string:nom_agence>')
    def disp_annonces_from_agence(nom_agence: str=None):
        annonces =  getListAnnonces(nom_agence)
        return render_template('show_annonces_from_agence.html', annonces=annonces, nom_agence=nom_agence)

    @app.route('/app/agence/infos/<string:nom_agence>')
    def disp_agence_infos(nom_agence: str=None):
        agence_infos = getInfoAgence(nom_agence)
        return render_template('show_agence.html', agence=agence_infos)
