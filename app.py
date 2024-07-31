import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()

def get_coordinates(location_name, GOOGLE_API_KEY):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            location = results[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            raise Exception("No results found for the given location name")
    else:
        raise Exception("Error fetching data from Google Geocoding API")

def get_nearby_real_estate_projects(location, radius, GOOGLE_API_KEY):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": "real_estate_agency",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        raise Exception("Error fetching data from Google Places API")

def search_amenities(project_name, serpapi_key):
    url = "https://serpapi.com/search"
    params = {
        "q": project_name + " amenities",
        "api_key": serpapi_key,
        "engine": "google"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        if 'organic_results' in results:
            snippets = [result['snippet'] for result in results['organic_results']]
            return " ".join(snippets) if snippets else "No information found"
        else:
            return "No information found"
    else:
        raise Exception("Error fetching data from SerpAPI")

def extract_amenities(text):
    amenities_keywords = [
        "wifi", "free wifi", "internet", "free internet",
        "parking", "car parking", "free parking",
        "gym", "fitness center", "fitness club", "health club",
        "swimming pool", "pool",
        "sauna", "steam room", "jacuzzi",
        "play area", "children play area", "kids activities", "kids zone",
        "garden", "landscape garden", "roof garden", "terrace garden",
        "security", "cctv", "surveillance",
        "club house", "community center", "lounge",
        "power backup", "generator", "24/7 power",
        "luxury bathroom", "modular kitchen", "spacious rooms", "living room"
    ]
    found_amenities = [keyword for keyword in amenities_keywords if keyword in text.lower()]
    return list(set(found_amenities))

def format_for_llm(df):
    formatted_text = ""
    for index, row in df.iterrows():
        formatted_text += f"{row['Project']} Amenities:\n"
        formatted_text += ", ".join(row['Extracted Amenities']) + "\n\n"
    return formatted_text

def main(location_name):
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')

    latitude, longitude = get_coordinates(location_name, GOOGLE_API_KEY)
    location = f"{latitude}, {longitude}"
    radius = 1000  # in meters

    projects = get_nearby_real_estate_projects(location, radius, GOOGLE_API_KEY)
    projects_df = pd.DataFrame(projects)
    amenities_data = {}

    for project_name in projects_df['name']:
        amenities = search_amenities(project_name, SERPAPI_KEY)
        amenities_data[project_name] = amenities

    df_amenities = pd.DataFrame({
        "Project": list(amenities_data.keys()),
        "Description": list(amenities_data.values())
    })

    df_amenities['Extracted Amenities'] = df_amenities['Description'].apply(extract_amenities)
    formatted_text = format_for_llm(df_amenities)

    llm = ChatOllama(model="llama3")

    comparison_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that compares amenities of real estate projects."),
            ("human", f"Compare the following amenities:\n\n{formatted_text}")
        ]
    )

    ranking_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant that ranks properties based on their amenities."),
            ("human", f"Rank the following properties based on their amenities considering general preferences and value:\n\n{formatted_text}")
        ]
    )

    comparison_chain = comparison_prompt | llm
    ranking_chain = ranking_prompt | llm

    comparison_response = comparison_chain.invoke({"formatted_text": formatted_text})
    comparison_result = comparison_response.content.strip()

    ranking_response = ranking_chain.invoke({"formatted_text": formatted_text})
    ranking_result = ranking_response.content.strip()

    return location_name, projects_df['name'].head(5), comparison_result, ranking_result

st.title("Real Estate Project Comparison and Ranking")

location_name = st.text_input("Enter a location name:")

if st.button("Get Comparison and Ranking"):
    if location_name:
        try:
            location_name, nearby_projects, comparison_result, ranking_result = main(location_name)
            st.write(f"Location: {location_name}")
            st.write(f"Nearby Real Estate Projects: {', '.join(nearby_projects)}")
            st.write("### Comparison Result:")
            st.write(comparison_result)
            st.write("### Ranking Result:")
            st.write(ranking_result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a location name.")
