from pymongo import MongoClient

def conexionDB():
    uri = "mongodb+srv://Angel1421:OuJK8fpTQzR0vgS8@cluster0.ypcdxhl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    db = client["Syra"]
    return db

