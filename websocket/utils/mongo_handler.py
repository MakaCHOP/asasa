from pymongo import MongoClient

client = MongoClient("localhost", 27017)
space = client["space-x-bot"]
users = space["users"]