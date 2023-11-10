from flask import Blueprint, render_template, request, redirect, url_for, session

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        qsearch = request.form.get('searchQuery')
        if qsearch:
            session['query'] = qsearch
            print(qsearch.split())
            return redirect(url_for('display.results'))
    return render_template("home.html")
