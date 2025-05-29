import requests
from datetime import date

# API endpoint
url = "http://localhost:8000/api/v1/user/search"

# Test parameters
params = {
    "registrationid": 1001,  # Using one of the registration IDs we just created
    "date": date.today().isoformat()  # Today's date in ISO format
}

try:
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Print the request URL for debugging
    print(f"Request URL: {response.url}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print("\nSuccess! Response data:")
        print(response.json())
    else:
        print(f"\nError: Status code {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print(f"Error occurred: {str(e)}") 