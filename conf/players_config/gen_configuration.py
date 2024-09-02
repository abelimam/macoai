def get_genetic_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.2,
        "elite_rate": 0.2
    }
    if budget == 0.5:
        conf["population_size"] = 5
        conf["generations"] = 125
    elif budget == 1:
        conf["population_size"] = 5
        conf["generations"] = 125
    elif budget == 3:
        conf["population_size"] = 5
        conf["generations"] = 125
    elif budget == 5:
        conf["population_size"] = 5
        conf["generations"] = 125
    return conf