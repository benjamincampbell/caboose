#!/usr/bin/env python

#Created by Josh Fuerst
# for question/bug reports please visit http://www.fuerstjh.com and submit through contact page. 

#only been tested on python 3.2
#Currently if an error is encountered the API does not handle the exception it raises it to the caller. 


#******************* USAGE *******************

#import espn_api
#espn_api_v3.get_scores(espn_api.NCAA_FB, 'Cincinnati, Ohio State')


#****************** ABOUT ****************************

#This API connects to ESPN bottomline and parses the page to get current game scores.
#Just call the get_scores function passing in a league string (defined below)

#The return value will be a dictionary of games. Each entry will have the following structure:
        # {espn_game_id:[team1_name,team1_score,team2_name,team2_score,game_time]}
        
#You can also pass in team_filter. This should be a comma separated string of the team names you wish to 
#get scores for
#NOTE: the team names must appear as listed on espn bottomline. To see list run once with no filter


from urllib import request

#LEAGE STRINGS
NCAA_FB = 'ncf'
NFL = 'nfl'
MLB = 'mlb'
NBA = 'nba'
NHL = 'nhl'
NCAA_BB = 'mens-college-basketball'

def get_scores(league,team_filter=None):

        scores = {}
        STRIP = "()1234567890 "
        if team_filter:
                team_filter=team_filter.lower().split(', ')

        try:
                #visit espn bottomline website to get scores as html page
                url = 'http://sports.espn.go.com/'+league+'/bottomline/scores'
		#url = "http://www.fuerstjh.com/test.html"
                req = request.Request(url)
                response = request.urlopen(req)
                page = response.read()

                #url decode the page and split into list
                data = request.unquote(str(page)).split('&'+league+'_s_left')

                #extract the important data
                for i in range(1,len(data)):

                        #get rid of junk at beginning of line, remove ^ which marks team with ball
                        main_str = data[i][data[i].find('=')+1:].replace('^','')

                        #extract time, you can use the ( and ) to find time in string
                        time =  main_str[main_str.rfind('('):main_str.rfind(')')+1].strip()

                        #extract score, it should be at start of line and go to the first (
                        score =  main_str[0:main_str.rfind('(')].strip()

                        #extract espn gameID use the keyword gameId to find it
                        gameID = main_str[main_str.rfind('gameId')+7:].strip()
						    
                        
                        if gameID == '':
                                #something wrong happened
                                continue
                          
                        #split score string into each teams string
                        team1_name = ''
                        team1_score = '0'
                        team2_name = ''
                        team2_score = '0'
                        

                        if (' at ' not in score):
                                teams = score.split('  ')
                                team1_name = teams[0][0:teams[0].rfind(' ')].lstrip(STRIP)
                                team2_name = teams[1][0:teams[1].rfind(' ')].lstrip(STRIP)
                                team1_score = teams[0][teams[0].rfind(' ')+1:].strip()
                                team2_score = teams[1][teams[1].rfind(' ')+1:].strip()
                        else:
                                teams = score.split(' at ')
                                team1_name = teams[0].lstrip(STRIP)
                                team2_name = teams[1].lstrip(STRIP)
                                
                        #add to return dictionary
                        if not team_filter:
                                scores[gameID] = ['','','','','']
                                scores[gameID][0] = team1_name
                                scores[gameID][1] = team1_score
                                scores[gameID][2] = team2_name
                                scores[gameID][3] = team2_score
                                scores[gameID][4] = time
                        elif team1_name.lower() in team_filter or team2_name.lower() in team_filter:
                                scores[gameID] = ['','','','','']
                                scores[gameID][0] = team1_name
                                scores[gameID][1] = team1_score
                                scores[gameID][2] = team2_name
                                scores[gameID][3] = team2_score
                                scores[gameID][4] = time
                                
        except Exception as e:
                print(str(e))
                raise e

        return scores
 
