import requests
from datetime import datetime
from .utils import CONSTANTS, get_user_info
from datetime import datetime
from .utils import CONSTANTS, get_user_info


def retrieve_stats(data, username, tag):
    meta = data.get("meta")
    stats = data.get("stats")

    map = meta.get("map").get("name")
    mode = meta.get("mode")
    time = datetime.strptime(meta.get("started_at"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    team = data.get("stats").get("team").lower()
    enemy_team = "red" if team == "blue" else "blue"
    rounds = data.get("teams")
    team_rounds = rounds.get(team)
    enemy_rounds = rounds.get(enemy_team)
    total_rounds = team_rounds + enemy_rounds
    result = (
        "W"
        if team_rounds > enemy_rounds
        else "L"
        if team_rounds < enemy_rounds
        else "D"
    )

    agent = stats.get("character").get("name")
    score = stats.get("score")
    kills = stats.get("kills")
    deaths = stats.get("deaths")
    assists = stats.get("assists")
    shots = stats.get("shots")
    damage = stats.get("damage")

    kda = f"{kills}/{deaths}/{assists}"
    acs = str(round(score / total_rounds))
    adr = str(round(damage.get("made") / total_rounds))
    dmg_delta = str(round((damage.get("made") - damage.get("received")) / total_rounds))
    kd = str(round(kills / deaths, 2))
    hsr = "{:.0%}".format(
        round(
            shots.get("head")
            / (shots.get("head") + shots.get("body") + shots.get("leg")),
            2,
        )
    )

    stats_message = f"""
    Match summary for {username}#{tag}:
    **{mode}** - __{time}__
    {agent} ({map})
    ({result}) {team_rounds}-{enemy_rounds}
    ```
    |    K/D/A    |   K/D   |   DDΔ   |   HSR   |   ADR   |   ACS   |
    |{kda.center(13)}|{kd.center(9)}|{dmg_delta.center(9)}|{hsr.center(9)}|{adr.center(9)}|{acs.center(9)}|
    ```
    """

    return stats_message

def retrieve_stats(data, username, tag):
    meta = data.get("meta")
    stats = data.get("stats")

    map = meta.get("map").get("name")
    mode = meta.get("mode")
    time = datetime.strptime(meta.get("started_at"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
        "%d/%m/%Y %H:%M:%S"
    )

    team = data.get("stats").get("team").lower()
    enemy_team = "red" if team == "blue" else "blue"
    rounds = data.get("teams")
    team_rounds = rounds.get(team)
    enemy_rounds = rounds.get(enemy_team)
    total_rounds = team_rounds + enemy_rounds
    result = (
        "W"
        if team_rounds > enemy_rounds
        else "L"
        if team_rounds < enemy_rounds
        else "D"
    )

    agent = stats.get("character").get("name")
    score = stats.get("score")
    kills = stats.get("kills")
    deaths = stats.get("deaths")
    assists = stats.get("assists")
    shots = stats.get("shots")
    damage = stats.get("damage")

    kda = f"{kills}/{deaths}/{assists}"
    acs = str(round(score / total_rounds))
    adr = str(round(damage.get("made") / total_rounds))
    dmg_delta = str(round((damage.get("made") - damage.get("received")) / total_rounds))
    kd = str(round(kills / deaths, 2))
    hsr = "{:.0%}".format(
        round(
            shots.get("head")
            / (shots.get("head") + shots.get("body") + shots.get("leg")),
            2,
        )
    )

    stats_message = f"""
    Match summary for {username}#{tag}:
    **{mode}** - __{time}__
    {agent} ({map})
    ({result}) {team_rounds}-{enemy_rounds}
    ```
    |    K/D/A    |   K/D   |   DDΔ   |   HSR   |   ADR   |   ACS   |
    |{kda.center(13)}|{kd.center(9)}|{dmg_delta.center(9)}|{hsr.center(9)}|{adr.center(9)}|{acs.center(9)}|
    ```
    """

    return stats_message


def get_recent_summary(data, member):
    options = data.get("options")[0].get("options")

    username, tag = get_user_info(options, member)
    options = data.get("options")[0].get("options")

    username, tag = get_user_info(options, member)

    extras = "?size=1"
    for option in options:
        if option.get("name") == "map":
            extras += "&map=" + option.get("value")
        if option.get("name") == "mode":
            extras += "&mode=" + option.get("value")

    response = requests.get(
        f"{CONSTANTS['API_URL']}/valorant/v1/lifetime/matches/na/{username}/{tag}{extras}"
    )
    response = requests.get(
        f"{CONSTANTS['API_URL']}/valorant/v1/lifetime/matches/na/{username}/{tag}{extras}"
    )

    if response.status_code == 200:
        data = response.json()
        message_content = retrieve_stats(data.get("data")[0], username, tag)
    else:
        message_content = f"Error from Valorant API: {response.status_code}"


    return message_content

