from flask import render_template, redirect, request
from App.forms import SearchForm


def Main_views(app):
    @app.route('/')
    def welcome():
        return render_template('welcome.html')


    @app.route('/app', methods=['GET', 'POST'])
    def app_run():
        form = SearchForm(request.form)
        print(request.method)
        print(form.validate_on_submit())
        if request.method == 'POST' and form.validate_on_submit():
            return redirect('/app/success/pl={}&ph={}&sl={}&sh={}&rn={}'.format(str(form.price_low.data), form.price_high.data, form.area_low.data, form.area_high.data, form.room_number.data))
        return render_template('app.html', form=form)

    @app.route('/app/success/pl=<int:price_low>&ph=<int:price_high>&sl=<int:surface_low>&sh=<int:surface_high>&rn=<int:room_num>')
    def success(price_low=None, price_high=None, surface_low=None, surface_high=None, room_num=None):
        print("{} {} {} {} {}".format(price_low, price_high, surface_low, surface_high, room_num))
        return "Nice, buddy ! ;)"
