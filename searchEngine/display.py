from flask import Blueprint, render_template, request, redirect, url_for, session
from searchEngine import retrieve

display = Blueprint('display', __name__)

@display.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        query = session.get('query')
        print("session stuff: ")
        print(query)
        documents = retrieve('sample_lucene_index/', query)
        print(documents)
    else:
        qsearch = request.form.get('searchQuery')
        if not qsearch:
            return redirect(url_for('views.home'))
        else:
            session['query'] = qsearch
            print(qsearch.split())
            return redirect(url_for('display.results'))
    return render_template("results.html", documents=documents, query=query)
