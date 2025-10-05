// Root myDeserializedClass = JsonConvert.DeserializeObject<Root>(myJsonResponse);
public class Historial
{
    public string titulo { get; set; }
    public string url { get; set; }
}

public class HistorialModel
{
    public List<Historial> historial { get; set; }
}

