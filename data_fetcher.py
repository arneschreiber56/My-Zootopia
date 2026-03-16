"""
Utility module for fetching animal data and loading the HTML template.

This module provides three core functions:

- get_response_json(animal):
    Sends a request to the Animals API using the provided animal name.
    Returns a list of raw JSON dictionaries on success or an empty list
    on failure. Network errors and non-200 responses are handled
    defensively to ensure stable downstream processing.

- get_html_content():
    Loads the HTML template file defined by TEMPLATE_HTML and returns its
    content as a string. Returns None if the file is missing.

- get_user_animal_query():
    Prompts the user for an animal name, strips surrounding whitespace,
    and returns the cleaned query string.
.
Returns: a list of animals, each animal is a dictionary:
{
  'name': ...,
  'taxonomy': {
    ...
  },
  'locations': [
    ...
  ],
  'characteristics': {
    ...
  }
},
"""
import requests

URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = "mguXnpVqJI7mcZYxz68YaMeJ88AlVeaaCjU1IsD1"
TEMPLATE_HTML = "animals_template.html"


def get_response_json(animal):
    """Request animal data from the API and return the JSON response as
    dicts in a list.

    Sends a GET request to the animals endpoint using the configured
    animal name and API key. If the request is successful (HTTP 200),
    the JSON response is returned. Otherwise, an empty list is returned
    to ensure stable downstream processing.

    Returns a list containing raw animal data from the API."""
    try:
        response = requests.get(
            URL,
            params={"name": animal},
            headers={"X-Api-Key": API_KEY},
            timeout=10
        )
    # requests.RequestExceptions only catches network errors
    except requests.RequestException as e:
        print(e)
        return []
    if response.status_code == 200:
        return response.json()
    return []


def get_html_content():
    """Load the HTML template file.

    Reads TEMPLATE_HTML and returns its content as a string.
    Returns None if the file is missing."""
    try:
        with open(TEMPLATE_HTML, "r") as txt:
            html_content = txt.read()
            return html_content
    except FileNotFoundError:
        return None


def get_user_animal_query():
    """Prompt the user to enter the name of an animal.

    Reads the user input from the console and returns the entered
    animal name as a string.

    Returns the user-provided animal query."""
    user_input = input("Enter a name of an animal: ")
    return user_input.strip()
