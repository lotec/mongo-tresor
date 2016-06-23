import os

from flask import Flask, redirect, url_for, request, render_template
import pymongo

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

client = pymongo.MongoClient()
db = client['some_db']
collection = db['some_collection']


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'content': request.form['content'],
        'tags': request.form['tags']
    }
    collection.insert_one(item_doc)

    return redirect(url_for('base'))


@app.route('/search')
def search():
    return render_template('searchpage.html')


@app.route('/search_results', methods=['POST'])
def search_results():

    collection.create_index([('$**', 'text')])

    result = request.form['search']

    # findall = collection.find({"$text": {"$search": result}})

    findall = collection.find({'$text': {'$search': result}}, {'score': {'$meta': 'textScore'}}).sort([['score', {'$meta': 'textScore'}]])
    items = [item for item in findall]

    return render_template('searchpage.html', items=items)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)