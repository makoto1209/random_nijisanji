import requests
from bs4 import BeautifulSoup
import re
import sqlite3

def main():
    get_liver()
    print("完了")

def get_liver():
    # DB接続、追加
    dbname = 'data/liver.db'
    conn = sqlite3.connect(dbname)
    conn.row_factory = dict_factory
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # 前準備：テーブルの中身リセット
    cur.execute('SELECT * FROM team;')
    team_list = cur.fetchall()

    # データベースへコミット。これで変更が反映される。
    #conn.commit()
    conn.close()

if __name__ == "__main__":
    main()