def get_onlineevolution_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.2,
        "survival_rate": 0.5
    }
    if budget == 0.5:
        conf["population_size"] = 100
    elif budget == 1:
        conf["population_size"] = 150
    elif budget == 3:
        conf["population_size"] = 200
    elif budget == 5:
        conf["population_size"] = 250
    return conf

def get_onlineevolution_random_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.2,
        "survival_rate": 0.5,
        "random_new_valid_action": True
    }
    if budget == 0.5:
        conf["population_size"] = 100
    elif budget == 1:
        conf["population_size"] = 150
    elif budget == 3:
        conf["population_size"] = 200
    elif budget == 5:
        conf["population_size"] = 250
    return conf