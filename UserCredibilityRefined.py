__author__ = 'Ninad'
import json
import sys
import numpy as np
from pymongo import MongoClient
from sklearn.cluster import KMeans
from itertools import groupby

import matplotlib.pyplot as plt


client = MongoClient()
database = client.yelp
reviewsCollection = database.reviews
businessCollection = database.business
userCollection = database.users


class OverallStats:
    allUsers = userCollection.find()
    totalFriendsAllUsersHave = 0
    averageFriendsPerUser = 0
    averageNumberOfReviewsGivenByUser = 0
    totalNumberOfReviewsGiven = 0
    totalNumberOfUsers = userCollection.count()
    friendDistribution = {}
    similarityScoreDistribution = {}

    def calculateOverallStats(self):
        for user in self.allUsers.limit(20):
            self.totalFriendsAllUsersHave += len(user["friends"])
            self.totalNumberOfReviewsGiven += user["review_count"]
        self.averageFriendsPerUser = self.totalFriendsAllUsersHave / self.totalNumberOfUsers
        self.averageNumberOfReviewsGivenByUser = self.totalNumberOfReviewsGiven / self.totalNumberOfUsers

    def printStats(self):
        print("self.totalFriends " + str(self.totalFriendsAllUsersHave))
        print("self.totalNumberOfReviewsGiven " + str(self.totalNumberOfReviewsGiven))
        print("self.totalNumberOfUsers " + str(self.totalNumberOfUsers))
        print("self.averageNumberOfReviewsGivenByUser " + str(self.averageNumberOfReviewsGivenByUser))
        print("self.averageFriendsPerUser " + str(self.averageFriendsPerUser))

    def caluserStats(self):
        allUsers = userCollection.find()
        for user in allUsers:
            scoreForUser = ((user["review_count"] * user["average_stars"] * 5) + (sum(user["compliments"].values()) * 2) +
                            (user["fans"] * 3)) / 3
            self.friendDistribution[user["user_id"]] = len(user["friends"]) / self.averageFriendsPerUser
            self.similarityScoreDistribution[user["user_id"]] = scoreForUser

        minOriginal = min(self.similarityScoreDistribution.values())
        dividingFactor = max(self.similarityScoreDistribution.values()) - minOriginal
        for key, value in self.similarityScoreDistribution.items():
            newScore = (value - minOriginal) / dividingFactor
            # print(newScore)
            self.similarityScoreDistribution[key] = newScore * 100
        arr = [float(v) for v in self.similarityScoreDistribution.values()]
        # print(arr)
        a = [[b] for b in arr]
        # print(a)
        # print(np.mean(a))
        # print(np.median(a))
        arr = np.asarray(arr)
        # print(arr)
        k_means = KMeans(n_clusters=428)
        km = k_means.fit(a)
        # km = KMeans(self,2).fit(a, None)
        # print(km.labels_)
        plt.hist(km.labels_, bins=np.arange(km.labels_.min(), km.labels_.max()+1))
        plt.show()
        freq = [len(list(group)) for key, group in groupby(km.labels_)]
        # print(freq)

    def printUserFriendDistribution(self):
        for key, value in self.friendDistribution.items():
            # print("key " + key + " Friends deviation value :" + str(value))
            print("Value similarity score " + str(self.similarityScoreDistribution[key]))



ustats = OverallStats()
ustats.calculateOverallStats()
ustats.caluserStats()
# ustats.printUserFriendDistribution()
ustats.printStats()


