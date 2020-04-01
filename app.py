from flask import Flask, render_template
import os
import env
import pymongo

app = Flask(__name__)


MONGO_URI = os.environ.get("MONGO_URI")
DBS_NAME = "myTestDB"
COLLECTION_NAME = "movies"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]


@app.route("/")
def home():
    return render_template('hello.html')


@app.route("/create")
def create():
    my_wonderful_new_document = {'title': 'Jaws',
                                 'release_year': '1975',
                                 'synopsis': 'Another very relaxing movie about a fish'}

    coll.insert_one(my_wonderful_new_document)

    return render_template('create.html', document=my_wonderful_new_document)


@app.route("/read")
def read():
    documents = coll.find()
    return render_template('read.html', documents=documents)


if __name__ == '__main__':
    app.run(host='0.0.0.0',
    port=5000,
    debug=True)
