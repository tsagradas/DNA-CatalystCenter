import requests  # Import the requests library for making HTTP requests
import csv  # Import the csv library to handle CSV file operations
import urllib3  # Import urllib3 to manage HTTP connections and warnings
 
# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
def get_auth_token(base_url, username, password):
    # Define the URL for the authentication request
    url = "{}/dna/system/api/v1/auth/token".format(base_url)
    # Make the POST request to obtain an authentication token
    response = requests.post(url, auth=(username, password), verify=False)
 
    # Validate response to check for errors
    if "error" in response.text:
        # Raise an error if token retrieval fails
        raise ValueError("ERROR: Failed to retrieve Access Token! REASON: {}".format(response.json()["error"]))
    else:
        # Extract the token from the response and return it
        token = response.json()["Token"]
        return token
 
def get_building_ids(headers):
    offset = 1  # Initialize the offset for pagination
    buildings = []  # List to store building information
    while True:
        # Send a GET request to retrieve building IDs
        response = requests.get(fhttps://YOURDNAIP/dna/intent/api/v2/site?type=building&limit=500&offset={offset}, headers=headers, verify=False)
        offset += 500  # Increment offset for the next batch of results
        if response.status_code == 200 and response.json().get("response"):
            # Append retrieved buildings to the list
            buildings.extend(response.json().get("response"))
        else:
            # Exit the loop if no more buildings are found
            break
 
    return buildings  # Return the list of buildings
 
def write_file(file, data):
    # Open a CSV file to write the results
    with open(file, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row to the CSV file
        csv_writer.writerow(['Building ID', 'Building Name', 'Total Planned APs'])
 
        # Write each row of building data to the CSV file
        for row in data:
            csv_writer.writerow(row)
 
def main():
    # Define the base API endpoint URL
    base_url = https://YOURDNAIP
 
    # Obtain the authentication token using the provided username and password
    token = get_auth_token(base_url, "admin", input("Enter your DNAC password:  "))
 
    # Define headers for authentication and request
    headers = {
        'x-auth-token': token,  # Include the obtained token in the headers
        'content-type': 'application/json'
    }
 
    try:
        results = []  # List to store results
        offset = 1  # Initialize offset for pagination
        building_ids = get_building_ids(headers)  # Get building IDs
        print(building_ids)  # Print building IDs for debugging
 
        # Check if any buildings were found
        if building_ids:
            # Extract "id" and "name" values from building data
            building_info = [(entry['id'], entry['name']) for entry in building_ids]
        else:
            # Print a message if no buildings are found
            print("No Buildings Found!")
            return
 
        print(building_info)  # Print building information for debugging
 
        # Iterate over each building ID and name
        for building_id, building_name in building_info:
            # Prepare the request URL with the building ID
            request_url = fhttps://YOURDNAIP/dna/intent/api/v1/buildings/{building_id}/planned-access-points?radios=true
 
            # Send GET request to retrieve planned access points for each building
            response = requests.get(request_url, headers=headers, verify=False)
            offset += 500  # Increment offset for pagination
 
            if response.status_code == 200 and response.json().get("response"):
                # Print the building name, response status code, and total planned APs
                print(building_name, response.status_code, response.json()["total"])
                # Append the building data to results
                results.append([building_id, building_name, response.json()["total"]])
 
        # Write the results to a CSV file
        write_file('combined_response_data.csv', results)
 
    except requests.exceptions.RequestException as e:
        # Print an error message if an exception occurs during the request
        print(f"An error occurred: {e}")
 
# Call the main function to execute the script
main()
 
#This script retrieves authentication tokens, building IDs, and planned access points from a DNA Center API and writes the results to a CSV file. It handles HTTP requests, pagination, and exceptions effectively.
