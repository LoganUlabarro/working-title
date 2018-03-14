"""core functions."""

from pathlib import Path
from random import choices

import pandas as pd

from wt.io import glob_str, yaml


def __batch_prepare_card_uuids_and_versions(path):
    import uuid
    cards = []
    p = Path(path)
    files = p.glob(glob_str)
    for file in files:
        with open(file, 'r+') as fid:
            doc = yaml.load(fid)
            doc['version'] = 1
            doc['uuid'] = str(uuid.uuid4())
            cards.append(doc.copy())
            fid.seek(0)
            fid.truncate()
            yaml.dump(doc, fid)
    return cards


def draw_cards(classes, database, n=1):
    """Draws a card for the user.

    Parameters
    ----------
    classes : iterable
        iterable of class(es) to draw valid cards for
    database: `pd.DataFrame`
        card database
    n: `int`
        number of cards to draw

    Returns
    -------
    TODO: return type

    """
    card_masks = []
    for class_ in classes:
        card_masks.append(database['class'] == class_)

    mask = pd.concat(card_masks, axis=1).any(axis=1)
    valid_cards = database[mask]

    # merger = partial(pd.merge, on='uuid', how='outer')
    # valid_cards = reduce(merger, card_subsets)
    uuids = valid_cards.uuid.values
    weights = valid_cards.draw_chance.values
    id_ = choices(uuids, weights, k=n)
    outmask = database.uuid.isin(id_)
    chosen_cards = database[outmask]
    dictionaries = chosen_cards.to_dict(orient='records')
    return dictionaries
