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
    'Activities',
    'Shopping',
    'Miscellaneous'
]


ATTRACTION_TYPE_CATEGORY_MAPPING = {
    'Museum': 'Activities',
    'Art Gallery': 'Activities',
    'Historic Site': 'Activities',
    'Park': 'Activities',
    'Zoo': 'Activities',
    'Aquarium': 'Activities',
    'Amusement Park': 'Activities',
    'Theater': 'Activities',
    'Concert Hall': 'Activities',
    'Stadium': 'Activities',
    'Sports Complex': 'Activities',
    'Shopping Mall': 'Shopping',
    'Market': 'Shopping',
    'Restaurant': 'Food and Drink',
    'Bar': 'Food and Drink',
    'Nightclub': 'Activities'
}


class WSEvent:
    TRIP_SUGGESTION = 'trip_suggestion'
    IMAGE_READY = 'image_ready'


CURRENCY_MAPPING = {
    '$': 'usd'
}


CURRENCY_RATES_FROM_USD = {
    '€': 0.98,
    '₴': 37.85,
}
