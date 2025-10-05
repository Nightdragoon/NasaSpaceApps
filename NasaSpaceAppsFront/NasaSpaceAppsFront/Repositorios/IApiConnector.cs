using Microsoft.Extensions.Options;
using NasaSpaceAppsFront.Models;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace NasaSpaceAppsFront.Repositorios
{
    public interface IApiConnector
    {
        Task<HistorialModel> getHistorial(int id);
        Task<ArticuloEntradaModel> EntradaDeArticulo(string titulo);
        Task<ArticuloModel> ArticuloCreator(ArticuloEntradaModel entrada);

        Task<ArticuloViewModel> ArticuloResumen(ArticuloFinal entrada);

    }

    public class ApiConnector : IApiConnector
    {
        public async Task<ArticuloModel> ArticuloCreator(ArticuloEntradaModel entrada)
        {
            var client = new HttpClient();
            var request = new HttpRequestMessage(HttpMethod.Post, "https://nasaspaceappsstemfesc-3ad0bcb04512.herokuapp.com/descripcion");
            request.Headers.Add("accept", "application/json");
            request.Content = new StringContent(JsonSerializer.Serialize(entrada), Encoding.UTF8, "application/json"); ;
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            var res = await response.Content.ReadFromJsonAsync<ArticuloModel>();
            return res;

        }

        public async Task<ArticuloViewModel> ArticuloResumen(ArticuloFinal entrada)
        {
            var client = new HttpClient();
            var request = new HttpRequestMessage(HttpMethod.Post, "https://nasaspaceappsstemfesc-3ad0bcb04512.herokuapp.com/resumen");
            request.Headers.Add("accept", "application/json");
            var content = new StringContent(JsonSerializer.Serialize(entrada), null, "application/json");
            request.Content = content;
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            var res = await response.Content.ReadFromJsonAsync<ArticuloViewModel>();
            return res;

        }

        public async Task<ArticuloEntradaModel> EntradaDeArticulo(string titulo)
        {

            var client = new HttpClient();
            var request = new HttpRequestMessage(HttpMethod.Post, "https://nasaspaceappsstemfesc-3ad0bcb04512.herokuapp.com/busqueda");
            request.Headers.Add("accept", "application/json");
            var tit = new EntradaTitulo()
            {
                titulo = titulo
            };
            request.Content = new StringContent(JsonSerializer.Serialize(tit),Encoding.UTF8, "application/json"); 
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            var res = await response.Content.ReadFromJsonAsync<ArticuloEntradaModel>();
            return res;



        }

        public async Task<HistorialModel> getHistorial(int id)
        {
            var client = new HttpClient();
            var request = new HttpRequestMessage(HttpMethod.Get, "https://nasaspaceappsstemfesc-3ad0bcb04512.herokuapp.com/historial?id=" + id.ToString());
            request.Headers.Add("accept", "application/json");
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            var res = await response.Content.ReadFromJsonAsync<HistorialModel>();
            return res;
        }
    }
}
