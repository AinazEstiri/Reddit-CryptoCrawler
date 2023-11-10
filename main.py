# export FLASK_APP=main
# flask run -h 0.0.0.0 -p 8888

from searchEngine import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
