from flask import Flask,render_template,request
import requests


app = Flask(__name__)

@app.route('/')
def welcome():
   return 'Hello welcome to my pokemon class built with flack'

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
   print(request.method)

   pokemon_names = ["bulbasaur", "charmander", "squirtle", "pikachu", "eevee"]

   pokemon_data = {} # created a empty dictionary which i will store in my pokemon data 

   name = request.form.get('name')
   for name in pokemon_names:
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    if response.status_code == 200: # if th response is 200 I want to make request to the api 
        pokemon_json = response.json()
        abilities = [ability['ability']['name'] for ability in pokemon_json['abilities']]
        sprite_url = pokemon_json['sprites']['front_shiny']
        base_experience = pokemon_json['base_experience']
        attack_base_stat = pokemon_json['stats'][1]['base_stat']
        hp_base_stat = pokemon_json['stats'][0]['base_stat']
        defense_base_stat = pokemon_json['stats'][2]['base_stat']
        
        #store my pokemon data into my empty dictionery 
        pokemon_data[name] = {
            
            "abilities": abilities,
            "sprite_url": sprite_url,
            "base_experience": base_experience,
            "attack_base_stat": attack_base_stat,
            "hp_base_stat": hp_base_stat,
            "defense_base_stat": defense_base_stat
        }
    else:
        # If th request is 404 I want to return error message 
        print(f'Error retrieving data for {name}: {response.status_code}')

    for name, data in pokemon_data.items():
        print(f"Pokemon: {name}")
        print(f"Abilities: {', '.join(data['abilities'])}")
        print(f"Sprite URL: {data['sprite_url']}")
        print(f"Base Experience: {data['base_experience']}")
        print(f"Attack Base Stat: {data['attack_base_stat']}")
        print(f"HP Base Stat: {data['hp_base_stat']}")
        print(f"Defense Base Stat: {data['defense_base_stat']}")
        print()
   return render_template('pokemon.html', pokemon_data = pokemon_data, name = name, data=data)

