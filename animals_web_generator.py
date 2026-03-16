"""MasterSchool Zootopia Codio Project"""

import json

JSON_FILE = "animals_data.json"
TEMPLATE_HTML = "animals_template.html"
NEW_HTML = "animals.html"
POINTER = "__REPLACE_ANIMALS_INFO__"


def load_data(file_path):
    """Load JSON data from a file.

    Opens the given file path and returns the parsed JSON content.
    Returns None if the file does not exist."""
    try:
        with open(file_path, "r") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return None


def get_check_animal_dict(animal):
    """Extract validated animal information from a raw JSON entry.

    Performs defensive extraction of name, diet, location and type.
    Missing or malformed fields are returned as None to ensure stability.

    Returns a dictionary with the keys: name, diet, location, type."""
    fox_name = animal.get("name")  # .get("name") gibt entweder value oder None

    if isinstance(animal.get("characteristics"), dict):
        characteristics = animal.get("characteristics")
        fox_diet = characteristics.get("diet")
        fox_type = characteristics.get("type")
    else:
        fox_diet = None
        fox_type = None

    if isinstance(animal.get("locations"), list) and animal.get("locations"):
        fox_location = animal.get("locations")[0]
    else:
        fox_location = None

    animal_dict = {
        "name": fox_name,
        "diet": fox_diet,
        "location": fox_location,
        "type": fox_type
    }
    return animal_dict


def create_reduced_animals_lst(animals_data):
    """Create a list of reduced animal dictionaries.

    Iterates through the raw JSON list and extracts core information
    for each valid animal entry using defensive extraction. Invalid or
    non-dictionary entries are skipped.

    Returns a list of dictionaries with normalized animal information."""
    fox_lst = []
    if animals_data:
        for animal in animals_data:
            if isinstance(animal, dict):
                animal_dict = get_check_animal_dict(animal)
                fox_lst.append(animal_dict)
        return fox_lst
    else:
        return []


def serialize_animal(fox):
    """Serialize a single animal dictionary into an HTML card.

    Builds a card-style HTML snippet for one animal using the provided
    dictionary. The name is rendered as the card title and the remaining
    attributes are displayed as labeled lines. Fields with None values
    are omitted.

    Returns an HTML string representing one animal card."""
    output = '<li class="cards__item">\n'
    output += f'<div class="card__title">{fox.get("name")}</div>\n'
    output += '<p class="card__text">\n'
    for cat, info in fox.items():
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
    for fox in animals_subdata:
        output += serialize_animal(fox)
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


def main():
    """Run the full animal processing and HTML generation pipeline.

    Loads JSON data, extracts reduced animal information, formats it
    into HTML, replaces the placeholder in the template, and writes
    the final output file. Prints status messages for all major steps."""
    animals_data = load_data(JSON_FILE)

    if animals_data:
        print("Data successfully loaded!")
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
        print(f"No file {JSON_FILE} found")


if __name__ == "__main__":
    main()
