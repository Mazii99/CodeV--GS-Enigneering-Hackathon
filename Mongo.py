from pymongo import MongoClient


def getDatabase():
    CONNECTION_STRING = "mongodb+srv://hackaton:eH52VkeWNSHgMdH@cluster0.nzxqt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    connection = MongoClient(CONNECTION_STRING)
    db = connection["hackathon"]
    return db