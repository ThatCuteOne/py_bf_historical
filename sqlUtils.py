import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    if conn.cursor().execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cloud_stats';").fetchone() is None:
        conn.cursor().execute("CREATE TABLE cloud_stats (id integer PRIMARY KEY, date text, players_online integer, players_in_dom integer, players_in_tdm integer, players_in_inf integer, players_in_gg integer, players_in_ttt integer, players_in_boot integer)")
    return conn

    return conn

def add_stats(stats):
    conn = create_connection("stats.db")
    """
    Create a new stats entry into the stats table
    :param conn:
    :param stats:
    :return: stats id
    """
    sql = ''' INSERT INTO cloud_stats(date, players_online, players_in_dom, players_in_tdm, players_in_inf, players_in_gg, players_in_ttt, players_in_boot)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, stats)
    conn.commit()
    return cur.lastrowid

def get_latest_stats():
    conn = create_connection("stats.db")
    """
    Query the latest row in the stats table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cloud_stats ORDER BY id DESC LIMIT 1")

    row = cur.fetchone()

    return row

def graph_data():   
    conn = create_connection("stats.db")
    """
    Query date and players_online columns from cloud_stats table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT date, players_online, players_in_dom, players_in_tdm, players_in_inf, players_in_gg, players_in_ttt, players_in_boot FROM cloud_stats")

    rows = cur.fetchall()
    formatted_entries = []
    for date_str, players_online, players_in_dom, players_in_tdm, players_in_inf, players_in_gg, players_in_ttt, players_in_boot in rows:
        formatted_entries.append(f'  {{Date: new Date("{date_str}"), Players: {players_online}, Dom: {players_in_dom}, TDM: {players_in_tdm}, Inf: {players_in_inf}, GG: {players_in_gg}, TTT: {players_in_ttt}, Boot: {players_in_boot}}}')

    output = "[\n" + ",\n".join(formatted_entries) + "\n]" 
    return output