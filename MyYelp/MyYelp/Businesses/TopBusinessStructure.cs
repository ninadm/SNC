using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace MyYelp.BusinessesStructure
{
    public class TopBusinessStructure
    {
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }
        public string name { get; set; }
        public int review_count { get; set; }

        [BsonRepresentation(BsonType.Double)]
        public Double stars { get; set; }
    }
}