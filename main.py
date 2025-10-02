import json
from dataclasses import dataclass
from typing import Union

from fastapi import FastAPI


with open('pokemons.json', 'r') as file:
    pokemons_list = json.load(file)

list_pokemons = {k+1:v for k, v in enumerate(pokemons_list)}


@dataclass
class Pokemon:
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
    evolution_id: Union[int, None]= None


app = FastAPI()