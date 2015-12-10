using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MyYelp.Properties;
using MongoDB.Driver;
using MyYelp.Business;
using MyYelp.TopBusinesses;
using MyYelp.BusinessesStructure;

namespace MyYelp.App_Start
{
    public class DBContext
    {
        public MongoDatabase Database;
        public MongoDatabase StatsDatabase;
        public DBContext()
        {
            var client = new MongoClient(Settings.Default.ConnectionStringMongo);
            var server = client.GetServer();
            Database = server.GetDatabase(Settings.Default.DatabaseName);
            StatsDatabase = server.GetDatabase(Settings.Default.DatabaseNameStats);
        }

        public MongoCollection<Business.Business> business  {
            get
            {
                return  Database.GetCollection<Business.Business>("business");
            }
        }

        public MongoCollection<TopBusinesses.TopBusiness> topBusiness
        {
            get
            {
                return StatsDatabase.GetCollection<TopBusinesses.TopBusiness>("topBusinessPerUserDuplicate");
            }
        }

        public MongoCollection<TopBusinessStructure> topBusinessStructure
        {
            get
            {
                return Database.GetCollection<TopBusinessStructure>("reviews");
            }
        }

    }
}