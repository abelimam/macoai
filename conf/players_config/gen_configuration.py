def get_genetic_conf(budget: int) -> dict:
    conf = {
        "mutation_rate": 0.2,
        "elite_rate": 0.1
    }
    if budget == 0.5:
        conf["population_size"] = 100
        conf["generations"] = 200
    elif budget == 1:
        conf["population_size"] = 100
        conf["generations"] = 200
    elif budget == 3:
        conf["population_size"] = 100
        conf["generations"] = 200
    elif budget == 5:
        conf["population_size"] = 100
        conf["generations"] = 200
    return conf