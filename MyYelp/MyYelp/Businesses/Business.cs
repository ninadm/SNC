using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace MyYelp.Business
{
    public class Business
    {
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }
        public string name { get; set; }
        public int numberOfReviews { get; set; }
        public string business_id { get; set; }
        public string full_address { get; set; }
        //[BsonRepresentation(BsonType.Document)]
        //public string hours { get; set; }
        public string open { get; set; }
        public string[] categories { get; set; }
        public string city { get; set; }
        [BsonRepresentation(BsonType.Double)]
        public decimal review_count { get; set; }
        public string[] neighborhoods { get; set; }
        [BsonRepresentation(BsonType.Double)]
        public decimal latitude { get; set; }
        [BsonRepresentation(BsonType.Double)]
        public decimal longitude { get; set; }
        //[BsonRepresentation(BsonType.Document)]
        //public string attributes { get; set; }
        [BsonRepresentation(BsonType.Double)]
        public decimal stars { get; set; }
        public string type { get; set; }
        public string state { get; set; }

    }
}