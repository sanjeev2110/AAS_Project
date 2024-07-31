import requests
import json

# Define the base URL of the Flask server
base_url = 'http://localhost:5005'

# Fetch the submodel
def fetch_submodel():
    response = requests.get(f'{base_url}/submodel')
    if response.status_code == 200:
        print("Submodel fetched successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error fetching submodel: {response.status_code}")

# Update a submodel element
def update_element(id_short, value):
    response = requests.post(f'{base_url}/submodel/element/{id_short}', json={'value': value})
    if response.status_code == 200:
        print(f"Element '{id_short}' updated successfully:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error updating element '{id_short}': {response.status_code}")
        print(response.json())

# Example usage
if __name__ == "__main__":
    print("\nFetching submodel...")
    fetch_submodel()

    print("\nUpdating submodel element 'GoodParts'...")
    update_element("GoodParts", 200)

    print("\nUpdating submodel element 'BadParts'...")
    update_element("BadParts", 20)
