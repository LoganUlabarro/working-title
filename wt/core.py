"""core functions."""

import json
from pathlib import Path
from functools import reduce, partial

import yaml
import pandas as pd


def __batch_prepare_card_uuids_and_versions(path):
    import uuid
    cards = []
    p = Path(path)
    files = p.glob('*.yaml')
    for file in files:
        with open(file, 'r+') as fid:
            doc = yaml.load(fid)
            doc['uuid'] = str(uuid.uuid4())
            doc['version'] = 1
            cards.append(doc.copy())
            fid.seek(0)
            fid.truncate()
            # yaml.dump(doc, fid)
    return cards


def load_schema(path):
    """Load the card schema from disk.

    Parameters
    ----------
    path : path_like
        location of the schema yaml file

    Returns
    -------
    `dict`
        dictionary schema

    """
    with open(path, 'r') as fid:
        return yaml.load(fid)


data_root = Path(__file__).parent / '..' / 'data'
schema_path = data_root / 'card-schema.yaml'
schema = load_schema(schema_path)


def validate_card(card, schema=schema_path):
    """Validate that the card is correctly formed.

    Parameters
    ----------
    card : `dict`
        a card
    schema: `dict`
        valid card schema

    Returns
    -------
    `dict`
        card dictionary

    Raises
    ------
    ValueError
        if card is malformed

    Notes
    -----
    TODO: re-organize to loop over the schema and check all properties of schema
    on card, find iterable card fields and do sub-iteration on that.

    """

    error_strs = []
    if 'name' not in card:
        error_strs.append('card does not have a name.')
        base_str1 = 'nameless card'
    else:
        base_str1 = card['name']

    base_str2 = base_str1 + ' does not have a '

    if 'uuid' not in card:
        error_strs.append(base_str2 + 'uuid.')

    if 'class' not in card:
        error_strs.append(base_str2 + 'class.')
    else:
        if card['class'] not in schema['class']:
            error_strs.append(base_str1 + ' invalid class.')

    if 'rarity' not in card:
        error_strs.append(base_str2 + 'rarity.')
    else:
        if card['rarity'] not in schema['rarity'].keys():
            error_strs.append(base_str1 + ' invalid rarity.')

    if 'types' not in card:
        error_strs.append(base_str2 + 'type(s).')
        for type_ in card['types']:
            if type_ not in schema['types']:
                error_strs.append(base_str1 + ' invalid type.')
    if 'cost' not in card:
        error_strs.append(base_str2 + 'cost.')
    else:
        if card['cost'] not in schema['cost']:
            error_strs.append(base_str1 + 'invalid cost.')
    if 'version' not in card:
        error_strs.append(base_str2 + 'version.')
    if 'description' not in card:
        error_strs.append(base_str2 + 'description.')
    else:
        try:
            iterator = iter(card['description'])
            for idx, item in enumerate(iterator):
                if not item.endswith(('.', ',', ')')):
                    error_strs.append(base_str1 + f' description line {idx+1} improper ending.')
        except TypeError:
            error_strs.append(base_str1 + 'description is not formatted as an iterable.')

    # if error_strs:
    #     error = '\n'.join(error_strs)
    #     raise ValueError(error)
    return card


def load_card(data, schema=schema):
    """Validate that the card is correctly formed.

    Parameters
    ----------
    data : `dict`
        raw card data
    schema : `dict`
        card schema dictionary

    Returns
    -------
    `dict`
        card dictionary

    Raises
    ------
    ValueError
        if data is malformed

    """
    out = data.copy()
    out['description'] = '\n'.join(data['description'])
    out['draw_chance'] = 1 / schema['rarity'][data['rarity']]
    return out


def load_cards(directory, schema=schema):
    """Load all cards in a directory.

    Parameters
    ----------
    directory: path_like
        location full of card yaml files

    Returns
    -------
    `pandas.DataFrame`

    """
    p = Path(directory)
    files = p.glob('*.yaml')
    cards = []
    for file in files:
        with open(file, 'r') as fid:
            data = validate_card(yaml.load(fid), schema)
            card = load_card(data, schema)
            cards.append(card)
    return pd.DataFrame(cards)


def cards_to_probabilities(database, schema=schema):
    """Create

    Parameters
    ----------
    database : `pd.DataFrame`
        database of cards

    Returns
    -------
    `list`
        list with duplicate entries for cards with non unity probability

    """
    multiplier = 1 / database.draw_chance.min()
    total_chance = int(database.draw_chance.sum() * multiplier)
    rares = database.query('rarity == "rare"').name.values
    uncommons = database.query('rarity == "uncommon"').name.values
    commons = database.query('rarity == "common"').name.values

    out = []



def draw_card(user, database):
    """Draws a card for the user.

    Parameters
    ----------
    user : `dict`
        dictionary with attr class
    database: `pd.DataFrame`
        card database

    Returns
    -------
    TODO: return type

    """
    user_classes = user['class']
    card_subsets = []
    for class_ in user_classes:
        card_subsets.append(database.query(f'class == {class_}'))

    merger = partial(pd.merge, on='uuid', how='outer')
    valid_cards = reduce(merger, card_subsets)

