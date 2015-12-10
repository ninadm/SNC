using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace MyYelp.TopBusinesses
{
    public class TopBusiness
    {
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }

        public string[] business { get; set; }

        public string user_id { get; set; }
    }
}