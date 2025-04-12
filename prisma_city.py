import requests

def get_pokemon_types():
    url = "https://pokeapi.co/api/v2/type/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["results"]

def get_pokemon_by_type(type_url):
    response = requests.get(type_url)
    response.raise_for_status()
    return response.json()["pokemon"]

def get_all_pokemon_data():
    url = "https://pokeapi.co/api/v2/pokemon/"
    all_pokemon_data = {}
    limit = 100  # Número de Pokémon por solicitud
    offset = 0

    while True:
        response = requests.get(url, params={"limit": limit, "offset": offset})
        response.raise_for_status()
        data = response.json()
        for pokemon in data["results"]:
            all_pokemon_data[pokemon["name"]] = pokemon["url"]

        if not data["next"]:  # Si no hay más páginas, sal del bucle
            break
        offset += limit

    return all_pokemon_data

def get_pokemon_height_from_cache(pokemon_name, pokemon_url, cache):
    if pokemon_name in cache:
        return cache[pokemon_name]
    response = requests.get(pokemon_url)
    response.raise_for_status()
    height = response.json()["height"]
    cache[pokemon_name] = height
    return height

def calculate_average_height():
    types = get_pokemon_types()
    all_pokemon_data = get_all_pokemon_data()
    print("all_pokemon_data", len(all_pokemon_data))
    type_heights = {}
    height_cache = {}

    for type_info in types:
        type_name = type_info["name"]
        print("type_name", type_name)
        pokemon_list = get_pokemon_by_type(type_info["url"])
        heights = []

        for pokemon_entry in pokemon_list:
            pokemon_name = pokemon_entry["pokemon"]["name"]
            pokemon_url = all_pokemon_data.get(pokemon_name)
            if pokemon_url:
                height = get_pokemon_height_from_cache(pokemon_name, pokemon_url, height_cache)
                heights.append(height)

        if heights:
            average_height = sum(heights) / len(heights)
            type_heights[type_name] = round(average_height, 3)

    # Ordenar alfabéticamente por tipo
    sorted_heights = dict(sorted(type_heights.items()))
    return sorted_heights

if __name__ == "__main__":
    print("Starting")
    average_heights = calculate_average_height()
    for type_name, avg_height in average_heights.items():
        print(f"{type_name}: {avg_height}")