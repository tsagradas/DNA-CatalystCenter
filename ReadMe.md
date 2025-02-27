Planned APs Cisco DNA/Catalyst Center Collection Automation

This automation is particularly useful for Prime to DNA/CC Center migrations or when there are multiple planned Access Points (APs) already present in the system.


Methods to Collect Planned APs:

Manual Collection: Navigate to the floor plan and use the "View Options" to collect planned APs.
API Method 1: Use the API to get planned access points for a specific floor.
API Method 2: Use the API to get planned access points for a specific building.

Currently, there is no option available to collect this information for all sites simultaneously.


Scripts for Collecting Planned AP Data:

Script 1: collect_total_planned_aps.py
This script collects the total number of planned Access Points.

Script 2: collect_total_planned_aps_info.py
This script gathers detailed information about each planned Access Point, formatted as follows:

 "response": [
        {
            "attributes": {
                "id": "number",
                "instanceUuid": "string",
                "name": "string",
                "typeString": "string",
                "domain": "string",
                "hierarchyName": "string",
                "source": "string",
                "createDate": "number",
                "macAddress": "string"
            },
            "location": {
                "altitude": "number",
                "latitude": "number",
                "longitude": "number"
            },
            "position": {
                "x": "number",
                "y": "number",
                "z": "number"
            },
            "radioCount": "integer",
            "radios": [
                {
                    "attributes": {
                        "id": "integer",
                        "instanceUuid": "string",
                        "slotId": "number",
                        "ifTypeString": "string",
                        "ifTypeSubband": "string",
                        "channel": "number",
                        "channelString": "string",
                        "ifMode": "string",
                        "txPowerLevel": "number"
                    },
                    "antenna": {
                        "name": "string",
                        "type": "string",
                        "mode": "string",
                        "azimuthAngle": "number",
                        "elevationAngle": "number",
                        "gain": "number"
                    },
                    "isSensor": "boolean"
                }
            ],
            "isSensor": "boolean"
        }
    ],
    "version": "integer",
    "total": "integer"
}

This structured JSON format includes comprehensive details of each planned AP, such as its attributes, location, position, and radio configuration.

Note:
- Ensure to handle any potential errors, such as a 404 response, which indicates that the requested resource could not be found.
- The output while be displayed under the same folder location with the name "combined_response_data.csv"

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
