import numpy as np
import networkx as nx


def create_groups():
    # todo: @marina I need the saved lectures with its attendants
    lectures = {"Audiokommunikation: 21S": ["uid1", "uid2", "uid3"],
                "Didaktisches und pädagogisches Training für Tutoren (IN9028): 21S": ["uid3", "uid5"],
                "Echtzeit-Computergrafik (IN0038): 21S": ["uid1", "uid2", "uid4", "uid5"]}
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
    # todo: @Felix please select a matching algorithm and implement it
    user_groups = [["uid1", "uid3", "uid5"], ["udi2", "uid4"]]
    # todo: @Marina: please fill the database with the user_groups{list{str}}
    pass
