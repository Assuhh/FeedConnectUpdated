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
                underweight: { name: "High Protein Dog Food", gramsPerDay: 350 },
                normal: { name: "Adult Dog Food", gramsPerDay: 300 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 250 }
            }
        },
        "Golden Retriever": {
            idealCBMImin: 65,
            idealCBMImax: 75,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 340 },
                normal: { name: "Adult Dog Food", gramsPerDay: 310 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 270 }
            }
        },
        "Beagle": {
            idealCBMImin: 20,
            idealCBMImax: 26,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 240 },
                normal: { name: "Small to Medium Breed Adult Food", gramsPerDay: 200 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 170 }
            }
        },
        "Pomeranian": {
            idealCBMImin: 28,
            idealCBMImax: 35,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 150 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 130 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 110 }
            }
        },
        "Dachshund": {
            idealCBMImin: 22,
            idealCBMImax: 28,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 220 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 200 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 170 }
            }
        },
        "Siberian Husky": {
            idealCBMImin: 25,
            idealCBMImax: 33,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 360 },
                normal: { name: "Adult Dog Food", gramsPerDay: 320 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 280 }
            }
        },
        "Aspin (Asong Pinoy)": {
            idealCBMImin: 30,
            idealCBMImax: 40,
            food: {
                underweight: { name: "Puppy Food", gramsPerDay: 180 },
                normal: { name: "Adult Dog Food", gramsPerDay: 150 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 120 }
            }
        },
        "Shih Tzu": {
            idealCBMImin: 22,
            idealCBMImax: 28,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 160 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 140 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 110 }
            }
        },
        "Philippine Kintamani": {
            idealCBMImin: 45,
            idealCBMImax: 55,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 300 },
                normal: { name: "Adult Dog Food", gramsPerDay: 270 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 230 }
            }
        },
        "Bulldog": {
            idealCBMImin: 50,
            idealCBMImax: 60,
            food: {
                underweight: { name: "Large Breed Puppy Food", gramsPerDay: 320 },
                normal: { name: "Adult Dog Food", gramsPerDay: 280 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 240 }
            }
        },
        "Cocker Spaniel": {
            idealCBMImin: 30,
            idealCBMImax: 40,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 220 },
                normal: { name: "Adult Dog Food", gramsPerDay: 190 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 160 }
            }
        },
        "Poodle": {
            idealCBMImin: 28,
            idealCBMImax: 35,
            food: {
                underweight: { name: "Small Breed Adult Food", gramsPerDay: 160 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 140 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 120 }
            }
        },
        "German Shepherd": {
            idealCBMImin: 70,
            idealCBMImax: 85,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 400 },
                normal: { name: "Adult Dog Food", gramsPerDay: 350 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 300 }
            }
        },
        "Chow Chow": {
            idealCBMImin: 40,
            idealCBMImax: 50,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 250 },
                normal: { name: "Adult Dog Food", gramsPerDay: 220 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 190 }
            }
        },
        "Boxer": {
            idealCBMImin: 65,
            idealCBMImax: 75,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 360 },
                normal: { name: "Adult Dog Food", gramsPerDay: 320 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 270 }
            }
        },
        // Additional common breeds in the Philippines
        "American Bully": {
            idealCBMImin: 55,
            idealCBMImax: 70,
            food: {
                underweight: { name: "High Protein Dog Food", gramsPerDay: 320 },
                normal: { name: "Adult Dog Food", gramsPerDay: 280 },
                overweight: { name: "Weight Management Dog Food", gramsPerDay: 240 }
            }
        },
        "Shih-Poo": {
            idealCBMImin: 20,
            idealCBMImax: 28,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 160 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 140 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 110 }
            }
        },
        "Chihuahua": {
            idealCBMImin: 15,
            idealCBMImax: 22,
            food: {
                underweight: { name: "Small Breed Puppy Food", gramsPerDay: 120 },
                normal: { name: "Small Breed Adult Food", gramsPerDay: 100 },
                overweight: { name: "Weight Management Small Breed Food", gramsPerDay: 80 }
            }
        }
    },
    cat: {
        "Siamese": {
            idealCBMImin: 14,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 90 },
                normal: { name: "Adult Cat Food", gramsPerDay: 70 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Maine Coon": {
            idealCBMImin: 15,
            idealCBMImax: 20,
            food: {
                underweight: { name: "High Protein Cat Food", gramsPerDay: 100 },
                normal: { name: "Adult Cat Food", gramsPerDay: 95 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 80 }
            }
        },
        "Bengal": {
            idealCBMImin: 14,
            idealCBMImax: 19,
            food: {
                underweight: { name: "High Protein Cat Food", gramsPerDay: 85 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Indoor Cat Food", gramsPerDay: 65 }
            }
        },
        "Norwegian Forest Cat": {
            idealCBMImin: 16,
            idealCBMImax: 22,
            food: {
                underweight: { name: "Indoor Cat Food", gramsPerDay: 100 },
                normal: { name: "Adult Cat Food", gramsPerDay: 90 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 75 }
            }
        },
        "Russian Blue": {
            idealCBMImin: 14,
            idealCBMImax: 19,
            food: {
                underweight: { name: "Balanced Protein Cat Food", gramsPerDay: 85 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Indoor Cat Food", gramsPerDay: 65 }
            }
        },
        "Oriental Shorthair": {
            idealCBMImin: 13,
            idealCBMImax: 18,
            food: {
                underweight: { name: "High Protein Cat Food", gramsPerDay: 80 },
                normal: { name: "Adult Cat Food", gramsPerDay: 70 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Domestic Shorthair": {
            idealCBMImin: 10,
            idealCBMImax: 16,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 90 },
                normal: { name: "Adult Cat Food", gramsPerDay: 70 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Domestic Longhair": {
            idealCBMImin: 12,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 95 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Indoor Cat Food", gramsPerDay: 65 }
            }
        },
        "Persian": {
            idealCBMImin: 12,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 90 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Siberian": {
            idealCBMImin: 15,
            idealCBMImax: 21,
            food: {
                underweight: { name: "High Protein Cat Food", gramsPerDay: 100 },
                normal: { name: "Adult Cat Food", gramsPerDay: 90 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 75 }
            }
        },
        "Scottish Fold": {
            idealCBMImin: 12,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 85 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Manx": {
            idealCBMImin: 13,
            idealCBMImax: 19,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 85 },
                normal: { name: "Adult Cat Food", gramsPerDay: 70 },
                overweight: { name: "Indoor Cat Food", gramsPerDay: 60 }
            }
        },
        // Additional common cat breeds in the Philippines
        "Japanese Bobtail": {
            idealCBMImin: 12,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 85 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
            }
        },
        "Balinese": {
            idealCBMImin: 14,
            idealCBMImax: 19,
            food: {
                underweight: { name: "High Protein Cat Food", gramsPerDay: 90 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 65 }
            }
        },
        "Himalayan": {
            idealCBMImin: 12,
            idealCBMImax: 18,
            food: {
                underweight: { name: "Kitten Food", gramsPerDay: 90 },
                normal: { name: "Adult Cat Food", gramsPerDay: 75 },
                overweight: { name: "Weight Management Cat Food", gramsPerDay: 60 }
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
