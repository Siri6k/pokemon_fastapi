import json
from dataclasses import asdict, dataclass
from typing import Union

from fastapi import FastAPI, HTTPException, Path


with open('pokemons.json', 'r') as file:
    pokemons_list = json.load(file)

list_pokemons = {k+1:v for k, v in enumerate(pokemons_list)}


@dataclass
class Pokemon():
    id: int
    name: str
    types: list[str]
    total: int
    hp: int
    attack: int
    defense: int
    attack_special: int
    defense_special: int
    speed: int
    evolution_id: Union[int, None] = None


app = FastAPI()


# Routes
# GET, POST, PUT, DELETE

@app.get('/total_pokemons')
def get_total_pokemons() -> dict:
    return {"total": len(list_pokemons)}

@app.get('/pokemons')
def get_all_pokemons() -> list[Pokemon]:
    res = []
    for id in list_pokemons:
        res.append(Pokemon(**list_pokemons[id]))
    return res

@app.get('/pokemons/{id}')
def get_pokemon_by_id(id: int = Path(ge=1)) -> Pokemon:
    if id not in list_pokemons:
        raise HTTPException(
            status_code=404, 
            detail="Ce pokemon n'existe pas"
            )
    
    return Pokemon(**list_pokemons[id])

@app.post('/pokemon/')
def create_pokemon(pokemon: Pokemon) -> Pokemon:
    if pokemon.id in list_pokemons:
        raise HTTPException(
            status_code=404,
            detail=f"Un pokemon avec cet ID: ({pokemon.id}) existe déjà"
        )
    list_pokemons[pokemon.id] = asdict(pokemon)
    return Pokemon(**list_pokemons[pokemon.id])

@app.put('/pokemon/{id}')
def update_pokemon(pokemon: Pokemon, id: int = Path(ge=1)) -> Pokemon:
    if id not in list_pokemons:
        raise HTTPException(
            status_code=404,
            detail="Le pokemon que vous essayez de modifier n'existe pas"
        )
    
    list_pokemons[pokemon.id] = asdict(pokemon)
    return Pokemon(**list_pokemons[pokemon.id])

@app.delete('/pokemon/{id}')
def delete_pokemon(id: int = Path(ge=1)) -> Pokemon:
    if id not in list_pokemons:
        raise HTTPException(
            status_code=404,
            detail="Le pokemon que vous essayez de supprimer n'existe pas"
        )
    
    deleted_pokemon = Pokemon(**list_pokemons[id])
    del list_pokemons[id]
    return deleted_pokemon
