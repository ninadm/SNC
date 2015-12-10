using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using MyYelp.App_Start;
using MongoDB.Driver.Builders;
using MyYelp.Business;
using System.Net.Http;
using System.Net.Http.Headers;
using Newtonsoft.Json.Linq;

namespace MyYelp.Controllers
{
    public class BusinessController : Controller
    {
        public readonly DBContext Context = new DBContext();
        // GET: Business
        public ActionResult Index()
        {
            var business = Context.business.FindAllAs<Business.Business>().SetFields(Fields.Exclude("attributes", "hours", "open"));
            business.SetLimit(10);
            return View(business);
        }

        
        public ActionResult SolrResults(string param)
        {
            param = param.Replace(" ", "+");
            string URL = "http://localhost:8080/solr/yelp/select?q=" + param + "&indent=true&wt=json";
            HttpClient client = new HttpClient();
            //client.BaseAddress = new Uri(URL);

            // Add an Accept header for JSON format.
            client.DefaultRequestHeaders.Accept.Add(
            new MediaTypeWithQualityHeaderValue("application/json"));

            HttpResponseMessage response = client.GetAsync(URL).Result;  // Blocking call!
                var json = JObject.Parse(response.Content.ReadAsStringAsync().Result);
                Console.WriteLine("{0} ({1})", (int)response.StatusCode, response.ReasonPhrase);
            ViewData["docs"] = json.Last.Last.Last;
            return Json(json.Last.Last.Last.Last.ToString(), JsonRequestBehavior.AllowGet);
        }

        public ActionResult FetchResultsOnUserId(string param)
        {
            var query = Query.EQ("user_id", param);
            var topBusiness = Context.topBusiness.FindOne(query);
            List<Business.Business> list = new List<Business.Business>();
            foreach(var a in topBusiness.business)
            {
                var q = Query.EQ("business_id", a);
                var business = Context.business.Find(q).SetFields(Fields.Exclude("attributes", "hours", "open")).SetLimit(1);
                foreach(var b in business)
                {
                    list.Add(b);
                }
            }
            return Json(list, JsonRequestBehavior.AllowGet);
        }
    }
}