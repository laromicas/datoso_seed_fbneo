from datoso.configuration import config


def seed_args(parser):
    parser.add_argument('--fetch-full', type=bool, help='Fetch the full set of files.', default=True)
    parser.add_argument('--fetch-light', type=bool, help='Fetch the light set of files.', default=False)

def post_parser(args):
    if getattr(args, 'fetch_full', None):
        config.set('FBNEO', 'FetchFull', str(args.fetch_full))
    if getattr(args, 'fetch_light', None):
        config.set('FBNEO', 'FetchLight', str(args.fetch_light))

def init_config():
    if not config.has_section('FBNEO'):
        config['FBNEO'] = {
            'FetchFull': True,
            'FetchLight': False,
        }
