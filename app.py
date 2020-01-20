from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/from/<direction>/')
def start_from(direction):

    mylist = ["Capicola","Celery Root","Marjoram - Dried, Rubbed", \
              "Bread - Italian Sesame Poly","Cheese - Bocconcini","Mushroom - Shitake, Dry","French Pastry - Mini Chocolate"]
    if direction == '1':
        return render_template("test_extend.html", direction=direction, user=False, mylist=mylist)
    return render_template("direction.html", direction=direction, user=False, mylist=mylist)


@app.route('/tours/<int:id>/')
def tours(id):
    return render_template("tour.html",id=id)


app.run(debug=True)
