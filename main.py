# This is the intellectual property of Benjamin Dellaripa, use of said program without explicit permission from Benjamin Dellaripa can result in consequences
from __future__ import print_function
from discord.ext import commands
from riotwatcher import LolWatcher
from requests_html import HTMLSession
from Google import Create_Service

API_Name = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
TOKEN = 'OTM3NzgwMzg2NzA3MTY1MjU0.YfguCw.gJCO7zXKVAa870o42hLNkzt8KxU'
bot = commands.Bot(command_prefix='!')
api_key = 'RGAPI-18f4d876-72bc-4c74-80a9-d50842c4b504'
watcher = LolWatcher(api_key)
region = 'na1'
s = HTMLSession()

@bot.command(name='log')
async def log(ctx, *args):
    if ctx.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot':
        await ctx.send('What is the Summoner name you would like to log')


@bot.command(name='account')
async def opgg(ctx, *args):
    wins = 0
    losses = 0
    rank = ''
    tier = ''
    summLevel = ''
    soloQ = False
    if ctx.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot':
        Account = ''.join(args)
        opggLink = f'https://na.op.gg/summoner/userName={Account}'
        leagueOfGraphsLink = f'https://www.leagueofgraphs.com/summoner/na/{Account}'
        uggLink = f'https://u.gg/lol/profile/na1/{Account}/overview'

        await ctx.send(opggLink)
        await ctx.send(leagueOfGraphsLink)
        await ctx.send(uggLink)
        me = watcher.summoner.by_name(region, Account)
        for i in me:
            if i == 'id':
                id = me[i]
            if i == 'summonerLevel':
                summLevel = me[i]
        await ctx.send(Account + ' is level ' + str(summLevel))
        if summLevel < 75:
            await ctx.send('**DENIED** Player summoner level is lower than minimum (75)')
        rankedStatsLst = watcher.league.by_summoner(region, id)
        if len(rankedStatsLst) == 0:
            await ctx.send("Player is unranked")
            return
        else:
            x = 0
            y = len(rankedStatsLst)
            while x != y:
                rankedStats = rankedStatsLst[x]
                for i in rankedStats:
                    if rankedStats['queueType'] == 'RANKED_SOLO_5x5':
                        soloQ = True
                        tier = rankedStats['tier']
                        rank = rankedStats['rank']
                        wins = rankedStats['wins']
                        losses = rankedStats['losses']
                        x += 1
                        break
                    else:
                        x += 1
                        break
        if soloQ:
            gamesPlayed = wins + losses
            winRate = wins / gamesPlayed * 100
            await ctx.send(Account + ' has a rank of ' + tier + ' ' + rank + ' and has played ' + str(
                gamesPlayed) + ' games this season with a win rate of ' + str(round(winRate, 2)) + '%')
            if gamesPlayed < 50:
                await ctx.send('**DENIED** Player has less than required games played (125)')
            if winRate >= 58:
                await ctx.send('**ATTENTION** Player has above a 58% win rate, please investigate further!')
        else:
            await ctx.send("Player is unranked")
        return
    else:
        return


def player_stats(player, ID):
    summName = player['summonerName']
    win = player['win']
    if win:
        winNum = 1
    else:
        winNum = 0
    kills = player['kills']
    deaths = player['deaths']
    assists = player['assists']
    neutral = player['totalMinionsKilled']
    jungle = player['neutralMinionsKilled']
    cs = neutral + jungle
    timePlayed = (player['timePlayed'] / 60)
    damage = player['totalDamageDealtToChampions']
    visionScore = player['visionScore']
    champName = player['championName']
    if champName == 'MonkeyKing':
        champName = 'Wukong'
    playerStats = [[summName], [ID], [timePlayed], [winNum], [champName], [kills], [deaths], [assists], [damage],
                   [visionScore], [cs]]
    return (playerStats)


def bans(team, league, service):
    isEmpty = is_Ban_Empty(league,  service)
    isEmptyLST = isEmpty[0]
    isEmptyNum = isEmptyLST[0]
    cell_range_insert = f'W{isEmptyNum}'
    teamBans = team['bans']
    if len(teamBans) == 5:
        teamBans1 = teamBans[0]
        teamBans2 = teamBans[1]
        teamBans3 = teamBans[2]
        teamBans4 = teamBans[3]
        teamBans5 = teamBans[4]
        ban1 = teamBans1['championId']
        ban2 = teamBans2['championId']
        ban3 = teamBans3['championId']
        ban4 = teamBans4['championId']
        ban5 = teamBans5['championId']
        bans = [[ban1], [ban2], [ban3], [ban4], [ban5]]
    elif len(teamBans) == 4:
        teamBans1 = teamBans[0]
        teamBans2 = teamBans[1]
        teamBans3 = teamBans[2]
        teamBans4 = teamBans[3]
        ban1 = teamBans1['championId']
        ban2 = teamBans2['championId']
        ban3 = teamBans3['championId']
        ban4 = teamBans4['championId']
        bans = [[ban1], [ban2], [ban3], [ban4], ['']]
    elif len(teamBans) == 3:
        teamBans1 = teamBans[0]
        teamBans2 = teamBans[1]
        teamBans3 = teamBans[2]
        ban1 = teamBans1['championId']
        ban2 = teamBans2['championId']
        ban3 = teamBans3['championId']
        bans = [[ban1], [ban2], [ban3], [''], ['']]
    elif len(teamBans) == 2:
        teamBans1 = teamBans[0]
        teamBans2 = teamBans[1]
        ban1 = teamBans1['championId']
        ban2 = teamBans2['championId']
        bans = [[ban1], [ban2], [''], [''], ['']]
    elif len(teamBans) == 1:
        teamBans1 = teamBans[0]
        ban1 = teamBans1['championId']
        bans = [[ban1], [''], [''], [''], ['']]
    else:
        bans = [[''], [''], [''], [''], ['']]
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'

    output = bans
    value_range_body = {
        'majorDimension': 'ROWS',
        'values': output
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetID,
        valueInputOption='USER_ENTERED',
        range='Games!' + cell_range_insert,
        body=value_range_body
    ).execute()

    updateBanCell(isEmpty, league, service)


def is_Ban_Empty(league, service):
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'

    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetID,
        majorDimension='ROWS',
        range='BanNum!A1'
    ).execute()

    range = response['values']
    return range


def updateBanCell(isEmpty, league, service):
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'
    isEmptyLST = isEmpty[0]
    isEmptyNum = isEmptyLST[0]
    isEmptyInt = int(isEmptyNum)
    newCell = isEmptyInt + 5
    newValueBody = [[newCell]]

    value_range_body = {
        'majorDimension': 'ROWS',
        'values': newValueBody
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetID,
        valueInputOption='USER_ENTERED',
        range='BanNum!A1',
        body=value_range_body
    ).execute()


def team_stats(team):
    teamObjectives = team['objectives']
    baronInfo = teamObjectives['baron']
    barons = baronInfo['kills']
    dragonInfo = teamObjectives['dragon']
    dragons = dragonInfo['kills']
    heraldInfo = teamObjectives['riftHerald']
    heralds = heraldInfo['kills']
    towerInfo = teamObjectives['tower']
    towers = towerInfo['kills']

    teamStats = [[towers], [barons], [dragons], [heralds]]
    return teamStats


async def stats(league, ID, service):
    league = league
    rawID = ID
    gameID = 'NA1_' + str(rawID)
    gameData = watcher.match.by_id('Americas', gameID)
    gameInfo = gameData['info']
    teamInfo = gameInfo['teams']
    participants = gameInfo['participants']
    team1 = teamInfo[0]
    team2 = teamInfo[1]

    team1Stats = team_stats(team1)
    team2Stats = team_stats(team2)
    player1 = participants[0]
    player1Stats = player_stats(player1, rawID)
    player_assembler(player1Stats, league, service)
    team_assembler(team1Stats, league, service)

    player2 = participants[1]
    player2Stats = player_stats(player2, rawID)
    player_assembler(player2Stats, league, service)
    team_assembler(team1Stats, league, service)

    player3 = participants[2]
    player3Stats = player_stats(player3, rawID)
    player_assembler(player3Stats, league, service)
    team_assembler(team1Stats, league, service)

    player4 = participants[3]
    player4Stats = player_stats(player4, rawID)
    player_assembler(player4Stats, league, service)
    team_assembler(team1Stats, league, service)

    player5 = participants[4]
    player5Stats = player_stats(player5, rawID)
    player_assembler(player5Stats, league, service)
    team_assembler(team1Stats, league, service)

    player6 = participants[5]
    player6Stats = player_stats(player6, rawID)
    player_assembler(player6Stats, league, service)
    team_assembler(team2Stats, league, service)

    player7 = participants[6]
    player7Stats = player_stats(player7, rawID)
    player_assembler(player7Stats, league, service)
    team_assembler(team2Stats, league, service)

    player8 = participants[7]
    player8Stats = player_stats(player8, rawID)
    player_assembler(player8Stats, league, service)
    team_assembler(team2Stats, league, service)

    player9 = participants[8]
    player9Stats = player_stats(player9, rawID)
    player_assembler(player9Stats, league, service)
    team_assembler(team2Stats, league, service)

    player10 = participants[9]
    player10Stats = player_stats(player10, rawID)
    player_assembler(player10Stats, league, service)
    team_assembler(team2Stats, league, service)

    bans(team1, league, service)
    bans(team2, league, service)


def team_assembler(team, league, service):
    worksheet_name = 'Games!'
    isEmpty = is_Empty(league, service)
    isEmptyLST = isEmpty[0]
    isEmptyNum = isEmptyLST[0]
    cell_range_insert = f'S{isEmptyNum}'
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'

    output = team

    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': output
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetID,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()

    updateCell(isEmpty, league, service)


def is_Empty(league, service):
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'

    response = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetID,
        majorDimension='ROWS',
        range='Num!A1'
    ).execute()

    range = response['values']
    return range


def player_assembler(player, league, service):
    worksheet_name = 'Games!'
    isEmpty = is_Empty(league, service)
    isEmptyLST = isEmpty[0]
    isEmptyNum = isEmptyLST[0]
    cell_range_insert = f'B{isEmptyNum}'

    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'

    output = player

    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': output
    }
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetID,
        valueInputOption='USER_ENTERED',
        range=worksheet_name + cell_range_insert,
        body=value_range_body
    ).execute()


def updateCell(isEmpty, league, service):
    if league == 'vts':
        spreadsheetID = '1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk'
    elif league == 'vrs':
        spreadsheetID = '19TMW4RWPuGpBztskMWpRYrS7QisVTLUqGvmZLBTpsK8'
    elif league == 'vas':
        spreadsheetID = '1UxYqCOvpWN_JVOIgb7It3JNG1wpGbJb477gHxoxaKm0'
    elif league == 'vad':
        spreadsheetID = '1JFTR-ksEk6NJAkzesF35r2C6jHiYn34JbWZHB0uRy9U'
    elif league == 'vrd':
        spreadsheetID = '1tnXb1U40pru1IlyDCY6t3LeG1B0o3vG8k3yUEg6394c'
    elif league == 'academy':
        spreadsheetID = '1H1q6kcerFK5LdNaalanxasiPnVoXsA0sxl_nlR9p8OU'
    elif league == 'premier':
        spreadsheetID = '10smBbQk7Orw1Xm7ROHraI7IEG8ZWPLuqG1O6FyIq0Io'
    isEmptyLST = isEmpty[0]
    isEmptyNum = isEmptyLST[0]
    isEmptyInt = int(isEmptyNum)
    newCell = isEmptyInt + 1
    newValueBody = [[newCell]]

    value_range_body = {
        'majorDimension': 'COLUMNS',
        'values': newValueBody
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetID,
        valueInputOption='USER_ENTERED',
        range='Num!A1',
        body=value_range_body
    ).execute()


@bot.command(name='vts')
async def vas(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vts.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'vts'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='vrs')
async def vas(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vrs.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'vrs'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='vas')
async def vas(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vas.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'vas'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='vad')
async def vas(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vad.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'vad'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='vrd')
async def vas(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vrd.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'vrd'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='pd')
async def premier(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vts.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'premier'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)


@bot.command(name='ad')
async def academy(ctx, *args):
    CLIENT_SECRET_FILE = 'client_secret_vts.json'
    if ctx.message.author == bot.user:
        return
    elif ctx.channel.name == 'ravenbot-stats':
        league = 'academy'
        id = ''.join(args)
        service = Create_Service(CLIENT_SECRET_FILE, API_Name, API_VERSION, SCOPES)
        await stats(league, id, service)

bot.run(TOKEN)
