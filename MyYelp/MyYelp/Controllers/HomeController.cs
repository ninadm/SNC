using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using MyYelp.App_Start;

namespace MyYelp.Controllers
{
    public class HomeController : Controller
    {
        public DBContext Context = new DBContext();
        public ActionResult Index()
        {
            Context.Database.GetStats();
            return Json(Context.Database.Server.BuildInfo, JsonRequestBehavior.AllowGet);
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}