import json
from pprint import pprint


def load_data(file_path):
    """Loads a JSON file"""
    try:
        with open(file_path, "r") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return None


def get_check_animal_dict(animal):
    """checks if animal information are valid and returns a comprehensive
    dictionary of information about the animal"""

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
    """Gets the json-data in animals_data and extracts core information
    about foxes (name, diet, location(first value), type) from animals_data
    and returns it as a list of dictionaries with each fox information bundle a dictionary.
    When one item of information bundle is not found in the json file,
    the value should be None in the newly created dictionary"""
    fox_lst = []
    if animals_data:
        for animal in animals_data:
            if isinstance(animal, dict):
                animal_dict= get_check_animal_dict(animal)
                fox_lst.append(animal_dict)
        return fox_lst
    else:
        return []


def main():
    animals_data = load_data("animals_data.json")
    if animals_data:
        animals_subdata = create_reduced_animals_lst(animals_data)
        for fox in animals_subdata:
            for cat, info in fox.items():
                if info:
                    print(f"{cat}: {info}")
            print()
    else:
        print("No file 'animals_data.json' found")



if __name__ == "__main__":
    main()
