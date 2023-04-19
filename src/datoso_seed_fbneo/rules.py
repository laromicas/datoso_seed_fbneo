from datoso_seed_fbneo.dats import FbneoDat

rules = [
    {
        'name': 'Fbneo Dat',
        'class_name': FbneoDat,
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