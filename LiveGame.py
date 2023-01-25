from PlayingTeam import *

class LiveGame:
    def __init__(self, game_url, live):
        response = requests.get(game_url)
        data = response.json()

        self.game_url = game_url
        self.home = PlayingTeam(game_url, "home", live)
        self.away = PlayingTeam(game_url, "away", live)
        self.game_is_live = live
        
        self.current_play = None
        if self.game_is_live:
            self.current_play = data["liveData"]["plays"]["currentPlay"]
            self.print_rink_using_coordinates(self.current_play["coordinates"])
    
    def update(self):
        play_has_updated = self.update_play()

        if play_has_updated:
            self.print_rink_using_coordinates(self.current_play["coordinates"])
            
            if self.current_play["result"]["description"] == "Game End" or self.current_play["result"]["description"] == "Game Official":
                self.game_is_live = False
                self.end_game()
    
    def print_rink_using_coordinates(self, coordinates):
        if coordinates:
            x_loc = coordinates['x']
            y_loc = coordinates['y']
            x_mod = (x_loc + 100) // 2
            y_mod = (y_loc + 42.5) // 4
            index = (y_mod * 100) + x_mod
            self.print_rink(index, self.current_play["result"]["description"])
        else:
            self.print_rink(-1, self.current_play["result"]["description"])
        
    def print_rink(self, index, play_description):
        clear_screen()

        left_column = self.generate_left_column(play_description)
        right_column = self.generate_right_column(index)
        
        for i in range(max(len(left_column), len(right_column))):
            if i < len(left_column):
                print("{:<45}".format(left_column[i]), end='')
            else:
                print(" " * 45, end='')
            print(" | ", end='')
            if i < len(right_column):
                print(" " * 5 + right_column[i], end='')
            else:
                print()
        
    def generate_left_column(self, play):
        left_column = []
        data = get_json_response(self.game_url)

        left_column.append("               {} Period               ".format(data["liveData"]["linescore"]["currentPeriodOrdinal"]))
        left_column.append("           {} minutes left           ".format(data["liveData"]["linescore"]["currentPeriodTimeRemaining"] if data["liveData"]["linescore"]["currentPeriodTimeRemaining"] != "END" else "00:00"))
        left_column.append("----------------------------------------")

        if len("Current Play: ") + len(play) <= 40:
            left_column.append("Current Play: {}".format(play))
        else:
            left_column.extend(capped_length_lines("Current Play: {}".format(play)))
        away_scored = self.away.update_score()
        home_scored = self.home.update_score()
        if home_scored or away_scored:
            if home_scored:
                left_column.append("")
                left_column.extend(capped_length_lines("GOAL! The {} have scored a goal!".format(self.home.get_name() if home_scored else self.away.get_name())))
                left_column.append("Updated Scores:")
                left_column.extend(capped_length_lines("{}: {}".format(self.home.get_name(), self.home.get_score())))
                left_column.extend(capped_length_lines("{}: {}".format(self.away.get_name(), self.away.get_score())))
        left_column.append("----------------------------------------")
        return left_column

    def generate_right_column(self, index):
        right_column = []

        data = get_json_response(self.game_url)

        # Really should only update sides on period changes
        period = data["liveData"]["linescore"]["currentPeriod"]

        self.home.set_side(data["liveData"]["linescore"]["periods"][period - 1]["home"]["rinkSide"])
        self.away.set_side(data["liveData"]["linescore"]["periods"][period - 1]["away"]["rinkSide"])

        left_name = self.home.get_name() + " (" + self.home.get_location().capitalize() + ")" if self.home.get_side() == "left" else self.away.get_name() + " (" + self.away.get_location().capitalize() + ")"
        left_score = self.home.get_score() if self.home.get_side() == "left" else self.away.get_score()
        right_name = self.home.get_name() + " (" + self.home.get_location().capitalize() + ")" if self.home.get_side() == "right" else self.away.get_name()+ " (" + self.away.get_location().capitalize() + ")"
        right_score = self.home.get_score() if self.home.get_side() == "right" else self.away.get_score()
        middle_spacing = 87 - (len(left_name) + 2 + len(str(left_score)) + len(right_name) + 2 + len(str(right_score)))

        # Fix this offcentered text for right?
        right_column.append("{1:>{0}}: {2:<{3}}".format(len(left_name) + 7, left_name, left_score, middle_spacing) + "{}: {}\n".format(right_name, right_score))
        
        temp = ""
        for i, element in enumerate(HOCKEY_RINK_LIST):
            if (i == index):
                temp += "&"
            elif (element == 'R') or (element == 'O') or (element == 'x') or (element == '1'):
                temp += (RED + element + RESET)
            elif (element == 'r') or (element == 'o') or (element == 'l'):
                temp += (BLUE + element + RESET)
            elif (element == '-') or (element == '/') or (element == '\\') or (element == '|'):
                temp += (BLACK + element + RESET)
            else:
                temp += element
            
            if ((i + 1) % 100 == 0):
                temp += '\n'
                right_column.append(temp)
                temp = ""

        return right_column

    def update_play(self):
        response = requests.get(self.game_url)
        data = response.json()

        updated_play = data["liveData"]["plays"]["currentPlay"]

        if (updated_play != self.current_play):
            self.set_last_play(updated_play)
            return True
        else:
            return False
    
    def get_live_status(self):
        response = requests.get(self.game_url)
        data = response.json()
        return data["gameData"]["status"]["abstractGameState"]

    def end_game(self):
        print("\n\nFinal Scores:")
        print("\tAway ({}): {}".format(self.away.name, self.away.score))
        print("\tHome ({}): {}".format(self.home.name, self.home.score))

    def get_game_url(self):
        return self.game_url

    def get_last_play(self):
        return self.current_play
    
    def set_game_url(self, game_url):
        self.game_url = game_url
    
    def set_last_play(self, current_play):
        self.current_play = current_play