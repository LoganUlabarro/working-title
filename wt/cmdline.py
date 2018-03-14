"""Command-line interface to the program."""
import cmd
from pathlib import Path

from wt.io import yaml, load_cards
from wt.core import draw_cards


def _load_cfg(cfgpath):
    p = Path(cfgpath)
    cfg = yaml.load(p)
    names = cfg['players'].keys()
    classes = [cfg['players'][name]['class'] for name in names]
    return names, classes


def _find_name(allnames, target):
    for idx, name in enumerate(allnames):
        if target == name:
            return idx
    raise ValueError('invalid name provided')


class WtShell(cmd.Cmd):
    intro = 'Welcome to working-title, you sick fuck.'
    prompt = '(wt) '
    names, classes = [], []
    cards = load_cards('../data/cards')

    def do_load_cfg(self, path):
        """Load config from the specified path.

        Parameters
        ----------
        path : path_like
            pathlike object pointing to a game config yaml file.

        """
        self.names, self.classes = _load_cfg(path)

    def do_draw(self, line):
        """Draw ncards for player.

        Parameters
        ----------
        line : `str`
            (player, ncards)

        """
        player, ncards = line.split()
        ncards = int(ncards)
        class_ = self.classes[_find_name(self.names, player)]
        draw = draw_cards(class_, self.cards, ncards)
        ret = []
        for card in draw:
            ret.append(card['name'])
        print(ret)


if __name__ == '__main__':
    WtShell().cmdloop()
