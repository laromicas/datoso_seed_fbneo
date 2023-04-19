from datoso_seed_fbneo.dats import FbneoDat

rules = [
    {
        'name': 'Fbneo Dat',
        '_class': FbneoDat,
        'seed': 'nointro',
        'priority': 50,
        'rules': [
            {
                'key': 'url',
                'operator': 'contains',
                'value': 'neo-source.com'
            },
            {
                'key': 'author',
                'operator': 'eq',
                'value': 'FinalBurn Neo'
            }
        ]
    }
]


def get_rules():
    return rules