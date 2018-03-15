"""Command-line interface to the program."""
import cmd
from pathlib import Path

from wt.io import yamlr, load_cards
from wt.core import draw_cards


def _load_cfg(cfgpath):
    p = Path(cfgpath)
    cfg = yamlr.load(p)
    names = list[cfg['players'].keys()]
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

    def do_players(self, _):
        """Print the names of the players in this game."""
        print(self.names)

    def do_class(self, player):
        """Reveal the class(es) of the given player.

        Parameters
        ----------
        player : `str`
            player name

        """
        idx = _find_name(self.names, player)
        print(self.classes[idx])


if __name__ == '__main__':
    WtShell().cmdloop()
