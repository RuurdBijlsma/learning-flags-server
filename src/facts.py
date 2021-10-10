import pathlib
from typing import List

import pandas as pd

from spacingmodel import SpacingModel, Fact


def load_facts(model: SpacingModel) -> None:
    facts = merge_data()

    for fact in facts:
        model.add_fact(fact)

    model.normalize_properties({'longitude': 0.5, 'latitude': 0.5, 'population': 1})


def merge_data() -> List[Fact]:
    base_path = pathlib.Path('../data')
    countries = pd.read_json(base_path / 'countries.json', orient='index')
    population = pd.read_csv(base_path / 'population.csv', index_col=['cca2'])
    location = pd.read_csv(base_path / 'flags-latlng.tsv', sep='\t', index_col='country')

    countries.columns = ['name']
    countries['population'] = population['pop2021']
    countries['latitude'] = location['latitude']
    countries['longitude'] = location['longitude']

    facts = []
    for idx, (country, properties) in enumerate(countries.iterrows()):
        name = properties['name']
        population = properties['population']
        longitude = properties['longitude']
        latitude = properties['latitude']

        if any(v is None for v in (population, longitude, latitude)):
            continue

        facts.append(Fact(
            fact_id=idx,
            question=country,
            answer=name,
            properties={
                'population': population,
                'longitude': longitude,
                'latitude': latitude,
            },
        ))

    return facts


if __name__ == '__main__':
    merge_data()