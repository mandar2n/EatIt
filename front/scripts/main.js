document.getElementById("searchButton").addEventListener("click", async () => {
    const location = document.getElementById("locationInput").value;
    const response = await fetch(`http://localhost:8000/location/store?location=${location}`);
    const stores = await response.json();
  
    const storeList = document.getElementById("storeList");
    storeList.innerHTML = stores.map(store => `<li>${store.name}</li>`).join('');
  });
  