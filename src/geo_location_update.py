import json
from opencage.geocoder import OpenCageGeocode
from src.config import OPENCAGE_API_KEY

def update_from_partial_address(json_file_path):

    # Initialize geocoder
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

    # Load address JSON
    with open(json_file_path, 'r') as f:
        address_data = json.load(f)

    # Get zipcode and country
    zipcode = address_data.get('zipcode')
    country = address_data.get('country')

    # Default country if missing
    if not country:
        country = 'United States'
        address_data['country'] = country

    # Build query
    if zipcode:
        query = f"{zipcode}, {country}"
    else:
        # Use only non-null fields to form query
        query_fields = ['house_no', 'street', 'unit', 'landmark', 'borough', 'county', 'city', 'state', 'country']
        query = ', '.join([
            str(address_data[field]) for field in query_fields if address_data.get(field)
        ])

    # Make the geocode API call
    results = geocoder.geocode(query)

    if not results:
        raise ValueError(f"No results found for query: {query}")

    components = results[0].get('components', {})
    print(components)

    # Map local keys to possible OpenCage component keys
    key_map = {
        'house_no': ['house_number'],
        'street': ['road'],
        'unit': ['unit'],  # Often unavailable
        'landmark': ['attraction', 'building', 'neighbourhood'],
        'borough': ['borough', 'suburb', 'neighbourhood', 'city_district'],
        'county': ['county'],
        'city': ['city'],
        'state': ['state'],
        'country': ['country'],
        'zipcode': ['postcode'],
    }

    # Overwrite existing fields only if API provides a non-null value
    for json_key, possible_keys in key_map.items():
        for comp_key in possible_keys:
            value = components.get(comp_key)
            if value is not None:
                address_data[json_key] = value
                break  # Stop at first found value

    # Save updated JSON back to file
    with open(json_file_path, 'w') as f:
        json.dump(address_data, f, indent=4)

    print("✅ Address updated (with overwrite protection).")