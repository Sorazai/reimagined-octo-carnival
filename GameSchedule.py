import time
import datetime
import dateutil.parser
from LiveGame import *

class GameSchedule:
    def __init__(self, main_team):
        self.main_team = main_team
        self.game_url = ""
        self.live_game = None

    def search_for_games(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule")
        schedule = response.json()

        for date in schedule["dates"]:
            game_times = date["games"]
            for game in game_times:
                if ((game["teams"]["away"]["team"]["name"] == self.main_team) or (game["teams"]["home"]["team"]["name"] == self.main_team)) and (game["status"]["detailedState"] != "Final"):
                    if (game["status"]["abstractGameState"] == "Live"):
                        self.start_game(game, live=True)
                    elif (game["status"]["abstractGameState"] == "Preview"):
                        self.queue_game(game)
    
    def queue_game(self, game):
        game_time = int(dateutil.parser.parse(game["gameDate"]).timestamp() * 1000)
        current_time =  int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
        time_difference = game_time - current_time
        if (time_difference > 0):
            print_formatted_countdown(time_difference)
            if (time_difference > (5 * 1000 * 60)):
                time.sleep((time_difference - (5 * 1000 *  60)) // 1000)
        self.start_game(game, live=False)
    
    def start_game(self, game, live):
        self.game_url =  "http://statsapi.web.nhl.com{}".format(game["link"])
        self.live_game = LiveGame(self.game_url, live)
        while not self.live_game.game_is_live:
            current_status = self.live_game.get_live_status()
            if (current_status == "Preview"):
                        self.live_game.game_is_live = True
            time.sleep(1)
        self.maintain_live_game()

    def maintain_live_game(self):
        while self.live_game.game_is_live:
            self.live_game.update()
            time.sleep(1)

    def get_main_team(self):
        return self.main_team
    
    def set_main_team(self, main_team):
        self.main_team = main_team