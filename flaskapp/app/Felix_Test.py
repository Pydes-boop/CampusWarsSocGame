import groupCreation
# from apis.v1.database.interface import get_all_teams
import metis

def metis_calulation():
    social_network = groupCreation.get_graph()
    max_groups = groupCreation.get_max_groups(social_network, 5)
    teams = metis.part_graph(social_network, max_groups)[1]
    print(teams)
    # user_groups = []
    # for team in teams:
    #     user_groups.append(Group(generate_team_name(), get_random_color(), team))
    # interface.add_new_teams(user_groups)

if __name__ == '__main__':
    metis_calulation()
    # print(get_all_teams())
