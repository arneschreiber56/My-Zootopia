"""MasterSchool Zootopia Codio Project"""
import data_fetcher
import html

NEW_HTML = "animals.html"
POINTER = "__REPLACE_ANIMALS_INFO__"


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


def write_html_animal(html_content):
    """Write the final HTML output to animals.html.

    Attempts to create or overwrite animals.html with the provided
    HTML content. Returns True on success, False on failure."""
    try:
        with open(NEW_HTML, "w") as fileobj:
            fileobj.write(html_content)
            return True
    #This exception is raised when a system function returns a system-related
    # error, including I/O failures such as “file not found” or “disk full”
    # (not for illegal argument types or other incidental errors).
    except OSError as e:
        print(e)
        return False


def replace_html_text(html_content, output):
    """Replace the placeholder in the HTML template with generated output.

    Searches the template for the predefined placeholder and replaces it
    with the provided HTML snippet. Replacement occurs only if the template
    exists and contains the placeholder exactly once.

    Returns the updated HTML string on success, or error message."""
    if html_content and html_content.count(POINTER) == 1:
        html_content_animal = html_content.replace(
            POINTER, output
        )
        print("Placeholder in HTML replaced!")
        return html_content_animal
    else:
        return "could not find HTML or add output data!"



def display_html_error_message(animal_query, html_content):
    """Insert an error message into the HTML template and write the output file.

    Escapes the user-provided query to prevent HTML injection, builds an
    error message, replaces the placeholder in the template, and writes the
    resulting HTML to the output file. Prints status messages indicating
    success or failure.

    Returns None"""
    # avoiding html injection:
    safe_query = html.escape(animal_query)
    error_message = (
        f"<h2>Could not find any animal in the database with your "
        f"search term {safe_query}!</h2>")
    html_content_error = replace_html_text(html_content, error_message)
    if write_html_animal(html_content_error):
        print("Request failed")
    else:
        print("Request and creation of HTML failed!")


def main():
    """Run the full animal processing and HTML generation pipeline.

    Loads JSON data, extracts reduced animal information, formats it
    into HTML, replaces the placeholder in the template, and writes
    the final output file. Prints status messages for all major steps."""
    html_content = data_fetcher.get_html_content()
    animal_query = data_fetcher.get_user_animal_query()
    animals_data = data_fetcher.get_response_json(animal_query)
    if not html_content:
        print("No HTML-Template found!")
        return
    if animals_data:
        print("Data successfully requested!")
        animals_subdata = create_reduced_animals_lst(animals_data)
        print("Reduced animals data list successfully created!")
        output = get_animal_info_output(animals_subdata)
        print("Animals info output successfully created!")
        html_content_animal = replace_html_text(html_content, output)
        if write_html_animal(html_content_animal):
            print("successfully created HTML animal.html!")
        else:
            print("could not create HTML animal.html!")
    else:
        display_html_error_message(animal_query, html_content)


if __name__ == "__main__":
    main()
