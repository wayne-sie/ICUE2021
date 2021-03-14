from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://sanjeev2001:mEm39dShwBgbf2@cluster0.w43vk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["customer"]
history = db["history"]
print(history[0])