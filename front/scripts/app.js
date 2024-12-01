document.addEventListener("DOMContentLoaded", async () => {
    const optionsContainer = document.getElementById("optionsContainer");
    const recipeForm = document.getElementById("recipeForm");
    const recipeResult = document.getElementById("recipeResult");
    const getLocationButton = document.getElementById("getLocationButton");
    const storeList = document.getElementById("storeList");

    // Add Recipe Query Button
    const recipeQueryButton = document.createElement("button");
    recipeQueryButton.id = "recipeQueryButton";
    recipeQueryButton.textContent = "레시피 조회";
    document.body.appendChild(recipeQueryButton);

    // Recipe Query Button Click Event
    recipeQueryButton.addEventListener("click", async () => {
        console.log("Fetching recipes...");
        const recipeData = await fetchRecipeData();
        console.log("Recipe data fetched:", recipeData);

        if (recipeData.length > 0) {
            displayRecipeResults(recipeData);
        } else {
            recipeResult.innerHTML = "<p>No recipes found.</p>";
        }
    });

    // Fetch recipe options and render UI
    const options = await fetchOptions();
    options.forEach((option) => {
        const div = document.createElement("div");
        div.classList.add("option-group");

        const label = document.createElement("label");
        label.textContent = option.display;

        const select = document.createElement("select");
        select.name = option.display;

        option.value.forEach((item) => {
            const opt = document.createElement("option");
            opt.value = item.value;
            opt.textContent = item.display;
            select.appendChild(opt);
        });

        div.appendChild(label);
        div.appendChild(select);
        optionsContainer.appendChild(div);
    });

    // Recipe Form Submission
    recipeForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const recipeName = document.getElementById("recipeName").value;
        const selectedOptions = Array.from(
            optionsContainer.querySelectorAll("select")
        ).map((select) => {
            const displayValue = select.options[select.selectedIndex].text;

            const valueMap = {
                "5000원": "5000",
                "8000원": "8000",
                "10000원": "10000",
                "세븐일레븐": "7ELEVEN",
                "GS25": "GS25",
                "CU": "CU",
                "상큼한 비타민": "vitamin",
                "에너지 넘치는 영양소": "nutritious",
                "건강한 저당": "healthy_low_sugar",
                "아삭한 식이섬유": "dietary_fiber",
                "균형 잡힌 식단": "balanced_diet",
                "가벼운 저칼로리": "low_calorie",
            };

            return {
                display: select.name,
                value: [{ display: displayValue, value: valueMap[displayValue] || displayValue }],
            };
        });

        const sortedOptions = [
            selectedOptions.find(option => option.display === "최대 금액 선택"),
            selectedOptions.find(option => option.display === "키워드"),
            selectedOptions.find(option => option.display === "편의점 선택"),
        ];

        const requestData = {
            recipe_name: recipeName,
            value: sortedOptions,
        };

        console.log("Request Data to Server:", requestData);

        const result = await generateRecipe(requestData);

        recipeResult.innerHTML = result.recipe_result.replace(/\n/g, '<br>');
    });

    // Location Button Event
    getLocationButton.addEventListener("click", () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    console.log("User location:", latitude, longitude);

                    const stores = await fetchNearbyStores(latitude, longitude);
                    console.log("Stores:", stores);

                    storeList.innerHTML = stores
                        .map(
                            (store) =>
                                `<li><strong>${store.store_name}</strong> - ${store.address}</li>`
                        )
                        .join("");
                },
                (error) => {
                    console.error("Error fetching location:", error);
                    alert("Unable to fetch your location. Please allow location access.");
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });
});

// Function to display recipe results
const displayRecipeResults = (data) => {
    const recipeResult = document.getElementById("recipeResult");
    recipeResult.innerHTML = data.map(recipe => `
        <div class="recipe">
            <h3>${recipe.recipe_name}</h3>
            <p>${recipe.description.replace(/\n/g, '<br>')}</p>
            <p><strong>Price:</strong> ${recipe.price_name}</p>
            <p><strong>Keyword:</strong> ${recipe.keyword_name}</p>
            <p><strong>Convenience Store:</strong> ${recipe.cstore_name}</p>
        </div>
    `).join("");
};
