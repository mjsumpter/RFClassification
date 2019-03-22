import sqlite3
import requests
from bs4 import BeautifulSoup
from sqlite3 import Error


def main():
    database = "./sigid.db"

    source = "https://www.sigidwiki.com/wiki/Database"

    sql_create_signals_table = """ CREATE TABLE IF NOT EXISTS signals (
                                        id integer PRIMARY KEY,
                                        active integer NOT NULL,
                                        sig_type text,
                                        sig_desc text,
                                        op_freq text,
                                        mode text,
                                        modulation text,
                                        bandwidth text,
                                        location text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        with conn:

            # create signals table
            create_table(conn, sql_create_signals_table)

            print("Scraping sigidwiki.com...")
            html_request = requests.get(source)

            wiki_soup = BeautifulSoup(html_request.content, 'html.parser')

            # extract table of sources from HTML
            source_table = wiki_soup.find_all(
                "table", {"class": "wikitable"})[1]

            count = 0  # tracks current row
            id_val = 1  # tracks number of sources

            for row in source_table:

                # skips header rows and rows that don't have full dataset(9 cells)
                if count < 2 and len(row) < 9:
                    count += 1
                    continue

                # source_row is a list of all html rows
                source_row = row.find_all('td')

                ''' 
                Wiki uses green background to signify active signal, red to signify inactive signal, 
                and no color to represent unknown
                '''
                if len(source_row) < 1:
                    continue
                # skip rows that haven't been determined to be active or not active
                if not source_row[0].has_attr('bgcolor'):
                    continue
                elif source_row[0]['bgcolor'] == "#DAFFDC":
                    active = 1
                else:
                    active = 0

                sig_type, sig_desc, op_freq, mode, modulation, bandwidth, location = None, None, None, None, None, None, None

                # for each cell in a row
                for x in range(len(source_row)):

                    # find tooltip spans within each cell
                    tooltips = source_row[x].find_all(
                        'span', {'class': 'mw-lingo-tooltip-definition'})

                    # cast BeautifulSoup object to string
                    cell = str(source_row[x].text.strip())

                    # if tool tips exist in cell, remove them
                    if tooltips != None:
                        for tooltip in tooltips:
                            tooltip = str(tooltip.text.strip())
                            cell = cell.replace(tooltip, "")

                    # assign cell to db value
                    if x == 0:
                        sig_type = cell
                    elif x == 1:
                        sig_desc = cell
                    elif x == 2:
                        op_freq = cell
                    elif x == 3:
                        mode = cell
                    elif x == 4:
                        modulation = cell
                    elif x == 5:
                        bandwidth = cell
                    elif x == 6:
                        location = cell

                source = (id_val, active, sig_type, sig_desc, op_freq,
                          mode, modulation, bandwidth, location)
                id_val += 1

                # add source to database
                create_source(conn, source)

            print("Complete")

    else:
        print("Error: cannot create database connection.")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_source(conn, source):
    """
    Create a new source into the signals table
    :param conn:
    :param source:
    :return: source id
    """

    sql = ''' INSERT or IGNORE into signals(id, active, sig_type, sig_desc, op_freq, mode, modulation, bandwidth, location)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, source)
    return cur.lastrowid


if __name__ == "__main__":
    main()
