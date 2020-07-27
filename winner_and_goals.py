import json
import requests

page = None
winner = None
BASE_URL = 'https://jsonmock.hackerrank.com/api/football_matches'
winner_url = 'https://jsonmock.hackerrank.com/api/football_competitions'
#https://jsonmock.hackerrank.com/api/football_matches?year={}&team1={}&competition={}}&page={}

def get_total_pages(winner,year,comp_name):
    res = requests.get(BASE_URL+f'?year={year}&team1={winner}&competition={comp_name}')
    j_data = res.content
    pydata = get_py_data(j_data)
    total_pages = pydata.get('total_pages')
    return total_pages


def get_json(winner,year,comp_name,team,page):
    if winner == None:
        response = requests.get(winner_url+'?year={}&name={}'.format(year,comp_name))
        data = response.content
        matchdata =get_py_data(data)
        return matchdata['data']

    else:
        res = None
        if team =='team1':
            res = requests.get(BASE_URL+f'?year={year}&team1={winner}&competition={comp_name}&page={page}')
        elif team == 'team2':
            res = requests.get(BASE_URL+f'?year={year}&team2={winner}&competition={comp_name}&page={page}')

        j_data = res.content
        matchdata = get_py_data(j_data)
        return matchdata['data']

def get_py_data(data):
    pydata = json.loads(data)
    matchdata = pydata
    return matchdata


def find_winner(year,comp_name,team):
    matchdata = get_json(winner,year,comp_name,team,page)
    winner_data = matchdata[0].get('winner')
    return winner_data


def count_goals(winner,year,comp_name,team,page):
    counter = 0
    for p in range(1,page+1):
        page = p
        page_goal = 0
        matchdata = get_json(winner,year,comp_name,team,page)
        for i in range(len(matchdata)):
            team_goal = 0
            if team =='team1':
                team_goal = matchdata[i].get('team1goals')
            elif team == 'team2':
                team_goal = matchdata[i].get('team2goals')

            team_goal_int = int(team_goal)
            counter = counter + team_goal_int
            page_goal += team_goal_int
        print('page =',p,'goals-->',page_goal)
    return counter

if __name__ == '__main__':
    # print("Enter Year and Competition name to find out winner")
    print("Select number from following to select competition:")
    print("""   {"1": 'Serie A',
                 '2': 'UEFA Champions League',
                 '3': 'La Liga',
                 '4': 'English Premier League',
                 '5': 'League 1',
                 '6': 'Bundesliga'}
    """)

    comp_name = None
    choice =input("Enter a number for competition:")
    if choice == '1':
        comp_name = 'Serie A'
    elif choice =='2':
        comp_name = 'UEFA Champions League'
    elif choice == '3':
        comp_name = 'La Liga'
    elif choice == '4':
        comp_name = 'English Premier League'
    elif choice == '5':
        comp_name = 'League 1'
    elif choice == '6':
        comp_name = 'Bundesliga'
    else:
        print("invalid number")

    year = int(input("Enter a year:"))
    winner = find_winner(year,comp_name,team=None)
    print(f"winner of the {comp_name} of {year} is--> ",winner)
    print("-----------------------------")
    pages = get_total_pages(winner,year,comp_name)
    print("total pages to be checked-->",pages)
    team1_total_goals = count_goals(winner,year,comp_name,team='team1',page=pages)
    print(f"total goal of {winner} as a team1-->",team1_total_goals)
    team2_total_goals = count_goals(winner, year, comp_name, team='team2',page=pages)
    print(f"total goal of {winner} as a team2-->",team2_total_goals)
    print(f"Total goals score by {winner} is ", team1_total_goals+team2_total_goals)
