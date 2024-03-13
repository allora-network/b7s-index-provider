import requests
import os
import sys
import json


UPSHOT_API_TOKEN = os.environ.get('UPSHOT_API_TOKEN')
INDEXES_SUPPORTED = [
    "yuga", "pfp", "artblocks", "30-liquid",
    "yuga-grail", "pfp-grail", "artblocks-grail"
]


def get_index_url(index_name):
    return f"https://api.upshot.xyz/v2/indexes/{index_name}/historical?include_count=false"


def get_first_price(url, api_key):
    headers = {'x-api-key': api_key}
    # Make an HTTP request to the specified URL with the API key in the headers
    response = requests.get(url, headers=headers)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Check if 'data' and 'prices' are present in the response
        if 'data' in data and 'prices' in data['data']:
            # Get the first price from the list of prices
            prices = data['data']['prices']
            if prices:
                first_price = prices[0]
                return first_price

    # If the request was not successful or the response format is unexpected, return None
    return None


def process(index_name):
    if index_name not in INDEXES_SUPPORTED:
        print(json.dumps({"error": "topic not supported"}))
        return
    url = get_index_url(index_name)
    first_price = get_first_price(url, UPSHOT_API_TOKEN)
    if first_price:
        # Extract the 'wei' value
        wei_value = first_price['wei']
        response = json.dumps({"value": str(wei_value)}) 
    else:
        response = json.dumps({"error": "No predictions"})
    return response


if __name__ == "__main__":
    # Your code logic with the parsed argument goes here
    # Parameters: topic_id, index_name
    try:
        # Not using to discriminate by topicId for simplicity.
        # topic_id = sys.argv[1]
        index_name = sys.argv[2]
        response = process(index_name)
    except Exception as e:
        response = json.dumps({"error": {str(e)}})
    print(response)
