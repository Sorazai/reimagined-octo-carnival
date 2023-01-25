from GameSchedule import *

schedule = GameSchedule("Chicago Blackhawks")

while (True):
    schedule.search_for_games()
    time.sleep(3600)