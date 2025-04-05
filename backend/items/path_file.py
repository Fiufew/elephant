def applications_path(instance, filename):
    if instance.application and instance.application.num:
        return f'files/applications/Application_{instance.application.num}/{filename}'
    return 'files/applications/noname/{filename}'


def applications_path_for_other_contract(instance, filename):
    if instance.application and instance.application.num:
        return f'files/applications/Application_{instance.application.num}/contracts_agregator/{filename}'
    return 'files/applications/noname/{filename}'


def applications_path_for_other_vaucher(instance, filename):
    if instance.application and instance.application.num:
        return f'files/applications/Application_{instance.application.num}/vauchers_agregator/{filename}'
    return 'files/applications/noname/{filename}'


def bluebook_upload_path(instance, filename):
    if hasattr(instance, 'car') and instance.car and instance.car.number:
        clean_name = f'{instance.car.brand} {instance.car.model} {instance.car.number} {instance.car.color}'
        return f'files/cars/{clean_name}/bluebook/{filename}'
    return f'files/cars/unknown/{filename}'


def car_photo_upload_path(instance, filename):
    if instance.car and instance.car.number:
        clean_name = f'{instance.car.brand} {instance.car.model} {instance.car.number} {instance.car.color}'
        return f'files/cars/{clean_name}/photos/{filename}'
    return f'files/cars/unknown/photos/{filename}'
