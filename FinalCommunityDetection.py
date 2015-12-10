

##
# Code to create graph based on friends and
##
import community # --> http://perso.crans.org/aynaud/communities/
import json
import networkx as nx
import random
import sys
import math
from pymongo import MongoClient

client = MongoClient()
database = client.yelp
databaseStats = client.yelpStats
statsSimilarUsers = databaseStats.similarUsers
reviewsCollection = database.reviews
businessCollection = database.business
userCollection = database.users
topBusinessPerUser = databaseStats.topBusinessPerUser
topBusinessPerUserDuplicate = databaseStats.topBusinessPerUserDuplicate

class CommunityDetection:
    MyYelpUserGraph = nx.Graph()
    partition = {}
    aggregateCommunities = {}

    def createFriendGraph(self):
        users = userCollection.find()
        for user in users:
            for friend in user["friends"]:
                self.MyYelpUserGraph.add_edge(user["user_id"], friend)

    def createClusterBasedGraph(self):
        averageFriendsPerUser = statsSimilarUsers.find()[0]["averageFriendsPerUser"]
        clusters = statsSimilarUsers.find().skip(1)
        users = userCollection.find()
        for user in users:
            if len(user["friends"]) < averageFriendsPerUser:
                numberOfUsersToFind = math.ceil(averageFriendsPerUser) - len(user["friends"])
                for cluster in clusters:
                    for key, value in cluster.items():
                        if key == "_id":
                            continue
                        if user["user_id"] in value:
                            if numberOfUsersToFind < len(value):
                                similarUsersFoundFromCluster = random.sample(value, numberOfUsersToFind)
                            else:
                                similarUsersFoundFromCluster = value
                            for similarUser in similarUsersFoundFromCluster:
                                self.MyYelpUserGraph.add_edge(user["user_id"], similarUser)

    def findCommunitiesFromGraph(self):
        self.partition = community.best_partition(self.MyYelpUserGraph)
        print("Louvain Modularity: ", community.modularity(self.partition, self.MyYelpUserGraph))
        print("My graph has " + str(self.MyYelpUserGraph.number_of_nodes()) + " nodes")
        print("My graph has " + str(self.MyYelpUserGraph.number_of_edges()) + " edges")

    def findAggregateCommunities(self):
        uniqueCommunityIndices = list(set([i for i in self.partition.values()]))
        print(uniqueCommunityIndices)
        for i in uniqueCommunityIndices:
            self.aggregateCommunities[i] = []
        for key, value in self.partition.items():
            self.aggregateCommunities[value].append(key)

    def findAverageBusinessStars(self):
        # topBusinessPerUserDuplicate.delete_many({})
        topBusinessPerUser.delete_many({})
        communityForUser = []
        users = userCollection.find().limit(10)
        dict = {}
        for outerUser in users:
            dict[outerUser["user_id"]] = []
            for key, comm in self.aggregateCommunities.items():
                if outerUser["user_id"] in comm:
                    communityForUser = comm
                    userBusiness = {}
                    for user in communityForUser:
                        reviewsForUser = reviewsCollection.find({"user_id": user}, {"business_id": True, "stars": True, "_id": False, "votes": True, "review_id": True}).limit(20)
                        for businessReviewed in reviewsForUser:
                            print("inside for 4")
                            userBusiness.setdefault(user,[]).append(businessReviewed)

                    businessStars = {}
                    for item in userBusiness:
                        for business in userBusiness[item]:
                            businessStars.setdefault(business["business_id"], []).append(float(business["stars"]))

                    averageStars = {}
                    for business in businessStars.items():
                        averageStars[business[0]] = sum(business[1]) / len(business[1])

                    sortedStars = ((k, averageStars[k]) for k in sorted(averageStars, key=averageStars.get, reverse=True))
                    for one_business in sortedStars:
                        if len(dict[outerUser["user_id"]]) < 10:
                            dict[outerUser["user_id"]].append(one_business[0])
                    print(dict)
            topBusinessPerUser.insert_one({"user_id" : outerUser["user_id"], "business" : dict[outerUser["user_id"]]})
            topBusinessPerUserDuplicate.insert_one({"user_id" : outerUser["user_id"], "business" : dict[outerUser["user_id"]]})

cd = CommunityDetection()
cd.createFriendGraph()
cd.createClusterBasedGraph()
cd.findCommunitiesFromGraph()
cd.findAggregateCommunities()
cd.findAverageBusinessStars()

