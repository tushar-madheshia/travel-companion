import os
import requests
from langchain.tools import tool
from typing import List, Dict, Any
import requests

api_key = os.environ["AMADEUS_API_KEY"]
api_secret = os.environ["AMADEUS_API_SECRET"]
base_url = "https://test.api.amadeus.com"

def get_access_token():
    """Retrieve an access token for authenticating API requests."""
    url = f"{base_url}/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret,
    }
    response = requests.post(url, headers=headers, data=data)
    print(response)
    response.raise_for_status()
    return response.json()["access_token"]
access_token = get_access_token()

# @tool("search_hotels")
def search_hotels(
    city_code: str,
    amenities: List[str] = None,
    ratings: List[int] = None,
) -> Dict[str, Any]:
    """
    Get a list of hotels by city code with optional filters.

    Args:
        city_code (str): The city IATA code (e.g., BLR for Bangalore).
        amenities (List[str], optional): List of amenities to filter hotels (e.g., ["SWIMMING_POOL", "SPA"]). Options available are: SWIMMING_POOL,SPA,RESTAURANT,GOLF,KITCHEN,BEACH,JACUZZI,SAUNA,MASSAGE
        ratings (List[int], optional): List of hotel star ratings (e.g., [3, 4]). range is from 1 to 5.

    Returns:
        dict: A dictionary containing hotel information.
    """
    radius: int = 5,
    radius_unit: str = "KM",
    hotel_source: str = "ALL"
    url = f"{base_url}/v1/reference-data/locations/hotels/by-city"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/vnd.amadeus+json"
    }
    params = {
        "cityCode": city_code,
        "radius": radius,
        "radiusUnit": radius_unit,
        "hotelSource": hotel_source,
    }
    if amenities:
        params["amenities"] = ",".join(amenities)
    if ratings:
        params["ratings"] = ",".join(str(r) for r in ratings)

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        hotels = []
        for hotel in data.get("data", [])[0:6]:
            hotels.append({
                "name": hotel.get("name"),
                "rating": hotel.get("rating"),
                "amenities": hotel.get("amenities", [])
            })

        return {"hotels": hotels}

    except requests.RequestException as e:
        return {"error": str(e)}

@tool("get_hotel_details")
def get_hotel_details( hotel_id: str):
    """
    Get details of a specific hotel.
    Args:
        hotel_id (str): The unique identifier of the hotel.
    Returns:
        dict: A dictionary containing hotel details.
    """
    url = f"{base_url}/v2/shopping/hotel-offers/by-hotel"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"hotelId": hotel_id}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
@tool("get_airport_and_city_search")
def get_airport_and_city_search( keyword: str, sub_type: str = "AIRPORT,CITY"):
    """
    Search for airports and cities by keyword.
    Args:
        keyword (str): The search keyword.
        sub_type (str, optional): The type of locations to search for (e.g., AIRPORT, CITY). Defaults to "AIRPORT,CITY".
    Returns:
        dict: A dictionary containing matching airports and cities.
    """
    url = f"{base_url}/v1/reference-data/locations"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"keyword": keyword, "subType": sub_type}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
@tool("get_airline_details")
def get_airline_details( airline_code: str):
    """
    Get details of an airline by its code.
    Args:
        airline_code (str): The IATA code of the airline.
    Returns:
        dict: A dictionary containing airline details.
    """
    url = f"{base_url}/v1/reference-data/airlines"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"airlineCodes": airline_code}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
@tool("get_city_and_airport_codes")
def get_city_and_airport_codes( latitude: float, longitude: float):
    """
    Get city and airport codes based on latitude and longitude.
    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    Returns:
        dict: A dictionary containing city and airport codes.
    """
    url = f"{base_url}/v1/reference-data/locations/airports"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"latitude": latitude, "longitude": longitude}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
@tool("get_flight_status")
def get_flight_status( flight_number: str, scheduled_departure_date: str):
    """
    Get the status of a flight.
    Args:
        flight_number (str): The flight number.
        scheduled_departure_date (str): The scheduled departure date in YYYY-MM-DD format.
    Returns:
        dict: A dictionary containing the flight status.
    """
    url = f"{base_url}/v2/schedule/flights"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "flightNumber": flight_number,
        "scheduledDepartureDate": scheduled_departure_date,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()