using System.Text.Json.Serialization;

namespace NasaSpaceAppsFront.Repositorios
{
    public interface IApiConnector
    {
        Task<HistorialModel> getHistorial(int id);
    }

    public class ApiConnector : IApiConnector
    {
        public async Task<HistorialModel> getHistorial(int id)
        {
            var client = new HttpClient();
            var request = new HttpRequestMessage(HttpMethod.Get, "http://127.0.0.1:8000/historial?id=" + id.ToString());
            request.Headers.Add("accept", "application/json");
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
            var res = await response.Content.ReadFromJsonAsync<HistorialModel>();
            return res;
        }
    }
}
