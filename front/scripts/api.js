const fetchOptions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/recipes/options");
      if (!response.ok) throw new Error("Failed to fetch options.");
      return await response.json();
    } catch (error) {
      console.error("Error fetching options:", error);
      return [];
    }
  };
  
  const generateRecipe = async (data) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/recipes/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error("Failed to generate recipe.");
      return await response.json();
    } catch (error) {
      console.error("Error generating recipe:", error);
      return { recipe_result: "Failed to generate recipe. Please try again." };
    }
  };
  
  const fetchNearbyStores = async (latitude, longitude) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/location/nearby_stores", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ latitude, longitude }),
      });
  
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error("Error fetching stores:", error);
      return [];
    }
  };
  