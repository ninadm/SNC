# SNC
Project For Social Networking Class
The project involves 2 python scripts for finding user similarity and community detection.

The community detection package that we used can be found on the link given below.
https://bitbucket.org/taynaud/python-louvain.

We used Yelp academic dataset as the base for creating our recommendation system.
https://www.yelp.com/academic_dataset

We first populate the MongoDb database using mongoexport command. A sample command is given below.
mongoimport --db yelp --collection users --file <your-file-path-for-user-jsons>

After the database is created we find useful statistics like average number of friends per user and find the user similarity score based on the reviews the users give, 
average stars given by the user, compliments the user has recieved and the number of fans a user has. We apply K means clustering to cluster similar users together.
After that we create a graph such that every user has atleast as many connections as that of the average friends statistic accross entire DB. 
We then apply and find communities based on this graph.

Based on the reviews given by users in a community we calculate the new average rating and find out the top 10 restaraunts per user and store them in the database.

The above 2 steps run as a part of a cron schedule. We schedule the 2 scripts to run one after the other once every 24 hours.

The website is just a mockup that fetches the top 10 restaraunts per user from the database according to the entered User Id and display the results. 
The website is created using ASP. Net MVC4, jQuery, and mongo C# driver.
