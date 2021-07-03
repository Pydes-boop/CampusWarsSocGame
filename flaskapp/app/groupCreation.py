import networkx as nx
import pulp
from apis.v1.utils.random_stuff import get_random_color, generate_team_name, used_names
from dataclasses import dataclass
from apis.v1.database import interface
from typing import Any
from random import choice


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
    loners = nx.isolates(social_network)
    for user in list(loners):
        social_network.add_edge(user, choice(list(social_network.nodes())), weight=0.0001, counter=1)
        social_network.add_edge(user, choice(list(social_network.nodes())), weight=0.0001, counter=1)
    for u, v, d in social_network.edges(data=True):
        d['weight'] = d['weight'] / d['counter']
    min_group_size = 4
    max_group_size = 6
    if len(social_network.nodes) % min_group_size > 0:
        max_groups = int((len(social_network.nodes) / min_group_size) + 1)
    else:
        max_groups = int(len(social_network.nodes) / min_group_size)

    # create list of all possible tables
    possible_groups = []
    for i in range(min_group_size, max_group_size + 1):
        possible_groups.extend([tuple(c) for c in pulp.combination(social_network.nodes, i)])

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
    # return user_groups
    return interface.add_new_teams(user_groups)


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


def alternative_calculation():
    biggest_change = -1
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
    loners = nx.isolates(social_network)
    for user in list(loners):
        social_network.add_edge(user, choice(list(social_network.nodes())), weight=0.0001, counter=1)
        social_network.add_edge(user, choice(list(social_network.nodes())), weight=0.0001, counter=1)
    for u, v, d in social_network.edges(data=True):
        d['weight'] = d['weight'] / d['counter']
    min_group_size = 4
    max_group_size = 6
    current_partition = [list(social_network.nodes)[x:x + min_group_size] for x in
                         range(0, social_network.number_of_nodes(), min_group_size)]
    if len(current_partition[len(current_partition) - 1]) != min_group_size:
        last_entries = current_partition[len(current_partition) - 1]
        current_partition.pop()
        for i in range(0, len(last_entries)):
            current_partition[i].append(last_entries[i])
    should_swap_again = True
    copied_list = []
    for i in current_partition:
        copied_list.append(i[:])
    # result = {"before": {"name": "before", "list": copied_list}, "swapList": [], "swaps": []}

    while should_swap_again:
        next_swap = find_next_swap(social_network, current_partition, min_group_size, max_group_size)
        # result["swaps"].append(next_swap["sum"])
        # result["swapList"].append(next_swap)
        if next_swap["sum"] == 0:
            break
        if biggest_change < next_swap["sum"]:
            biggest_change = next_swap["sum"]
        if next_swap["sum"] < biggest_change * 0.1:
            should_swap_again = False
        if not next_swap["player1"] is None:
            player = current_partition[next_swap["partition1"]].pop(next_swap["player1"])
            current_partition[next_swap["partition2"]].append(player)
        if not next_swap["player2"] is None:
            player = current_partition[next_swap["partition2"]].pop(next_swap["player2"])
            current_partition[next_swap["partition1"]].append(player)
    # result["after"] = current_partition
    teams = []
    for group in current_partition:
        teams.append(Group(generate_team_name(), get_random_color(), group))
    return interface.add_new_teams(teams)


def find_next_swap(graph, current_partition, min_size, max_size):
    best_result = get_best_result_as_dict(0, None, None, None, None)
    for i, p in enumerate(current_partition):
        for j, p2 in enumerate(current_partition):
            if i == j:
                continue
            old_sum = happiness(p, graph) + happiness(p2, graph)
            if len(p) > min_size and len(p2) < max_size:
                for k in range(0, len(p)):
                    pl1 = p[k]
                    new_p = p[:]
                    new_p.pop(k)
                    new_p2 = p2[:]
                    new_p2.append(pl1)
                    new_sum = happiness(new_p, graph) + happiness(new_p2, graph)
                    if new_sum - old_sum > best_result["sum"]:
                        best_result = get_best_result_as_dict(new_sum - old_sum, k, None, i, j)
            if i <= j:
                for k in range(0, len(p)):
                    for m in range(0, len(p2)):
                        pl1 = p[k]
                        pl2 = p2[m]
                        new_p = p[:]
                        new_p.pop(k)
                        new_p.append(pl2)
                        new_p2 = p2[:]
                        new_p2.pop(m)
                        new_p2.append(pl1)
                        new_sum = happiness(new_p, graph) + happiness(new_p2, graph)
                        if new_sum - old_sum > best_result["sum"]:
                            best_result = get_best_result_as_dict(new_sum - old_sum, k, m, i, j)

    return best_result


def get_best_result_as_dict(sum, pl1, pl2, part1, part2):
    return {"sum": sum,
            "player1": pl1,
            "player2": pl2,
            "partition1": part1,
            "partition2": part2}
