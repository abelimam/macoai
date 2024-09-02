def get_montecarlotreesearch_conf(budget: int):
    if budget == 0.5 or budget == 1:
        return {"c_value": 4.2}
    elif budget == 3 or budget == 5:
        return {"c_value": 4.2}
    
def get_montecarlotreesearch_full_conf(budget: int):
    if budget == 0.5 or budget == 1:
        return {"c_value": 4.2, "full_rollout_on": True}
    elif budget == 3 or budget == 5:
        return {"c_value": 4.2, "full_rollout_on": True}
    
def get_bridgeburningmontecarlotreesearch_conf(budget: int):
    if budget == 0.5 or budget == 1:
        return {"c_value": 1.4}
    elif budget == 3 or budget == 5:
        return {"c_value": 1.4}