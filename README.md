# Real Estate Project Comparison and Ranking

This application compares and ranks real estate projects based on their amenities using Google Geocoding API, Google Places API, SerpAPI, and the LangChain framework with Ollama's llama3 model.
![image](https://github.com/user-attachments/assets/ea2b7155-a2a0-4d98-b2c7-957e8d1ad321)


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Tools Used](#tools-used)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/arsh248/Real_estate_project_comparison
   cd Real_estate_project_comparison
   
2. **Creating a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
3. **Install the required packages:**
   ```bash
    pip install -r requirements.txt
   
4. **Create a .env file in the root directory and add your API keys:**
   ```bash
    GOOGLE_API_KEY=your_google_api_key
    SERPAPI_KEY=your_serpapi_key


## Usage

1. **Run the Streamlit application:**
  ```bash
  streamlit run app.py
```
2. **Open your web browser and go to http://localhost:8501.**
3. **Enter a location name in the input box and click on the "Get Comparison and Ranking" button.**


## Code Explanation

### Functions

- **`get_coordinates(location_name, GOOGLE_API_KEY)`**
  - Fetches the geographical coordinates (latitude and longitude) for a given location name using the Google Geocoding API.

- **`get_nearby_real_estate_projects(location, radius, GOOGLE_API_KEY)`**
  - Retrieves nearby real estate projects within a specified radius using the Google Places API.

- **`search_amenities(project_name, serpapi_key)`**
  - Searches for amenities of a given real estate project using SerpAPI.

- **`extract_amenities(text)`**
  - Extracts a list of amenities from a given text description.

- **`format_for_llm(df)`**
  - Formats the extracted amenities data into a text format suitable for input to a language model.

- **`main(location_name)`**
  - Main function to fetch nearby real estate projects, extract and format amenities, and get comparison and ranking results from the language model.

## Streamlit Integration

The Streamlit app takes a location name as input and displays the comparison and ranking results for the top nearby real estate projects based on their amenities.

## Tools Used

- **Google Geocoding API**: To convert location names into geographical coordinates.
- **Google Places API**: To find nearby real estate projects based on the given location.
- **SerpAPI**: To search and fetch amenities information for the real estate projects.
- **LangChain Framework**: To handle prompts and responses for comparing and ranking amenities.
- **Ollama's llama3 Model**: Used as the language model to generate comparison and ranking of amenities.



