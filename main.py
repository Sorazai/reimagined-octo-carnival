from GameSchedule import *

schedule = GameSchedule("New York Islanders")

while (True):
    schedule.search_for_games()
    time.sleep(3600)