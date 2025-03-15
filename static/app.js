// app.js

document.addEventListener('DOMContentLoaded', function() {
  const searchButton = document.getElementById('searchButton');
  const searchInput = document.getElementById('searchInput');
  const resultContainer = document.getElementById('resultContainer');

  // Fonction pour envoyer la requête de recherche et afficher les résultats
  searchButton.addEventListener('click', function() {
    const query = searchInput.value.trim();
    if (query) {
      fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => {
          // Afficher les résultats
          if (data.length > 0) {
            resultContainer.innerHTML = '';
            data.forEach(item => {
              const resultElement = document.createElement('div');
              resultElement.classList.add('bg-gray-800', 'p-4', 'rounded-lg', 'my-2');
              resultElement.innerHTML = `
                <h3 class="text-xl text-white">${item.title}</h3>
                <p class="text-gray-400">${item.description}</p>
                <a href="/download/${item.id}" class="text-blue-500">Télécharger le PDF</a>
              `;
              resultContainer.appendChild(resultElement);
            });
          } else {
            resultContainer.innerHTML = '<p class="text-white">Aucun résultat trouvé.</p>';
          }
        })
        .catch(error => {
          console.error('Erreur de recherche:', error);
          resultContainer.innerHTML = '<p class="text-white">Erreur lors de la recherche.</p>';
        });
    } else {
      resultContainer.innerHTML = '<p class="text-white">Veuillez entrer un mot-clé.</p>';
    }
  });
});
