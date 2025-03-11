MAX_PROBLEM_LEN = 512

CURRENCY_CHOICES = [
    ('thb', 'THB'),
    ('usd', 'USD'),
    ('rub', 'RUB'),
]

FUEL_CHOICES = [
    ('Benzin', 'Benzin'),
    ('Dizel', 'Dizel'),
    ('Hybrid', 'Hybrid'),
    ('Turbo Dizel', 'Turbo Dizel'),
    ('Gaz', 'Gaz'),
    ('Electricity', 'Electricity'),
]

TRANSMISSION_CHOICES = [
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
    ('Automatic + Manual', 'Automatic + Manual'),
]

DRIVE_CHOICES = [
    ('Front wheel', 'Front wheel'),
    ('Rear wheel', 'Rear wheel'),
    ('4 wheels', '4 wheels'),
]

CATEGORY_DRIVES_LICENSE_CHOICES = [
    ('A', 'A'),
    ('A1', 'A1'),
    ('A or B or M', 'A or B or M'),
    ('B', 'B'),
    ('B1', 'B1'),
    ('BE', 'BE'),
    ('M', 'M'),
]

AIR_CONDITIONER_CHOICES = [
    ('Air conditioning', 'Air conditioning'),
    ('1-zone climate control', '1-zone climate control'),
    ('2-zone climate control', '2-zone climate control'),
    ('4-zone climate control', '4-zone climate control'),
    ('None', 'None'),
]

INTERIOR_CHOICES = [
    ('Fabric', 'Fabric'),
    ('Leather', 'Leather'),
    ('Sport', 'Sport'),
    ('Sport Leather', 'Sport Leather'),
]

ROOF_CHOICES = [
    ('Standard', 'Standard'),
    ('Sunroof', 'Sunroof'),
    ('Rigid foldable automatic', 'Rigid foldable automatic'),
    ('Soft foldable manual', 'Soft foldable manual'),
    ('Soft foldable automatic', 'Soft foldable automatic'),
]

POWERED_WINDOW_CHOICES = [
    (2, 2),
    (4, 4),
]

SIDE_WHEEL_CHOICES = [
    ('Left', 'Left'),
    ('Right', 'Right'),
]

COLOR_CHOICES = [
    ('White', 'White'),
    ('Black', 'Black'),
    ('Grey', 'Grey'),
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Yellow', 'Yellow'),
    ('Brown', 'Brown'),
    ('Beige', 'Beige'),
    ('Orange', 'Orange'),
    ('Silver', 'Silver'),
    ('Sky blue', 'Sky blue'),
    ('Purple', 'Purple'),
]

BODY_TYPE_CHOICES = [
    ('Sedan', 'Sedan'),
    ('Hatchback', 'Hatchback'),
    ('Wagon', 'Wagon'),
    ('Minivan', 'Minivan'),
    ('Minibus', 'Minibus'),
    ('Crossover', 'Crossover'),
    ('Pickup', 'Pickup'),
    ('Convertible', 'Convertible'),
    ('Scooter', 'Scooter'),
    ('Motorcycle', 'Motorcycle'),
    ('ATV', 'ATV'),
    ('Buggy', 'Buggy'),
    ('Coupe', 'Coupe'),
]

AGGREGATOR_CHOICES = [
    ('Localrent', 'Localrent'),
    ('Trip', 'Trip'),
    ('Klook', 'Klook'),
    ('Rentconnected', 'Rentconnected'),
]