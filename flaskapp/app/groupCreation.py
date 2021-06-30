import numpy as np
import networkx as nx
import pulp
from apis.v1.utils.random_stuff import get_random_color, generate_team_name
from dataclasses import dataclass

from typing import Any
# used solution for wedding seating problem


@dataclass
class Group:
    name: str
    color: str
    members: Any


def create_groups():
    # todo: @marina I need the saved lectures with its attendants
    lectures = {"Audiokommunikation: 21S": ["uid1", "uid2", "uid3"],
                "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S": ["uid3", "uid5"],
                "Echtzeit-Computergrafik (IN0038): 21S": ["uid1", "uid2", "uid4", "uid5"]} # remove this line after db integration
    social_network = nx.Graph()
    for title, attendants in lectures.items():
        social_network.add_nodes_from(attendants)

    for users in lectures.values():
        for i in range(0, len(users) - 1):
            for j in range(i + 1, len(users)):
                if social_network.has_edge(users[i], users[j]):
                    social_network[users[i]][users[j]]['weight'] += (1 / len(users))
                    social_network[users[i]][users[j]]['counter'] += 1
                else:
                    social_network.add_edge(users[i], users[j], weight=(1 / len(users)), counter=1)
    for u, v, d in social_network.edges(data=True):
        d['weight'] = d['weight']/d['counter']

    max_groups = len(social_network.nodes)/5
    max_group_size = 5

    # create list of all possible tables
    possible_groups = [tuple(c) for c in pulp.allcombinations(social_network.nodes, max_group_size)]

    # create a binary variable to state that a table setting is used
    x = pulp.LpVariable.dicts('table', possible_groups,
                              lowBound=0,
                              upBound=1,
                              cat=pulp.LpInteger)
    seating_model = pulp.LpProblem("Wedding-Seating-Model", pulp.LpMinimize)
    seating_model += sum([happiness(group, social_network) * x[group] for group in possible_groups])

    # specify the maximum number of groups
    seating_model += sum([x[group] for group in possible_groups]) <= max_groups, \
                     "Maximum_number_of_tables"
    for user in social_network.nodes:
        seating_model += sum([x[group] for group in possible_groups
                             if user in group]) == 1, "Must_seat_%s" % user
    seating_model.solve()
    user_groups = []
    for group in possible_groups:
        if x[group].value() == 1.0:
            user_groups.append(Group(generate_team_name(), get_random_color(), group))
    user_groups = [["uid1", "uid3", "uid5"], ["udi2", "uid4"]] # remove this line after db integration
    #todo: @Robin teamname generator and color generator fills data
    user_groups = {"Teamname1": ["uid1", "uid3", "uid5"], "Teamname2": ["udi2", "uid4"]}
    group_colors = {"Teamname1": "rot", "Teamname2": "blau"}
    # todo: @Marina: please fill the database with the user_groups{list{str}}
    pass


def happiness(group, social_network):
    """
    find the happiness a group of people have inbetween themself
    :param social_network:
    :param group:
    :return:
    """
    return_value = 0
    for i in range(0, len(group) - 1):
        for j in range(i+1, len(group)):
            if social_network.has_edge(group[i], group[j]):
                return_value += social_network[group[i]][group[j]]['weight']
    return return_value
