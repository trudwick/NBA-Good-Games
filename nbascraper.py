from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplay
from datetime import date
from datetime import timedelta


def goodGameFinder(gameDate):
    gamefinder = leaguegamefinder.LeagueGameFinder()
    # The first DataFrame of those returned is what we want.
    games = gamefinder.get_data_frames()[0]

    # games_2023 = games[] 
    games_on_date = games.loc[(games['GAME_DATE']==gameDate)  & (games['GAME_ID'].astype(str).str[0]=='0')]
    # print(games_on_date['GAME_DATE'])
    games_on_date = games_on_date.drop_duplicates(subset=['GAME_ID'])
    games_on_date = games_on_date.sort_values('GAME_ID')
    print("\n\nTotal games on this date:",len(games_on_date))
    if len(games_on_date)==0:
        print ("No games found on this date :(. Try again!")
        return
    game_id = games_on_date.sort_values('GAME_ID').iloc[0]['GAME_ID']

    # print(games_on_date.columns)
    good=[]
    bad=[]
    for game_id, team_name in zip(games_on_date['GAME_ID'], games_on_date['TEAM_NAME']):
        teams = games[games["GAME_ID"]==game_id]['TEAM_NAME'].tolist()
        matchup_str=teams[0]+" vs "+teams[1]
        if gameIsGood(game_id):
            good.append(matchup_str)
        else:
            bad.append(matchup_str)
    print("Good Games:")
    for matchup in good:
        print("\t",matchup)
    print("\n")



def gameIsGood(game_id):
    pbp = playbyplay.PlayByPlay(game_id).get_data_frames()[0]
    pbp_q4 = pbp.loc[ (pbp['PERIOD']==4) &(pbp['PCTIMESTRING'].astype(str).str[0]<'4')&(pbp['PCTIMESTRING'].astype(str).str[1]==':')]     # 
    
    for play in pbp_q4['SCOREMARGIN']:

        if play is not None:
            if play == "TIE" or abs(int(play))<5:
                return True
    return False

def main():
    # game_date = '2024-01-15'
    game_date = input("Input date in the format YYYY-MM-DD. (leave blank for yesterday):")
    if game_date=='':
        game_date=str(date.today()-timedelta(days = 1)) #use yesterday
    print('Games for date:',game_date)
    goodGameFinder(game_date)

if __name__ == "__main__":
    main()
