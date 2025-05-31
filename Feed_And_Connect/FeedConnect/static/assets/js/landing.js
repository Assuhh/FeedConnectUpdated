function showSection(sectionId) {
    // First, hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show the selected section
    const activeSection = document.getElementById(sectionId);
    activeSection.classList.add('active');
}

const breedData = {
    dog: {
        "Labrador Retriever": {
            idealCBMImin: 65,
            idealCBMImax: 75,
            food: {
                underweight: { name: "Purina Pro Plan Sport", gramsPerDay: 350 },
                normal: { name: "Royal Canin Labrador Retriever Adult", gramsPerDay: 300 },
                overweight: { name: "Hill's Science Diet Perfect Weight", gramsPerDay: 250 }
            }
        },
        "Golden Retriever": {
            idealCBMImin: 65,
            idealCBMImax: 75,
            food: {
                underweight: { name: "Purina ONE High Protein", gramsPerDay: 340 },
                normal: { name: "Purina Pro Plan Large Breed", gramsPerDay: 310 },
                overweight: { name: "Hill’s Science Diet Light", gramsPerDay: 270 }
            }
        },
        "Beagle": {
            idealCBMImin: 20,
            idealCBMImax: 26,
            food: {
                underweight: { name: "Iams Minichunks", gramsPerDay: 240 },
                normal: { name: "Iams ProActive Health Small to Medium Breed", gramsPerDay: 200 },
                overweight: { name: "Hill's Science Diet Perfect Weight Small & Mini", gramsPerDay: 170 }
            }
        },
        "Pomeranian": {
            idealCBMImin: 28,
            idealCBMImax: 35,
            food: {
                underweight: { name: "Royal Canin Small Puppy", gramsPerDay: 150 },
                normal: { name: "Wellness CORE Small Breed", gramsPerDay: 130 },
                overweight: { name: "Hill's Science Diet Adult Light Small Bites", gramsPerDay: 110 }
            }
        },
        "Dachshund": {
            idealCBMImin: 22,
            idealCBMImax: 28,
            food: {
                underweight: { name: "Purina Pro Plan Small Breed", gramsPerDay: 220 },
                normal: { name: "Royal Canin Dachshund Adult", gramsPerDay: 200 },
                overweight: { name: "Hill's Science Diet Weight Management", gramsPerDay: 170 }
            }
        },
        "Siberian Husky": {
            idealCBMImin: 25,
            idealCBMImax: 33,
            food: {
                underweight: { name: "Blue Buffalo Wilderness High Protein", gramsPerDay: 360 },
                normal: { name: "Taste of the Wild Pacific Stream", gramsPerDay: 320 },
                overweight: { name: "Nutro Ultra Weight Management", gramsPerDay: 280 }
            }
        }
    },
    cat: {
        "Siamese": {
            min: 14, max: 18,
            food: {
                underweight: { name: "Royal Canin Kitten", gramsPerDay: 90 },
                normal: { name: "Royal Canin Siamese Adult", gramsPerDay: 70 },
                overweight: { name: "Hill’s Science Diet Perfect Weight Cat", gramsPerDay: 60 }
            }
        },
        "Maine Coon": {
            min: 15, max: 20,
            food: {
                underweight: { name: "Purina Pro Plan True Nature", gramsPerDay: 100 },
                normal: { name: "Royal Canin Maine Coon Adult", gramsPerDay: 95 },
                overweight: { name: "Hill’s Science Diet Light", gramsPerDay: 80 }
            }
        },
        "Bengal": {
            min: 14, max: 19,
            food: {
                underweight: { name: "Blue Buffalo Wilderness High Protein", gramsPerDay: 85 },
                normal: { name: "Hill's Science Diet Adult Chicken", gramsPerDay: 75 },
                overweight: { name: "Purina ONE Indoor Advantage", gramsPerDay: 65 }
            }
        },
        "Norwegian Forest Cat": {
            min: 16, max: 22,
            food: {
                underweight: { name: "Blue Buffalo Wilderness Indoor", gramsPerDay: 100 },
                normal: { name: "Royal Canin Indoor Long Hair", gramsPerDay: 90 },
                overweight: { name: "Hill's Science Diet Adult Light", gramsPerDay: 75 }
            }
        },
        "Russian Blue": {
            min: 14, max: 19,
            food: {
                underweight: { name: "Nutro Wholesome Essentials", gramsPerDay: 85 },
                normal: { name: "Hill's Science Diet Adult Chicken", gramsPerDay: 75 },
                overweight: { name: "Purina ONE Indoor Advantage", gramsPerDay: 65 }
            }
        },
        "Oriental Shorthair": {
            min: 13, max: 18,
            food: {
                underweight: { name: "Wellness CORE High Protein", gramsPerDay: 80 },
                normal: { name: "Royal Canin Indoor Adult", gramsPerDay: 70 },
                overweight: { name: "Iams Indoor Weight & Hairball", gramsPerDay: 60 }
            }
        }
    }
};

function toggleHeightField() {
    const petType = document.getElementById("pet").value;
    document.getElementById("height-container").style.display = petType === "dog" ? "block" : "none";
    document.getElementById("length-container").style.display = petType === "cat" ? "block" : "none";
}

function updateBreeds() {
    const petType = document.getElementById("pet").value;
    const breedSelect = document.getElementById("breed");
    breedSelect.innerHTML = "";

    Object.keys(breedData[petType]).forEach(breed => {
        const option = document.createElement("option");
        option.value = breed;
        option.textContent = breed;
        breedSelect.appendChild(option);
    });
}

function calculateBMI() {
    const petType = document.getElementById("pet").value;
    const breed = document.getElementById("breed").value;
    const weight = parseFloat(document.getElementById("weight").value);
    const length = parseFloat(document.getElementById("length").value); // for cat
    const height = parseFloat(document.getElementById("height").value); // for dog
    const resultText = document.getElementById("result");
    const foodText = document.getElementById("food-recommendation");

    if (!weight || (petType === "cat" && !length) || (petType === "dog" && !height)) {
        resultText.textContent = "Please enter valid weight and length/height.";
        foodText.textContent = "";
        return;
    }

    // Make sure height for dogs is within reasonable range (e.g., between 0.2m and 1m)
    if (petType === "dog" && (height < 0.2 || height > 1)) {
        resultText.textContent = "Please enter a valid height for dogs (between 0.2m and 1m).";
        foodText.textContent = "";
        return;
    }

    let cbmi = 0;
    let status = '';
    let foodPlan = {};

    if (petType === "dog") {
        cbmi = weight / (height ** 1.33); 

        console.log("Height:", height);
        console.log("Weight:", weight);
        console.log("CBMI:", cbmi);
    
        const breedInfo = breedData.dog[breed];
    
        if (cbmi < breedInfo.idealCBMImin) {
            status = "Underweight";
            foodPlan = breedInfo.food.underweight;
        } else if (cbmi > breedInfo.idealCBMImax) {
            status = "Overweight";
            foodPlan = breedInfo.food.overweight;
        } else {
            status = "Healthy Weight";
            foodPlan = breedInfo.food.normal;
        }
    
        resultText.innerHTML = `
            🐾 Breed: ${breed}<br>
            ⚖️ Actual Weight: ${weight} kg<br>
            📏 Height: ${height} m<br>
            💡 CBMI: ${cbmi.toFixed(2)}<br>
            📊 Status: <strong>${status}</strong>
        `;
    
    } else if (petType === "cat") {
        // For cats, calculate CBMI using the formula: weight / (length * length)
        cbmi = weight / (length * length);

        const breedInfo = breedData.cat[breed];

        if (cbmi < breedInfo.min) {
            status = "Underweight";
            foodPlan = breedInfo.food.underweight;
        } else if (cbmi > breedInfo.max) {
            status = "Overweight";
            foodPlan = breedInfo.food.overweight;
        } else {
            status = "Healthy Weight";
            foodPlan = breedInfo.food.normal;
        }

        resultText.innerHTML = `
            🐾 Breed: ${breed}<br>
            ⚖️ Actual Weight: ${weight} kg<br>
            📏 Body Length: ${length} m<br>
            💡 CBMI: ${cbmi.toFixed(2)}<br>
            📊 Status: <strong>${status}</strong>
        `;
    }

    foodText.innerHTML = `
        
        🍽️ <strong>Recommended Daily Amount:</strong> ${foodPlan.gramsPerDay}g per day
    `;
}

document.getElementById("pet").addEventListener("change", () => {
    updateBreeds();
    toggleHeightField();
});

window.onload = () => {
    updateBreeds();
    toggleHeightField();
};

function showSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');

    document.getElementById(sectionId).style.display = 'block';

    const imageDiv = document.getElementById('default-image');
    if (sectionId === 'bmi') {
        imageDiv.style.display = 'none';
    } else {
        imageDiv.style.display = 'block';
    }
}
