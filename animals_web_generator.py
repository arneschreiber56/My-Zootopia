"""MasterSchool Zootopia Codio Project"""

import requests

URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = "mguXnpVqJI7mcZYxz68YaMeJ88AlVeaaCjU1IsD1"
TEMPLATE_HTML = "animals_template.html"
NEW_HTML = "animals.html"
POINTER = "__REPLACE_ANIMALS_INFO__"


def get_response_json(animal):
    """Request animal data from the API and return the JSON response as
    dicts in a list.

    Sends a GET request to the animals endpoint using the configured
    animal name and API key. If the request is successful (HTTP 200),
    the JSON response is returned. Otherwise, an empty list is returned
    to ensure stable downstream processing.

    Returns a list containing raw animal data from the API."""
    response = requests.get(
        URL,
        params={"name": animal},
        headers={"X-Api-Key": API_KEY},
        timeout=10
    )
    if response.status_code == 200:
        return response.json()
    return []


def get_check_animal_dict(animal):
    """Extract validated animal information from a raw JSON entry.

    Performs defensive extraction of name, diet, location and type.
    Missing or malformed fields are returned as None to ensure stability.

    Returns a dictionary with the keys: name, diet, location, type."""
    animal_name = animal.get("name")  # .get("name") gibt entweder value oder None

    if isinstance(animal.get("characteristics"), dict):
        characteristics = animal.get("characteristics")
        animal_diet = characteristics.get("diet")
        animal_type = characteristics.get("type")
    else:
        animal_diet = None
        animal_type = None

    if isinstance(animal.get("locations"), list) and animal.get("locations"):
        animal_location = animal.get("locations")[0]
    else:
        animal_location = None

    animal_dict = {
        "name": animal_name,
        "diet": animal_diet,
        "location": animal_location,
        "type": animal_type
    }
    return animal_dict


def create_reduced_animals_lst(animals_data):
    """Create a list of reduced animal dictionaries.

    Iterates through the raw JSON list and extracts core information
    for each valid animal entry using defensive extraction. Invalid or
    non-dictionary entries are skipped.

    Returns a list of dictionaries with normalized animal information."""
    animal_lst = []
    if animals_data:
        for animal in animals_data:
            if isinstance(animal, dict):
                animal_dict = get_check_animal_dict(animal)
                animal_lst.append(animal_dict)
        return animal_lst
    else:
        return []


def serialize_animal(animal):
    """Serialize a single animal dictionary into an HTML card.

    Builds a card-style HTML snippet for one animal using the provided
    dictionary. The name is rendered as the card title and the remaining
    attributes are displayed as labeled lines. Fields with None values
    are omitted.

    Returns an HTML string representing one animal card."""
    output = '<li class="cards__item">\n'
    output += f'<div class="card__title">{animal.get("name")}</div>\n'
    output += '<p class="card__text">\n'
    for cat, info in animal.items():
        if info and cat != 'name':
            output += f'<strong>{cat.title()}:</strong> {info}<br/>\n'
    output += '</p>\n'
    output += '</li>\n'
    return output


def get_animal_info_output(animals_subdata):
    """Generate HTML list items for the given animal data.

    Builds a card-style HTML snippet for each animal, including a title
    and formatted attributes. Fields with None values are omitted.

    Returns a concatenated HTML string containing all list items."""
    output = ""
    for animal in animals_subdata:
        output += serialize_animal(animal)
    return output


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


def write_html_animal(html_content):
    """Write the final HTML output to animals.html.

    Attempts to create or overwrite animals.html with the provided
    HTML content. Returns True on success, False on failure."""
    try:
        with open(NEW_HTML, "w") as fileobj:
            fileobj.write(html_content)
            return True
    except FileNotFoundError:
        return False


def get_user_animal_query():
    """Prompt the user to enter the name of an animal.

    Reads the user input from the console and returns the entered
    animal name as a string.

    Returns the user-provided animal query."""
    user_input = input("Enter a name of an animal: ")
    return user_input.strip()


def main():
    """Run the full animal processing and HTML generation pipeline.

    Loads JSON data, extracts reduced animal information, formats it
    into HTML, replaces the placeholder in the template, and writes
    the final output file. Prints status messages for all major steps."""
    animal_query = get_user_animal_query()
    animals_data = get_response_json(animal_query)
    if animals_data:
        print("Data successfully requested!")
        animals_subdata = create_reduced_animals_lst(animals_data)
        print("Reduced animals data list successfully created!")
        output = get_animal_info_output(animals_subdata)
        print("Animals info output successfully created!")
        html_content = get_html_content()
        if html_content and html_content.count(POINTER) == 1:
            html_content_animal = html_content.replace(
                POINTER, output
            )
            print("Placeholder in HTML replaced!")
        else:
            print("could not find HTML or add output data!")
            return
        if write_html_animal(html_content_animal):
            print("successfully created HTML animal.html!")
        else:
            print("could not create HTML animal.html!")
    else:
        print(f"Request failed")


if __name__ == "__main__":
    main()
