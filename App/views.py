from flask import render_template, redirect, request
from App.forms import SearchForm


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
                if 0 < form.price_low.data < form.price_high.data and 0 < form.area_low.data < form.area_high.data and \
                                form.room_number.data > 0:
                    return redirect('/app/result/pl={}&ph={}&sl={}&sh={}&rn={}'.format(form.price_low.data,
                                                                                       form.price_high.data,
                                                                                       form.area_low.data,
                                                                                       form.area_high.data,
                                                                                       form.room_number.data))
                else:
                    return render_template('app_form.html', form=form, error=True)
            else:
                return render_template('app_form.html', form=form, error=False)
        else:
            return render_template('show_results.html')


    @app.route('/app/result/pl=<int:price_low>&ph=<int:price_high>&sl=<int:surface_low>&sh=<int:surface_high>&rn=<int:room_num>')
    def success(price_low=None, price_high=None, surface_low=None, surface_high=None, room_num=None):
        print("{} {} {} {} {}".format(price_low, price_high, surface_low, surface_high, room_num))
        return render_template('form_result.html')

    @app.route('/app/annonce/<string:annonce>')
    def disp_annonce(annonce: str=None):
        return render_template('show_annonce.html', annonce=annonce)
