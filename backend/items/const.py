MAX_PROBLEM_LEN = 512

CURRENCY_CHOICES = [
    ('Thb', 'thb'),
    ('Usd', 'usd'),
    ('Rub', 'rub'),
]

DOORS_CHOICES = [
    (2, '2'),
    (4, '4'),
]

AIRBAGS_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
]

BRAND_CHOICES = [
    ('Toyota', 'toyota'),
    ('BMW', 'bmw'),
    ('Mercedes-Benz', 'mercedes_benz'),
    ('Audi', 'audi'),
    ('Ford', 'ford'),
    ('Chevrolet', 'chevrolet'),
    ('Honda', 'honda'),
    ('Nissan', 'nissan'),
    ('Hyundai', 'hyundai'),
    ('Volkswagen', 'volkswagen'),
]

FUEL_CHOICES = [
    ('Benzin', 'benzin'),
    ('Dizel', 'dizel'),
    ('Hybrid', 'hybrid'),
    ('Turbo Dizel', 'turbo dizel'),
    ('Gaz', 'gaz'),
    ('Electricity', 'electricity'),
]

TRANSMISSION_CHOICES = [
    ('Manual', 'manual'),
    ('Automatic', 'automatic'),
    ('Automatic + Manual', 'automatic + manual'),
]

DRIVE_CHOICES = [
    ('Front wheel', 'front wheel'),
    ('Rear wheel', 'rear wheel'),
    ('4 wheels', '4 wheels'),
]

CATEGORY_DRIVES_LICENSE_CHOICES = [
    ('A', 'a'),
    ('A1', 'a1'),
    ('A or B or M', 'a or b or m'),
    ('B', 'b'),
    ('B1', 'b1'),
    ('BE', 'be'),
    ('M', 'm'),
]

AIR_CONDITIONER_CHOICES = [
    ('Air conditioning', 'air conditioning'),
    ('1-zone climate control', '1-zone climate control'),
    ('2-zone climate control', '2-zone climate control'),
    ('4-zone climate control', '4-zone climate control'),
    ('-', '-'),
]

INTERIOR_CHOICES = [
    ('Fabric', 'fabric'),
    ('Leather', 'leather'),
    ('Sport', 'sport'),
    ('Sport Leather', 'sport leather'),
]

ROOF_CHOICES = [
    ('Standard', 'standard'),
    ('Sunroof', 'sunroof'),
    ('Rigid foldable automatic', 'rigid foldable automatic'),
    ('Soft foldable manual', 'soft foldable manual'),
    ('Soft foldable automatic', 'soft foldable automatic'),
]

POWERED_WINDOW_CHOICES = [
    (2, '2'),
    (4, '4'),
]

SIDE_WHEEL_CHOICES = [
    ('Left', 'left'),
    ('Right', 'right'),
]

COLOR_CHOICES = [
    ('White', 'white'),
    ('Black', 'black'),
    ('Grey', 'grey'),
    ('Red', 'red'),
    ('Blue', 'blue'),
    ('Green', 'green'),
    ('Yellow', 'yellow'),
    ('Brown', 'brown'),
    ('Beige', 'beige'),
    ('Orange', 'orange'),
    ('Silver', 'silver'),
    ('Sky blue', 'sky blue'),
    ('Purple', 'purple'),
]

BODY_TYPE_CHOICES = [
    ('Sedan', 'sedan'),
    ('Hatchback', 'hatchback'),
    ('Wagon', 'wagon'),
    ('Minivan', 'minivan'),
    ('Minibus', 'minibus'),
    ('Crossover', 'crossover'),
    ('Pickup', 'pickup'),
    ('Convertible', 'convertible'),
    ('Scooter', 'scooter'),
    ('Motorcycle', 'motorcycle'),
    ('ATV', 'atv'),
    ('Buggy', 'buggy'),
    ('Coupe', 'coupe'),
]

AGREGATOR_CHOICES = [
    ('Localrent', 'localrent'),
    ('Trip', 'trip'),
    ('Klook', 'klook'),
    ('Rentconnected', 'rentconnected'),
]

STATUS_CHOICES = [
    ('Active', 'active'),
    ('Closed', 'closed'),
    ('Expired', 'expired'),
]

CONTACT_CHOICES = [
    ('Phone', 'phone'),
    ('Telegram', 'telegram'),
    ('WhatsApp', 'whatsapp'),
    ('Viber', 'viber'),
]

BABY_SEAT_CHOICES = [
    ('-', '-'),
    ('Baby seat low', 'baby seat low'),
    ('Baby seat high', 'baby seat high'),
    ('Booster', 'booster'),
]

ANOTHER_REGIONS_CHOICES = [
    ('-', '-'),
    (
        'Southern provinces (Phuket, Phang Nga, Krabi-mainland)',
        'southern provinces (phuket, phang nga, krabi-mainland)'
    ),
    (
        'Islands (Phangan, Samui)',
        'islands (phangan, samui)'
    ),
    (
        'Central Provinces (Bangkok, Pattaya, Hua Hin)',
        'central provinces (bangkok, pattaya, hua hin)'
    ),
    (
        'Northern Provinces (Chiang Mai)',
        'northern provinces (chiang mai)'
    ),
]

COMPLEX_INSURANCE_CHOICES = [
    ('-', '-'),
    ('Full insurance', 'full insurance'),
    ('Super Insurance', 'super insurance'),
]
