using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using NasaSpaceAppsFront.Models;
using NasaSpaceAppsFront.Repositorios;

namespace NasaSpaceAppsFront.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IApiConnector _apiConnector;


        public HomeController(ILogger<HomeController> logger , IApiConnector apiConnector)
        {
            _logger = logger;
            _apiConnector = apiConnector;
        }

        public IActionResult Index(int? id)
        {
            ViewBag.id = id;
            return View();
        }
        public async Task<IActionResult> Historial(int id)
        {
            var historial = await _apiConnector.getHistorial(id);
            return View(historial);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        public async Task<IActionResult> login()
        {
            return View();
        }
        public async Task<IActionResult> singUp()
        {
            return View();
        }
        public async Task<IActionResult> busc()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
