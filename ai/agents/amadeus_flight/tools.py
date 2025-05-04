import os
import requests
from langchain.tools import tool


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

# @tool("search_flights")
def search_flights(origin: str, destination: str, departure_date: str, return_date: str = None, nonStop: str="true", travelClass:str ="ECONOMY", adults: int = 1):
    """
    Search for flight offers.
    Args:
        origin (str): The IATA code of the origin airport.
        destination (str): The IATA code of the destination airport.
        departure_date (str): The departure date in YYYY-MM-DD format.
        return_date (str, optional): The return date in YYYY-MM-DD format.
        adults (int, optional): Number of adult passengers. Defaults to 1.
        nonStop (bool, optional): Whether to search for non-stop flights. Defaults to True, meaning non-stop flights only. You should inform this to user when you respond
        travelClass (str, optional): The travel class (e.g., ECONOMY, BUSINESS). Defaults to "ECONOMY".        
        
    Returns:
        dict: A dictionary containing flight offers.
    """
    url = f"{base_url}/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "nonStop": nonStop,
        "travelClass": travelClass,
        "max": 3,
    }
    if return_date:
        params["returnDate"] = return_date
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
@tool("search_hotels")
def search_hotels( city_code: str, check_in_date: str, check_out_date: str, adults: int = 1):
    """
    Search for hotel offers.
    Args:
        city_code (str): The IATA city code.
        check_in_date (str): The check-in date in YYYY-MM-DD format.
        check_out_date (str): The check-out date in YYYY-MM-DD format.
        adults (int, optional): Number of adult guests. Defaults to 1.
    Returns:
        dict: A dictionary containing hotel offers.
    """
    url = f"{base_url}/v2/shopping/hotel-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "cityCode": city_code,
        "checkInDate": check_in_date,
        "checkOutDate": check_out_date,
        "adults": adults,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
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