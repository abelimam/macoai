def get_onlineevolution_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.15,
        "survival_rate": 0.15
    }
    if budget == 0.5:
        conf["population_size"] = 125
    elif budget == 1:
        conf["population_size"] = 125
    elif budget == 3:
        conf["population_size"] = 125
    elif budget == 5:
        conf["population_size"] = 125
    return conf

def get_onlineevolution_random_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.15,
        "survival_rate": 0.15,
        "random_new_valid_action": True
    }
    if budget == 0.5:
        conf["population_size"] = 125
    elif budget == 1:
        conf["population_size"] = 125
    elif budget == 3:
        conf["population_size"] = 125
    elif budget == 5:
        conf["population_size"] = 125
    return conf