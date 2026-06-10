import requests
import pandas as pd
import time

API_KEY = "8f55643a19b17fd293c0f7bd1729a577"

SPORTS = [
    "soccer_china_superleague",
    "soccer_japan_j_league",
    "soccer_brazil_campeonato"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_matches = []

for sport in SPORTS:

    print(f"正在获取: {sport}")

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds"

    params = {
        "apiKey": API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    success = False

    for retry in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:

                print(
                    "状态码:",
                    response.status_code
                )

                print(
                    response.text
                )

                time.sleep(2)

                continue

            data = response.json()

            for game in data:

                home_team = game.get(
                    "home_team"
                )

                away_team = game.get(
                    "away_team"
                )

                commence_time = game.get(
                    "commence_time"
                )

                bookmakers = game.get(
                    "bookmakers",
                    []
                )

                if not bookmakers:
                    continue

                markets = bookmakers[0].get(
                    "markets",
                    []
                )

                if not markets:
                    continue

                outcomes = markets[0].get(
                    "outcomes",
                    []
                )

                home_odds = None
                draw_odds = None
                away_odds = None

                for o in outcomes:

                    name = o.get("name")
                    price = o.get("price")

                    if name == home_team:

                        home_odds = price

                    elif name == away_team:

                        away_odds = price

                    elif str(name).lower() == "draw":

                        draw_odds = price

                all_matches.append({

                    "比赛时间": commence_time,

                    "主队": home_team,
                    "客队": away_team,

                    "主胜赔率": home_odds,
                    "平局赔率": draw_odds,
                    "客胜赔率": away_odds,

                    "初始主胜赔率": home_odds,
                    "初始平局赔率": draw_odds,
                    "初始客胜赔率": away_odds,

                    "赛事": sport

                })

            success = True

            break

        except Exception as e:

            print(
                f"第{retry+1}次失败:"
            )

            print(e)

            time.sleep(3)

    if not success:

        print(
            f"{sport} 获取失败"
        )

df = pd.DataFrame(all_matches)

if len(df) == 0:

    print("没有抓到赔率")

else:

    df["比赛时间"] = (
        pd.to_datetime(
            df["比赛时间"],
            utc=True
        )
        .dt.tz_convert(
            "Asia/Tokyo"
        )
        .dt.tz_localize(
            None
        )
    )

    df = df.sort_values(
        "比赛时间"
    )

    df.to_excel(
        "matches_with_odds.xlsx",
        index=False
    )

    print()
    print("成功生成 matches_with_odds.xlsx")
    print("比赛数:", len(df))

    print(
        df[
            [
                "比赛时间",
                "主队",
                "客队"
            ]
        ].head()
    )