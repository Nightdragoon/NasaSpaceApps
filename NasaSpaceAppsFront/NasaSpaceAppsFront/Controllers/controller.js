document.getElementById('searchBtn').addEventListener('click', function () {
  const query = document.getElementById('searchInput').value.trim();

  if (query === "") {
    alert("Please enter a search term.");
    return;
  }

  // Cargar datos del modelo (simulado)
  fetch('../model/data.json')
    .then(res => res.json())
    .then(data => {
      const results = data.filter(item =>
        item.title.toLowerCase().includes(query.toLowerCase())
      );
      console.log("Resultados:", results);
      alert(results.length ? "Resultados encontrados en consola" : "Sin coincidencias");
    })
    .catch(err => console.error("Error al cargar el modelo:", err));
});
