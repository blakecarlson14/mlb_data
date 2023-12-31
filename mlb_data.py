import datetime
import requests
import json


def getGamePks(fromDate: datetime.date, toDate: datetime.date):
    # get all game data for today
    gamePks = []

    gameData = requests.get(
        f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={fromDate}&endDate={toDate}"
    )

    gameDataJson = gameData.json()

    # get all gamePk for today
    for date in gameDataJson["dates"]:
        if "games" in date:
            for game in date["games"]:
                gamePks.append(game["gamePk"])

    return gamePks


def getGameData(gamePk: int):
    gameData = requests.get(
        f"https://statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live"
    )
    return gameData


def getBattingOrder(gameData: dict):
    battingOrders = {"home": {}, "away": {}}

    awayTeamCode = gameData["gameData"]["teams"]["away"]["teamCode"]
    battingOrders["away"][awayTeamCode] = []
    awayBattingOrder = gameData["liveData"]["boxscore"]["teams"]["away"]["battingOrder"]
    for player in awayBattingOrder:
        battingOrders["away"][awayTeamCode].append(
            gameData["gameData"]["players"][f"ID{player}"]["fullName"]
        )

    homeTeamCode = gameData["gameData"]["teams"]["home"]["teamCode"]
    battingOrders["home"][homeTeamCode] = []
    homeBattingOrder = gameData["liveData"]["boxscore"]["teams"]["home"]["battingOrder"]
    for player in homeBattingOrder:
        battingOrders["home"][homeTeamCode].append(
            gameData["gameData"]["players"][f"ID{player}"]["fullName"]
        )

    return battingOrders


def getTeamBattingOrder(gameData: dict, teamCode: str):
    res = [
        key
        for key, value in gameData["gameData"]["teams"].items()
        if "min" in value["teamCode"]
    ]
    if res:
        data = gameData["liveData"]["boxscore"]["teams"][res[0]]["battingOrder"]
        for player in data:
            print(gameData["gameData"]["players"][f"ID{player}"]["fullName"])


def wasGamePlayed(gameData: dict):
    if gameData["gameData"]["status"]["codedGameState"] == "F":
        return True
    else:
        return False


def printBoxScore(gameData: dict):
    pass


if __name__ == "__main__":
    # This is the first date found in the api
    firstDate = datetime.datetime(1901, 4, 18).date()

    date = datetime.datetime(1900, 1, 1).date()
    today = datetime.datetime.today().date()
    # print(date)
    # gamePks = getGamePks(fromDate=date, toDate=today)

    delta = datetime.timedelta(days=1)

    while date <= today:
        # don't count anything before april
        if date.month <= 3:
            date = datetime.datetime(date.year, 4, 1).date()
            continue

        print(date)
        gamePks = getGamePks(fromDate=date, toDate=date)

        # couldn't find any games in june, move on to the next year
        if date.month == 6 and len(gamePks) == 0:
            date = datetime.datetime(date.year + 1, 1, 1).date()
            continue

        # The season has ended, move on to the next year
        if date.month >= 9 and len(gamePks) == 0:
            date = datetime.datetime(date.year + 1, 1, 1).date()
            continue

        # if len(gamePks) > 0:
        #     break

        print(gamePks)
        date += delta

    # for gamePk in gamePks:
    #     gameData = getGameData(gamePk=gamePk).json()

    #     # check if game was played
    #     if wasGamePlayed(gameData=gameData):
    #         battingOrders = getBattingOrder(gameData=gameData)
    #         # battingOrders = getTeamBattingOrder(gameData=gameData, teamCode='min')
    #         if battingOrders:
    #             print(battingOrders)
    #             print("")
    #         # printBoxScore(gameData=gameData)
