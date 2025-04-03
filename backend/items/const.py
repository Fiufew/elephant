MAX_PROBLEM_LEN = 512

CURRENCY_CHOICES = [
    ('THB', 'thb'),
    ('USD', 'usd'),
    ('RUB', 'rub'),
]

DOORS_CHOICES = [
    (2, 2),
    (4, 4),
]

AIRBAGS_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
]

BRAND_CHOICES = [
    ('toyota', 'Toyota'),
    ('bmw', 'BMW'),
    ('mercedes_benz', 'Mercedes-Benz'),
    ('audi', 'Audi'),
    ('ford', 'Ford'),
    ('chevrolet', 'Chevrolet'),
    ('honda', 'Honda'),
    ('nissan', 'Nissan'),
    ('hyundai', 'Hyundai'),
    ('volkswagen', 'Volkswagen'),
]

FUEL_CHOICES = [
    ('benzin', 'Benzin'),
    ('dizel', 'Dizel'),
    ('hybrid', 'Hybrid'),
    ('turbo dizel', 'Turbo Dizel'),
    ('gaz', 'Gaz'),
    ('electricity', 'Electricity'),
]

TRANSMISSION_CHOICES = [
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
    ('automatic + manual', 'Automatic + Manual'),
]

DRIVE_CHOICES = [
    ('front wheel', 'Front wheel'),
    ('rear wheel', 'Rear wheel'),
    ('4 wheels', '4 wheels'),
]

CATEGORY_DRIVES_LICENSE_CHOICES = [
    ('a', 'A'),
    ('a1', 'A1'),
    ('a or b or m', 'A or B or M'),
    ('b', 'B'),
    ('b1', 'B1'),
    ('be', 'BE'),
    ('m', 'M'),
]

AIR_CONDITIONER_CHOICES = [
    ('air conditioning', 'Air conditioning'),
    ('1-zone climate control', '1-zone climate control'),
    ('2-zone climate control', '2-zone climate control'),
    ('4-zone climate control', '4-zone climate control'),
    ('none', 'None'),
]

INTERIOR_CHOICES = [
    ('fabric', 'Fabric'),
    ('leather', 'Leather'),
    ('sport', 'Sport'),
    ('sport leather', 'Sport Leather'),
]

ROOF_CHOICES = [
    ('standard', 'Standard'),
    ('sunroof', 'Sunroof'),
    ('rigid foldable automatic', 'Rigid foldable automatic'),
    ('soft foldable manual', 'Soft foldable manual'),
    ('soft foldable automatic', 'Soft foldable automatic'),
]

POWERED_WINDOW_CHOICES = [
    (2, 2),
    (4, 4),
]

SIDE_WHEEL_CHOICES = [
    ('left', 'Left'),
    ('right', 'Right'),
]

COLOR_CHOICES = [
    ('white', 'White'),
    ('black', 'Black'),
    ('grey', 'Grey'),
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('yellow', 'Yellow'),
    ('brown', 'Brown'),
    ('beige', 'Beige'),
    ('orange', 'Orange'),
    ('silver', 'Silver'),
    ('sky blue', 'Sky blue'),
    ('purple', 'Purple'),
]

BODY_TYPE_CHOICES = [
    ('sedan', 'Sedan'),
    ('hatchback', 'Hatchback'),
    ('wagon', 'Wagon'),
    ('minivan', 'Minivan'),
    ('minibus', 'Minibus'),
    ('crossover', 'Crossover'),
    ('pickup', 'Pickup'),
    ('convertible', 'Convertible'),
    ('scooter', 'Scooter'),
    ('motorcycle', 'Motorcycle'),
    ('atv', 'ATV'),
    ('buggy', 'Buggy'),
    ('coupe', 'Coupe'),
]

AGGREGATOR_CHOICES = [
    ('localrent', 'Localrent'),
    ('trip', 'Trip'),
    ('klook', 'Klook'),
    ('rentconnected', 'Rentconnected'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('closed', 'Closed'),
    ('expired', 'Expired')
]

CONTACT_CHOICES = [
    ('phone', 'Phone'),
    ('telegram', 'Telegram'),
    ('whatsapp', 'WhatsApp'),
    ('viber', 'Viber')
]
