from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as fmt
from configparser import ConfigParser


def init(doc=None):
    args = get_args(doc)
    cfg = read_config(args.config)
    return dict(cfg, config=args.config, refresh=args.refresh)


def get_args(doc):
    "Return the command-line arguments"
    parser = ArgumentParser(description=doc, formatter_class=fmt)

    add = parser.add_argument  # shortcut
    add('-c', '--config', default='clickdown.cfg', help='configuration file')
    add('-r', '--refresh', action='store_true', help='force refresh from url')

    return parser.parse_args()


def read_config(fname):
    cp = ConfigParser()
    with open(fname) as fp:
        cp.read_string('[top]\n' + fp.read())
    return cp['top']
