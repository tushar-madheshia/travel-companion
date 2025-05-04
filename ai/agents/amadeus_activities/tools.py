import os
import requests
from langchain.tools import tool
from typing import List, Dict, Any


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

@tool("get_activities")
def get_activities(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get a list of activities based on latitude and longitude.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        dict: A dictionary containing a list of simplified activities.
    """
    radius = 25
    url = f"{base_url}/v1/shopping/activities"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/vnd.amadeus+json"
    }
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        activities = []
        for activity in data.get("data", [])[0:3]:  # Limit to 3 activities
            activities.append({
                "name": activity.get("name"),
                "price": activity.get("price", {}).get("amount"),
                "currency": activity.get("price", {}).get("currencyCode"),
                "description": activity.get("shortDescription"),
            })

        return {"activities": activities}

    except requests.RequestException as e:
        return {"error": str(e)}
