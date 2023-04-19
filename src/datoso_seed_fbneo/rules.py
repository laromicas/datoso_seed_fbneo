import datoso_seed_fbneo

rules = [
    {
        'name': 'Fbneo Dat',
        'class_name': datoso_seed_fbneo.dats.FbneoDat,
        'seed': 'nointro',
        'priority': 50,
        'rules': [
            {
                'key': 'url',
                'operator': 'contains',
                'value': 'www._fbneo.org'
            },
            {
                'key': 'homepage',
                'operator': 'eq',
                'value': '_fbneo'
            }
        ]
    }
]


def get_rules():
    return rules