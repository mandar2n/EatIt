document.addEventListener("DOMContentLoaded", async () => {
    const optionsContainer = document.getElementById("optionsContainer");
    const recipeForm = document.getElementById("recipeForm");
    const recipeResult = document.getElementById("recipeResult");
    const getLocationButton = document.getElementById("getLocationButton");
    const storeList = document.getElementById("storeList");
  
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
  
    // Handle form submission for recipe generation
recipeForm.addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const recipeName = document.getElementById("recipeName").value;
    const selectedOptions = Array.from(
      optionsContainer.querySelectorAll("select")
    ).map((select) => {
      const displayValue = select.options[select.selectedIndex].text;
  
      // 매핑 예시 (필요한 경우 새로운 매핑 추가)
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
        "가벼운 저칼로리": "low_calorie"
      };
  
      return {
        display: select.name,
        value: [{ display: displayValue, value: valueMap[displayValue] || displayValue }],
      };
    });
  
    // 순서를 "최대 금액 선택", "키워드", "편의점 선택" 순으로 맞추기
    const sortedOptions = [
      selectedOptions.find(option => option.display === "최대 금액 선택"),
      selectedOptions.find(option => option.display === "키워드"),
      selectedOptions.find(option => option.display === "편의점 선택"),
    ];
  
    const requestData = {
      recipe_name: recipeName,
      value: sortedOptions,
    };
  
    console.log("Request Data to Server:", requestData); // 전송할 데이터 확인
  
    const result = await generateRecipe(requestData);
    recipeResult.textContent = result.recipe_result;
  });
  
  
  
    // Handle location button click for fetching nearby stores
    getLocationButton.addEventListener("click", () => {
      if ("geolocation" in navigator) {
        // 위치 정보 가져오기
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
  
            console.log("User location:", latitude, longitude);
  
            // Fetch nearby stores
            const stores = await fetchNearbyStores(latitude, longitude);
            console.log("Stores:", stores);
  
            // Display stores
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
  