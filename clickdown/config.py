from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as fmt
from configparser import ConfigParser


def init(doc=None):
    "Return dict with config file properties and command-line arguments"
    args = get_args(doc)
    cfg = read_config(args.config)
    return dict(cfg, config=args.config, refresh=args.refresh)  # cfg + args


def get_args(doc):
    "Return the command-line arguments"
    parser = ArgumentParser(description=doc, formatter_class=fmt)

    add = parser.add_argument  # shortcut
    add('-c', '--config', default='clickdown.cfg', help='configuration file')
    add('-r', '--refresh', action='store_true', help='force refresh from url')

    return parser.parse_args()


def read_config(fname):
    valid_keys = ['token', 'team', 'user', 'ignored', 'cache_age_max',
                  'days_max', 'theme']

    cp = ConfigParser()
    cp.read_string('[top]\n' + open(fname).read())
    cfg = cp['top']

    for k in cfg.keys():
        assert k in valid_keys, f'Unknown property in config file {fname}: {k}'

    return cfg
