import networkx as nx
import pulp
from apis.v1.utils.random_stuff import get_random_color, generate_team_name, used_names
from dataclasses import dataclass
from apis.v1.database import interface
from typing import Any


@dataclass
class Group:
    name: str
    color: str
    members: Any


def create_groups():
    """
    uses the wedding seating problem and solution to match users to groups
    (see https://coin-or.github.io/pulp/CaseStudies/a_set_partitioning_problem.html)
    gets the lectures and users from the db,
    and saves the new groups with a random name and color to the db
    :return:
    """
    used_names.clear()
    lectures = {}
    lecture_list = interface.get_all_lecture_ids()
    for lecture in lecture_list:
        lectures[lecture] = interface.get_users_of_lecture(lecture)
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
        d['weight'] = d['weight'] / d['counter']

    max_groups = len(social_network.nodes) / 5
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
    seating_model += sum([x[group] for group in possible_groups]) <= max_groups, "Maximum_number_of_tables"
    for user in social_network.nodes:
        seating_model += sum([x[group] for group in possible_groups
                              if user in group]) == 1, "Must_seat_%s" % user
    seating_model.solve()
    user_groups = []
    for group in possible_groups:
        if x[group].value() == 1.0:
            user_groups.append(Group(generate_team_name(), get_random_color(), group))
    interface.add_new_teams(user_groups)
    pass


def happiness(group, social_network):
    """
    find the happiness a group of people have inbetween themself
    :param social_network: nx graph with edges, nodes and weight on edges
    :param group: list of node names to check
    :return: sum of all weights between the group
    """
    return_value = 0
    for i in range(0, len(group) - 1):
        for j in range(i + 1, len(group)):
            if social_network.has_edge(group[i], group[j]):
                return_value += social_network[group[i]][group[j]]['weight']
    return return_value
