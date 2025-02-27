import requests
import csv
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_auth_token(base_url, username, password):
    """
    Retrieves an authentication token from the DNA Center.
    
    :param base_url: The base URL of the DNA Center.
    :param username: The username for authentication.
    :param password: The password for authentication.
    :return: The authentication token as a string.
    """
    url = "{}/dna/system/api/v1/auth/token".format(base_url)
    # Make the POST request to obtain the token
    response = requests.post(url, auth=(username, password), verify=False)

    # Validate the response to check for errors
    if "error" in response.text:
        raise ValueError("ERROR: Failed to retrieve Access Token! REASON: {}".format(response.json()["error"]))
    else:
        token = response.json()["Token"]
        return token  # Return only the token

def get_building_ids(headers):
    """
    Retrieves a list of building IDs from the DNA Center.
    
    :param headers: The headers for the request, including the authentication token.
    :return: A list of building data.
    """
    offset = 1
    buildings = []
    while True:
        # Send a GET request to get all building IDs with pagination
        response = requests.get(f"https://172.28.60.227/dna/intent/api/v2/site?type=building&limit=500&offset={offset}", headers=headers, verify=False)
        offset += 500
        if response.status_code == 200 and response.json().get("response"):
            buildings.extend(response.json().get("response"))  # Add building data to the list
        else:
            break  # Exit loop if no more data is found

    return buildings

def main():
    """
    Main function to execute the script tasks.
    """
    # Define the base API endpoint
    base_url = "https://172.28.60.227"

    # Get the authentication token using the provided username and password
    token = get_auth_token(base_url, "admin", input("Enter your DNAC password:  "))

    # Define headers for authentication and request
    headers = {
        'x-auth-token': token,
        'content-type': 'application/json'
    }

    # Open a CSV file to write the combined results
    with open('combined_response_data.csv', mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row to the CSV file
        csv_writer.writerow(['Building ID', 'Building Name', 'Response Data'])

        try:
            offset = 1
            # Retrieve building IDs
            building_ids = get_building_ids(headers)
            print(building_ids)

            if building_ids:
                # Extract all "id" and "name" values from the building data
                building_info = [(entry['id'], entry['name']) for entry in building_ids]
            else:
                print("No Buildings Found!")
                return

            print(building_info)

            # Iterate over each building and collect planned access point data
            for building_id, building_name in building_info:
                while True:
                    # Prepare the request URL with the building ID for planned access points
                    request_url = f"https://172.28.60.227/dna/intent/api/v1/buildings/{building_id}/planned-access-points?limit=500&offset={offset}&radios=true"

                    # Send GET request for each building
                    response = requests.get(request_url, headers=headers, verify=False)
                    offset += 500

                    if response.status_code == 200 and response.json().get("response"):
                        # Write the building ID, name, and response data to the CSV file
                        csv_writer.writerow([building_id, building_name, response.text])
                        print(building_name, response.status_code, response.text)
                    else:
                        break  # Exit loop if no more data is found

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")  # Handle exceptions

# Execute the main function
main()
