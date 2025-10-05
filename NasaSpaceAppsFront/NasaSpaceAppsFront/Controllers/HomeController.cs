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

        public async Task<IActionResult> busc(string search)
        {
            var articulo =await  _apiConnector.EntradaDeArticulo(search);
            var modelDto = await _apiConnector.ArticuloCreator(articulo);
            var entrada = new ArticuloFinal
            {
                descripcion = modelDto.descripcion,
                link = modelDto.url,
                titulo = modelDto.titulo
            };

           var model1 = await _apiConnector.ArticuloResumen(entrada);
            var model = new ArticuloModelFinal
            {
                titulo = model1.titulo,
                desarrollo = modelDto.descripcion,
                conclusion_implicaciones = model1.conclusion_implicaciones,
                hallazgos_clave = model1.hallazgos_clave,
                introduccion_contexto = model1.introduccion_contexto,
                url = articulo.url

            };

            return View(model);
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

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
