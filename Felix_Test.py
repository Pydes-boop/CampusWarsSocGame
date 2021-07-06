import metis
import networkx as nx
from random import choice


def get_graph():
    """
    creates a nx graph with overlapping lectures/user in lecture as edge weights and students/users as nodes
    :return:
    """
    lectures = lectures = {"Audiokommunikation: 21S": ["uid2"],
                "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S": ["uid3"],
                "Echtzeit-Computergrafik (IN0038): 21S": ["uid1"],
                "Vorlesung B": ["uid6"],
                "Vorlesung A": ["uid4"],
                "Vorlesung D": ["uid5", "uid4"],
                "Vorlesung E": ["uid7"],
                "Vorlesung F": ["uid8"],
                "Vorlesung G": ["uid10"],
                "Vorlesung H": ["uid11"],
                "Vorlesung I": ["uid12"],
                "Vorlesung J": ["uid13"],
                "Vorlesung K": ["uid14"],
                "Vorlesung L": ["uid15"],
                "Vorlesung M": ["uid16"],
                "Vorlesung C": ["uid6", "uid9"],}
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
    return social_network

def get_max_groups(social_network, min_group_size=4):
    if len(social_network.nodes) % min_group_size > 0:
        max_groups = int((len(social_network.nodes) / min_group_size) + 1)
    else:
        max_groups = int(len(social_network.nodes) / min_group_size)
    return max_groups

def metis_calulation():
    social_network = get_graph()
    social_network.graph['edge_weight_attr'] = 'weight'
    max_groups = get_max_groups(social_network, 5)
    (edgecuts, parts) = metis.part_graph(social_network, max_groups)
    teams = []
    for i in range(0, max_groups):
        teams.append([])
    j = 0
    for node in social_network.nodes():
        teams[parts[j]].append(node)
        j = j + 1
    print(teams)
    # user_groups = []
    # for team in teams:
    #     user_groups.append(Group(generate_team_name(), get_random_color(), team))
    # interface.add_new_teams(user_groups)

if __name__ == '__main__':
    metis_calulation()
    # print(get_all_teams())
