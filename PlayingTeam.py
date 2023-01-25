from extraLib import *

class PlayingTeam:
    def __init__(self, game_url, location, live):
        data = get_json_response(game_url)

        self.game_url = game_url
        self.location = location
        self.name = data["gameData"]["teams"][self.location]["name"]
        self.score = 0
        self.side = ""
        if live:
            self.score = data["liveData"]["plays"]["currentPlay"]["about"]["goals"][self.location]
    
    def update_score(self):
        response = requests.get(self.game_url)
        data = response.json()

        updated_score = data["liveData"]["plays"]["currentPlay"]["about"]["goals"][self.location]

        if updated_score != self.score:
            self.score = updated_score
            return True
        else:
            return False

    def get_game_url(self):
        return self.game_url
    
    def get_location(self):
        return self.location

    def get_name(self):
        return self.name
    
    def get_score(self):
        return self.score
    
    def get_side(self):
        return self.side
    
    def set_game_url(self, game_url):
        self.game_url = game_url

    def set_location(self, location):
        self.location = location

    def set_name(self, name):
        self.name = name
    
    def set_score(self, score):
        self.score = score
    
    def set_side(self, side):
        self.side = side