from macaw.configs import FIELD_NAMES


def normalize_plan(plan: dict[str, str], origin: str) -> dict[str, str]:
    '''maps the plan keys (in lowercase!!!!!!)
    to the project's standard'''
    result = {}
    result[FIELD_NAMES[0]] = origin
    for key in plan.keys():
        match [key.lower()]:
            case ['cpu'] | ['vcpu'] | ['cputype']:
                result[FIELD_NAMES[1]] = plan[key]

            case ['memory'] | ['cpuamount']:
                result[FIELD_NAMES[2]] = plan[key]

            case ['storage'] | ['ssd disk'] | ['ssdamount']:
                result[FIELD_NAMES[3]] = plan[key]

            case ['bandwidth'] | ['transfer'] | ['transferamount']:
                result[FIELD_NAMES[4]] = plan[key]

            case ['/mo'] | ['usd_rate_per_month']:
                result[FIELD_NAMES[5]] = plan[key]

    return result
