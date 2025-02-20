import requests
from bs4 import BeautifulSoup
import re
import sqlite3

def main():
    #team_update()
    player_update()

# 各チーム名を取得、DBに上書き登録
def team_update():
    team = [
        {
            'team_name'  : '阪神タイガース',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : '広島東洋カープ',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : '横浜DeNAベイスターズ',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : '読売ジャイアンツ',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : '東京ヤクルトスワローズ',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : '中日ドラゴンズ',
            'league'    : 'セントラル',
        },
        {
            'team_name'  : 'オリックス・バファローズ',
            'league'    : 'パシフィック',
        },
        {
            'team_name'  : '千葉ロッテマリーンズ',
            'league'    : 'パシフィック',
        },
        {
            'team_name'  : '福岡ソフトバンクホークス',
            'league'    : 'パシフィック',
        },
        {
            'team_name'  : '東北楽天ゴールデンイーグルス',
            'league'    : 'パシフィック',
        },
        {
            'team_name'  : '埼玉西武ライオンズ',
            'league'    : 'パシフィック',
        },
        {
            'team_name'  : '北海道日本ハムファイターズ',
            'league'    : 'パシフィック',
        },
    ]

    # sql作成
    sql =   'INSERT INTO team(team_id, team_name, league)VALUES'
    first = True
    id = 1
    for line in team:
        if first:
            first = False
        else:
            sql += ', '

        sql += '('
        sql += '' + str(id) + ', '
        sql += '"' + line['team_name'] + '", '
        sql += '"' + line['league'] + '"'
        sql += ')'
        id += 1
    
    # DB接続、追加
    dbname = 'data/baseball_player_db.db'
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # 前準備：テーブルの中身リセット
    cur.execute('DELETE from team')
    cur.execute(sql)

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()
    return

# 各チームの選手情報を取得、DBに上書き登録
def player_update():
    team_list = [] # DBから取得したチーム一覧を格納
    # DB接続、追加
    dbname = 'data/baseball_player_db.db'
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


    # 各チーム選手情報ページURL　配列
    team_url_list = [
        'https://npb.jp/bis/players/active/rst_t.html', # タイガース
        'https://npb.jp/bis/players/active/rst_c.html', # カープ
        'https://npb.jp/bis/players/active/rst_db.html',# ベイスターズ
        'https://npb.jp/bis/players/active/rst_g.html', # ジャイアンツ
        'https://npb.jp/bis/players/active/rst_s.html', # スワローズ
        'https://npb.jp/bis/players/active/rst_d.html', # ドラゴンズ
        'https://npb.jp/bis/players/active/rst_b.html', # バファローズ
        'https://npb.jp/bis/players/active/rst_m.html', # マリーンズ
        'https://npb.jp/bis/players/active/rst_h.html', # ホークス
        'https://npb.jp/bis/players/active/rst_e.html', # イーグルス
        'https://npb.jp/bis/players/active/rst_l.html', # ライオンズ
        'https://npb.jp/bis/players/active/rst_f.html'  # ファイターズ
    ]
    # 選手情報連想配列
    players = []

    ########################################
    # url情報取得
    ########################################
    for url in team_url_list:
        #url = "https://npb.jp/bis/players/active/rst_h.html"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        data = soup.select(".player_unit_1 ")
        
        ########################################
        # 選手情報をループしてplayersに挿入
        ########################################
        for line in data:
            pos = ""
            number = -999
            name = ""
            team = ""

            # 背番号取得準備
            pos = line.select_one(".pos").get_text()
            pos = pos.split(" ")
            # posから背番号のみ抜き出す
            for line2 in pos:
                if is_int(line2):
                    number = int(line2)
                    break

            # 氏名取得
            name = line.select_one(".name").get_text()
            name = name.replace(' ', '')    # 半角スペース除去
            name = name.replace('　', '')   # 全角スペース除去
            name = name.replace('\r\n', '') # 改行コード除去

            # チーム名取得
            team = line.select_one(".team").get_text()
            team = team.replace(' ', '')    # 半角スペース除去
            team = team.replace('　', '')   # 全角スペース除去
            team = team.replace('\r\n', '') # 改行コード除去
            
            # チーム名をチームIDに変換
            team_id = -999
            for line2 in team_list:
                if line2['team_name'] == team:
                    team_id = line2['team_id']
                    break
            
            if team_id < 0:
                print('チーム判定失敗')
                continue

            # 連想配列に挿入
            players.append({
                'number': number,
                'name'  : name,
                'team'  : team,
                'team_id'  : team_id,
            })


        #print(players)
        #print(remove_bracket(tmp_pos[0]))
        #number = tmp_pos.split(",")
        #print(tmp_pos)
    

    ########################################
    # 選手情報をループしてplayersに挿入
    ########################################
    
    # SQL文作成
    sql =   'INSERT INTO player(number, name, team_id)VALUES'
    
    first = True
    for line in players:
        if first:
            first = False
        else:
            sql += ', '

        sql += '('
        sql += str(line['number']) + ', '
        sql += '"' + line['name'] + '", '
        sql += '' + str(line['team_id']) + ''
        sql += ')'
    
    # DB接続、追加
    dbname = 'data/baseball_player_db.db'
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # 前準備：テーブルの中身リセット
    cur.execute('DELETE from player')
    cur.execute(sql)

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()
    return

# 参考：https://atmarkit.itmedia.co.jp/ait/articles/2102/09/news026.html
# 文字列が数値を表し、int／float関数による変換が可能かどうかを判定
def is_int(s):  # 整数値を表しているかどうかを判定
    try:
        int(s, 10)  # 文字列を実際にint関数で変換してみる
    except ValueError:
        return False
    else:
        return True

# 参考：https://qiita.com/nekobake/items/aebd40e07037fc7911bc
# 独自ファクトリを使用する
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == "__main__":
    main()