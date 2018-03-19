"""core functions."""

from pathlib import Path
from random import choices

import numpy as np
import pandas as pd

from wt.io import glob_str, yamlr, yamlw


def __batch_prepare_card_uuids_and_versions(path):
    import uuid
    cards = []
    p = Path(path)
    files = p.glob(glob_str)
    for file in files:
        with open(file, 'r+') as fid:
            doc = yamlr.load(fid)
            doc['version'] = 1
            doc['uuid'] = str(uuid.uuid4())
            cards.append(doc.copy())
            fid.seek(0)
            fid.truncate()
            yamlw.dump(doc, fid)
    return cards


def prep_cards(database, classes, types=None):
    """Prepares the set of valid cards for a search on classes and types.

    Parameters
    ----------
    database: `pd.DataFrame`
        card database
    classes : iterable
        iterable of class(es) to draw valid cards for
    types : iterable, optional
        types to further filter by; card can be any of the specified types

    Returns
    -------
    `pandas.DataFrame`
        filtered dataframe of valid cards

    """
    # begin all valid sets with all generic cards
    class_masks = [database['class'] == 'generic']

    # for each class specified, create a mask on the database of cards which have that class
    for class_ in classes:
        class_masks.append(database['class'] == class_)

    # concatonate the masks and accept values where any mask passes
    class_mask = pd.concat(class_masks, axis=1).any(axis=1)
    total_mask = class_mask

    # if some card types are specified, repeat class masking for types
    if types:
        types_masks = []
        for type_ in types:
            types_masks.append(database[database['types'].apply(lambda x: type_ in x)])
        type_mask = pd.concat(types_masks, axis=1).any(axis=1)

        # finally, find the mask which satisfies both the class and type masks simultaneously
        total_mask = pd.concat((class_mask, type_mask), axis=1)
        total_mask = total_mask.replace(np.NaN, False).all(axis=1)

    return database[total_mask]  # return cards satisfying this mask


def draw_cards(valid_cards, n=1):
    """Draw card(s).

    Parameters
    ----------
    valid_cards: `pd.DataFrame`
        card database
    n: `int`
        number of cards to draw

    Returns
    -------
    iterable of `dict`s
        iterable containing a dict for each card

    """
    uuids = valid_cards.uuid.values
    weights = valid_cards.draw_chance.values
    id_ = choices(uuids, weights, k=n)
    outmask = valid_cards.uuid.isin(id_)
    chosen_cards = valid_cards[outmask]
    dictionaries = chosen_cards.to_dict(orient='records')
    return dictionaries


def prep_and_draw_cards(database, classes, types=None, n=1):
    """Prepares valid cards and draws a card for the user.

    This is a macro that calls the preparation and draw functions, it is a convenience function
    for when the valid cards for a particular case are not already cached.

    Parameters
    ----------
    valid_cards: `pd.DataFrame`
        card database
    classes : iterable
        iterable of class(es) to draw valid cards for
    types : iterable, optional
        types to further filter by; card can be any of the specified types
    n: `int`
        number of cards to draw

    Returns
    -------
    iterable of `dict`s
        iterable containing a dict for each card

    """
    valid_cards = prep_cards(database, classes, types)
    return draw_cards(valid_cards, n)
