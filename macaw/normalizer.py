FIELD_NAMES = ['CPU / VCPU', 'MEMORY', 'STORAGE / SSD DISK',
               'BANDWIDTH / TRANSFER', 'PRICE [$/mo]']


def normalize_plan(plan: dict[str, str]) -> dict[str, str]:
    '''maps the plan keys to the project standard'''
    result = {}
    for key in plan.keys():
        match [key.lower()]:
            case ['cpu'] | ['vcpu']:
                result[FIELD_NAMES[0]] = plan[key]
            case ['memory']:
                result[FIELD_NAMES[1]] = plan[key]
            case ['storage'] | ['ssd disk']:
                result[FIELD_NAMES[2]] = plan[key]
            case ['bandwidth'] | ['transfer']:
                result[FIELD_NAMES[3]] = plan[key]
            case ['/mo']:
                result[FIELD_NAMES[4]] = plan[key]
    return result
