__author__ = 'Ninad'

##
# Code To calculate Similarity Values for all users and storing in database.
##
import json
import sys
import numpy as np
from pymongo import MongoClient
from sklearn.cluster import KMeans
from itertools import groupby

import matplotlib.pyplot as plt


client = MongoClient()
database = client.yelp
databaseStats = client.yelpStats
statsSimilarUsers = databaseStats.similarUsers
reviewsCollection = database.reviews
businessCollection = database.business
userCollection = database.users


class OverallStats:
    kMeansUserCluster = {}
    totalNumberOfUsers = userCollection.count()
    friendDistribution = {}
    similarityScoreDistribution = {}
    averageFriendsPerUser = 0

    def calculateOverallStats(self):
        allUsers = userCollection.find()
        totalFriendsAllUsersHave = 0
        for user in allUsers:
            totalFriendsAllUsersHave += len(user["friends"])
        self.averageFriendsPerUser = totalFriendsAllUsersHave / self.totalNumberOfUsers

    def caluserStats(self):
        allUsers = userCollection.find()
        for user in allUsers:
            scoreForUser = ((user["review_count"] * user["average_stars"] * 5) + (sum(user["compliments"].values()) * 2) +
                            (user["fans"] * 3)) / 3
            self.similarityScoreDistribution[user["user_id"]] = scoreForUser

        # Normalization between 0 to 100
        minOriginal = min(self.similarityScoreDistribution.values())
        dividingFactor = max(self.similarityScoreDistribution.values()) - minOriginal
        for key, value in self.similarityScoreDistribution.items():
            newScore = (value - minOriginal) / dividingFactor
            self.similarityScoreDistribution[key] = newScore * 100
        arr = [float(v) for v in self.similarityScoreDistribution.values()]
        # K means
        a = [[b] for b in arr]  # K means needs list of list as input
        k_means = KMeans(n_clusters=428)
        km = k_means.fit(a)
        self.clusterSimilarUsers(km.labels_, self.similarityScoreDistribution.keys())

    def printDistribution(self):
        for key, value in self.kMeansUserCluster.items():
            print("Value similarity score " + str(self.similarityScoreDistribution[key]))

    def clusterSimilarUsers(self, labels, users):
        dictionary = dict(zip(users, labels))
        uniqueLabels = set(labels)
        for key in uniqueLabels:
            self.kMeansUserCluster[str(key)] = []
        for key, value in dictionary.items():
            self.kMeansUserCluster[str(value)].append(key)

    def insertInMongoDb(self):
        self.calculateOverallStats()
        statsSimilarUsers.delete_many({})
        statsSimilarUsers.insert_one({"averageFriendsPerUser": self.averageFriendsPerUser})
        for k,v in ustats.kMeansUserCluster.items():
            statsSimilarUsers.insert_one({k : v})

ustats = OverallStats()
ustats.caluserStats()
ustats.insertInMongoDb()




