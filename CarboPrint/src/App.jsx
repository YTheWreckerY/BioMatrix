import React, { useState } from "react";
import "./App.css";
import bgVideo from "./background_vid.mp4"; 

function App() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    vehicleOwned: "",
    foodType: "",
    meatType: "",
    clothType: "",
    IntTravelPerYear: "",
    buildingType: "",
    waterUsageDay: "",
    transportType: "",
    workCulture: "",
    Gardens: "",
    fuelTypeVehicle: "",
    fuelTypeDomestic: "",
    DailyTravel: ""
  });

  const [carbonFootprint, setCarbonFootprint] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);

  const totalSlides = 15; 

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const calculateCarbonFootprint = () => {
    let userTotalData = 0;

    if (formData.vehicleOwned === "Yes") userTotalData += 500;

    userTotalData +=
      formData.foodType === "Vegetarian" ? 100 :
      formData.foodType === "Lacto-Vegetarian" ? 200 :
      formData.foodType === "Pescetarian" ? 300 :
      formData.foodType === "Flexitarian" ? 400 :
      formData.foodType === "Non-Vegetarian" ? 500 : 0;

    userTotalData +=
      formData.meatType === "Beef" ? 800 :
      formData.meatType === "Mutton" ? 750 :
      formData.meatType === "Bacon" ? 700 :
      formData.meatType === "Pork" ? 650 :
      formData.meatType === "Turkey" ? 500 :
      formData.meatType === "Duck" ? 450 :
      formData.meatType === "Chicken" ? 400 :
      formData.meatType === "Seafood" ? 300 : 0;

    userTotalData +=
      formData.clothType === "Silk" ? 700 :
      formData.clothType === "Velvet" ? 660 :
      formData.clothType === "Georgette" ? 640 :
      formData.clothType === "Nylon" ? 580 :
      formData.clothType === "Wool" ? 550 :
      formData.clothType === "Rayon" ? 510 :
      formData.clothType === "Denim" ? 470 :
      formData.clothType === "Cotton" ? 440 : 0;

    userTotalData += Number(formData.IntTravelPerYear) * 200 || 0;

    userTotalData +=
      formData.buildingType === "High-Rise" ? 500 :
      formData.buildingType === "Low-Rise" ? 300 :
      formData.buildingType === "Independent" ? 650 : 0;

    userTotalData += Number(formData.waterUsageDay) || 0;

    userTotalData +=
      formData.transportType === "Bus" ? 600 :
      formData.transportType === "Bike" ? 400 :
      formData.transportType === "Car" ? 500 :
      formData.transportType === "Train" ? 750 : 0;

    if (formData.workCulture === "at home") {
      userTotalData /= 2;
    } else if (formData.workCulture === "at office") {
      userTotalData *= 2;
    }

    if (formData.Gardens === "Yes") {
      userTotalData /= 2;
    } else if (formData.Gardens === "No") {
      userTotalData *= 1.5;
    }

    userTotalData +=
      formData.fuelTypeVehicle === "Petrol" ? 500 :
      formData.fuelTypeVehicle === "Diesel" ? 450 :
      formData.fuelTypeVehicle === "Gasoline" ? 600 :
      formData.fuelTypeVehicle === "Hydrogen" ? 250 :
      formData.fuelTypeVehicle === "Electric" ? 50 : 0;
      
    userTotalData +=
        formData.fuelTypeDomestic === "Gas" ? 300 :
        formData.fuelTypeDomestic === "Electric" ? 100 :
        formData.fuelTypeDomestic === "Wood" ? 400 : 0;

    userTotalData += Number(formData.DailyTravel) * 10 || 0;

    return Math.round(userTotalData);
  };

  const handleSubmit = e => {
    e.preventDefault();
    const total = calculateCarbonFootprint();
    setCarbonFootprint(total);
    setCurrentSlide(totalSlides); 
  };

  const nextSlide = () => setCurrentSlide(prev => (prev + 1 < totalSlides + 1 ? prev + 1 : prev));
  const prevSlide = () => setCurrentSlide(prev => (prev > 0 ? prev - 1 : prev));

  return (
    <div id="root">
      <video autoPlay muted loop playsInline className="bg-video">
        <source src={bgVideo} type="video/mp4" />
      </video>

      <h1 className="title">CarboPrint Calculator</h1>

      <form onSubmit={handleSubmit}>
        {currentSlide === 0 && (
          <div className="form-slide">
            <label htmlFor="firstName">First Name</label>
            <input 
              className="form" 
              id="firstName"
              placeholder="Enter First Name" 
              name="firstName" 
              value={formData.firstName} 
              onChange={handleChange} 
            />
            
            <label htmlFor="lastName">Last Name</label>
            <input 
              className="form" 
              id="lastName"
              placeholder="Enter Last Name" 
              name="lastName" 
              value={formData.lastName} 
              onChange={handleChange} 
            />
          </div>
        )}

        {currentSlide === 1 && (
          <div className="form-slide">
            <label htmlFor="vehicleOwned">Do you own a vehicle?</label>
            <select
              id="vehicleOwned"
              name="vehicleOwned" 
              value={formData.vehicleOwned} 
              onChange={handleChange}
            >
              <option value="">Select an option</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        )}

        {currentSlide === 2 && (
          <div className="form-slide">
            <label htmlFor="foodType">Choose one of the food types:</label>
            <select 
              id="foodType"
              name="foodType" 
              value={formData.foodType} 
              onChange={handleChange} 
            >
              <option value="">Select a food type</option>
              <option value="Vegetarian">Vegetarian (No meat, eggs)</option>
              <option value="Lacto-Vegetarian">Lacto-Vegetarian (Includes dairy)</option>
              <option value="Pescetarian">Pescetarian (Includes fish/seafood)</option>
              <option value="Flexitarian">Flexitarian (Mostly vegetarian, occasional meat)</option>
              <option value="Non-Vegetarian">Non-Vegetarian (Eats meat regularly)</option>
            </select>
          </div>
        )}

        {currentSlide === 3 && (
          <div className="form-slide">
            <label htmlFor="meatType">Which meat do you consume most often?</label>
            <select 
              id="meatType"
              name="meatType" 
              value={formData.meatType} 
              onChange={handleChange} 
            >
              <option value="">Select a meat type</option>
              <option value="Beef">Beef</option>
              <option value="Mutton">Mutton/Lamb</option>
              <option value="Pork">Pork (Bacon/Ham/Pork)</option>
              <option value="Turkey">Turkey</option>
              <option value="Duck">Duck</option>
              <option value="Chicken">Chicken</option>
              <option value="Seafood">Seafood/Fish</option>
            </select>
          </div>
        )}

        {currentSlide === 4 && (
          <div className="form-slide">
            <label htmlFor="clothType">What type of cloth do you purchase most often?</label>
            <select
              id="clothType"
              name="clothType" 
              value={formData.clothType} 
              onChange={handleChange}
            >
              <option value="">Select a cloth type</option>
              <option value="Cotton">Cotton</option>
              <option value="Denim">Denim</option>
              <option value="Rayon">Rayon/Viscose</option>
              <option value="Wool">Wool</option>
              <option value="Nylon">Nylon/Polyester (Synthetic)</option>
              <option value="Georgette">Georgette/Chiffon</option>
              <option value="Velvet">Velvet</option>
              <option value="Silk">Silk</option>
            </select>
          </div>
        )}

        {currentSlide === 5 && (
          <div className="form-slide">
            <label htmlFor="IntTravelPerYear">International flights per year (Round Trips):</label>
            <input 
              type="number" 
              id="IntTravelPerYear"
              name="IntTravelPerYear" 
              value={formData.IntTravelPerYear} 
              onChange={handleChange} 
              min="0"
              placeholder="0 for none"
            />
          </div>
        )}

        {currentSlide === 6 && (
          <div className="form-slide">
            <label htmlFor="buildingType">Type of building you live in:</label>
            <select
              id="buildingType"
              name="buildingType" 
              value={formData.buildingType} 
              onChange={handleChange}
            >
              <option value="">Select a building type</option>
              <option value="Independent">Independent House/Villa</option>
              <option value="High-Rise">Apartment (High-Rise)</option>
              <option value="Low-Rise">Apartment (Low-Rise/Block)</option>
            </select>
          </div>
        )}

        {currentSlide === 7 && (
          <div className="form-slide">
            <label htmlFor="waterUsageDay">Estimated daily water usage (Liters):</label>
            <input 
              type="number" 
              id="waterUsageDay"
              name="waterUsageDay" 
              value={formData.waterUsageDay} 
              onChange={handleChange} 
              min="0"
              placeholder="e.g., 150"
            />
          </div>
        )}

        {currentSlide === 8 && (
          <div className="form-slide">
            <label htmlFor="transportType">Primary daily transport type:</label>
            <select
              id="transportType"
              name="transportType" 
              value={formData.transportType} 
              onChange={handleChange}
            >
              <option value="">Select a transport type</option>
              <option value="Bus">Bus/Public Transport</option>
              <option value="Train">Train/Metro</option>
              <option value="Bike">Motorcycle/Scooter</option>
              <option value="Car">Car</option>
              <option value="Walk/Cycle">Walk/Cycle (Low Impact)</option>
            </select>
          </div>
        )}

        {currentSlide === 9 && (
          <div className="form-slide">
            <label htmlFor="workCulture">Primary work location:</label>
            <select
              id="workCulture"
              name="workCulture" 
              value={formData.workCulture} 
              onChange={handleChange}
            >
              <option value="">Select location</option>
              <option value="at home">Work from Home (at home)</option>
              <option value="at office">Work at Office (at office)</option>
            </select>
          </div>
        )}

        {currentSlide === 10 && (
          <div className="form-slide">
            <label htmlFor="Gardens">Do you have a personal garden/green space?</label>
            <select
              id="Gardens"
              name="Gardens" 
              value={formData.Gardens} 
              onChange={handleChange}
            >
              <option value="">Select an option</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>
        )}

        {currentSlide === 11 && (
          <div className="form-slide">
            <label htmlFor="fuelTypeVehicle">Vehicle fuel type (if owned):</label>
            <select
              id="fuelTypeVehicle"
              name="fuelTypeVehicle" 
              value={formData.fuelTypeVehicle} 
              onChange={handleChange}
            >
              <option value="">Select fuel type</option>
              <option value="Petrol">Petrol/Gasoline</option>
              <option value="Diesel">Diesel</option>
              <option value="Gasoline">LPG/CNG/Gasoline</option>
              <option value="Hydrogen">Hydrogen</option>
              <option value="Electric">Electric/Hybrid</option>
            </select>
          </div>
        )}

        {currentSlide === 12 && (
          <div className="form-slide">
            <label htmlFor="fuelTypeDomestic">Primary home heating/cooking fuel type:</label>
            <select
              id="fuelTypeDomestic"
              name="fuelTypeDomestic" 
              value={formData.fuelTypeDomestic} 
              onChange={handleChange}
            >
              <option value="">Select fuel type</option>
              <option value="Gas">Natural Gas/LPG</option>
              <option value="Electric">Electricity (Grid)</option>
              <option value="Wood">Wood/Coal/Biomass</option>
            </select>
          </div>
        )}

        {currentSlide === 13 && (
          <div className="form-slide">
            <label htmlFor="DailyTravel">Average daily commute distance (km):</label>
            <input 
              type="number" 
              id="DailyTravel"
              name="DailyTravel" 
              value={formData.DailyTravel} 
              onChange={handleChange} 
              min="0"
              placeholder="Distance one way (km)"
            />
          </div>
        )}

        {currentSlide === 14 && (
          <div className="form-slide">
            <button type="submit">Calculate Footprint</button>
          </div>
        )}

        {currentSlide === totalSlides && (
          <div className="result-screen">
            <h1>Your Estimated Annual Carbon Footprint:</h1>
            <h2>{carbonFootprint ? `${carbonFootprint} kg CO2e` : 'N/A'}</h2>
            <p>
                <small>*This is an estimation based on your input and general carbon factors.</small>
            </p>
          </div>
        )}
      </form>

      <div className="navigation-controls">
        <button 
          className="prev" 
          onClick={prevSlide} 
          disabled={currentSlide === 0 || currentSlide === totalSlides}
        >
          &larr; Previous
        </button>
        <button 
          className="next" 
          onClick={nextSlide} 
          disabled={currentSlide >= totalSlides - 1 || currentSlide === totalSlides}
        >
          Next &rarr;
        </button>
      </div>

    </div>
  );
}

export default App;