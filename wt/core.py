"""core functions."""

import glob
import json
from pathlib import Path

import yaml


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
        if card['rarity'] not in schema['rarity']:
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

    if error_strs:
        error = '\n'.join(error_strs)
        raise ValueError(error)
    else:
        return card


def load_card(card_dict):
    """Validate that the card is correctly formed.

    Parameters
    ----------
    card_dict : `dict`
        dictionary representation of card

    Returns
    -------
    `dict`
        card dictionary

    Raises
    ------
    ValueError
        if card is malformed

    """
    pass


def load_cards(directory):
    """Load all cards in a directory.

    Parameters
    ----------
    directory: path_like
        location full of card yaml files

    Returns
    -------
    todo

    """
    p = Path(directory)
    files = glob.iglob(p / '*.yaml')
    out = {}
    for file in files:
        with open(file, 'r') as fid:
            data = yaml.load(fid)
    #         key = data['uuid']
    #         out{key} = data
    # return out
