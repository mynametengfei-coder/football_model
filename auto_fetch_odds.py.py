import pandas as pd
from datetime import datetime
import os

print("开始抓取赔率...")

os.system("python fetch_odds.py")

history_file = "odds_history.xlsx"

try:

    df = pd.read_excel(
        "matches_with_odds.xlsx"
    )

    df["抓取时间"] = datetime.now()

    if os.path.exists(history_file):

        old = pd.read_excel(
            history_file
        )

        df = pd.concat(
            [old, df],
            ignore_index=True
        )

    df.to_excel(
        history_file,
        index=False
    )

    print("历史赔率更新成功")
    print("记录数:", len(df))

except Exception as e:

    print("更新失败")
    print(e)