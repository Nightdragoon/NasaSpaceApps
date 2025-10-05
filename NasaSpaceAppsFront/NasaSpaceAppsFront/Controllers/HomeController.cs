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


        [HttpGet]
        public async Task<IActionResult> busc(string search , bool ciego)
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
                url = articulo.url,
                DatosCuriosos = [
  "Human DNA can survive in space for over a year if protected from the Sun.",
  "Tardigrades survived the vacuum of space, and some even reproduced after returning to Earth.",
  "Plants change their shape in space; some grow in spirals due to the lack of gravity.",
  "Astronauts’ brains physically reorganize in microgravity, altering their structure.",
  "Certain bacteria on the International Space Station developed antibiotic resistance in less than 30 days.",
  "NASA successfully grew flowers in space with larger petals than on Earth.",
  "Yeast grown in space produced more antioxidants than on Earth.",
  "Mice sent into space showed signs of cellular rejuvenation.",
  "Solar radiation can erase DNA, which is why researchers study melanin coatings as protection.",
  "Astronauts say that space smells like hot metal and seared meat.",
  "Astronaut Scott Kelly returned from space with over 500 genes expressing differently than his twin brother.",
  "DNA can travel between planets inside meteorites, supporting the panspermia theory.",
  "Frozen bacteria that survived millions of years suggest life could endure on Mars.",
   "The human metabolism slows down in space, reducing calorie consumption.",
  "Lunar dust can destroy human lung cells due to its sharp microscopic structure.",
  "Many astronauts experience worsened vision in space due to fluid pressure on the optic nerve.",
  "Gut bacteria composition changes during space missions.",
  "Some bacteria grow faster on spacecraft metal surfaces than in laboratory conditions.",
  "Chernobyl fungi can absorb cosmic radiation and convert it into energy.",
  "Plants can orient toward light without gravity using internal chemical sensors.",
  "Mouse sperm stored in space for six years still successfully fertilized eggs.",
  "Bones lose calcium 12 times faster in microgravity than on Earth.",
  "Scientists plan to study human embryo development in microgravity.",
  "Proteins change their structure in space, helping design more stable medicines.",
  "Astronauts experience 'space brain,' a temporary disorientation and memory alteration.",
  "Plants may communicate better in microgravity thanks to evenly distributed gases.",
  "The International Space Station has its own microbiome that evolves over time.",
  "Some bacteria survive attached to the outside of spacecraft, enduring extreme temperatures and vacuum.",
  "Water forms floating spheres in space, changing how astronauts drink and clean.",
  "Space biology could help terraform Mars using microbes that produce oxygen."
]




            };
            ViewBag.ciego = ciego;
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
