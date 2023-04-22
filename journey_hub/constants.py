class Roles:
    ADMIN = 'ADMIN'
    USER = 'USER'


ATTRACTION_TYPES = [
    'Museum',
    'Art Gallery',
    'Historic Site',
    'Park',
    'Zoo',
    'Aquarium',
    'Amusement Park',
    'Theater',
    'Concert Hall',
    'Stadium',
    'Sports Complex',
    'Shopping Mall',
    'Market',
    'Restaurant',
    'Bar',
    'Nightclub'
]


BUDGET_CATEGORIES = [
    'Accommodation',
    'Transportation',
    'Food and Drink',
    'Activities and Entertainment',
    'Shopping',
    'Miscellaneous'
]


ATTRACTION_TYPE_CATEGORY_MAPPING = {
    'Museum': 'Activities and Entertainment',
    'Art Gallery': 'Activities and Entertainment',
    'Historic Site': 'Activities and Entertainment',
    'Park': 'Activities and Entertainment',
    'Zoo': 'Activities and Entertainment',
    'Aquarium': 'Activities and Entertainment',
    'Amusement Park': 'Activities and Entertainment',
    'Theater': 'Activities and Entertainment',
    'Concert Hall': 'Activities and Entertainment',
    'Stadium': 'Activities and Entertainment',
    'Sports Complex': 'Activities and Entertainment',
    'Shopping Mall': 'Shopping',
    'Market': 'Shopping',
    'Restaurant': 'Food and Drink',
    'Bar': 'Food and Drink',
    'Nightclub': 'Activities and Entertainment'
}
