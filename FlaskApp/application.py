from flask import Flask, request, render_template
from mysql.connector import Error
import mysql.connector

application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        name = details['name']
        choice = details['choice']

        conn = None
        try:
            #INN Master DB.
            #
            # conn = mysql.connector.connect(host='mysql-master.service.inneractive.consul',
            #                                port='3306',
            #                                database='actors_db',
            #                                user='keshavp',
            #                                password='ca2vYGB4fuc4YPCF',
            #                                auth_plugin='mysql_native_password')

            #Local DB.
            conn = mysql.connector.connect(host='127.0.0.1',
                                           port='3306',
                                           database='actors_db',
                                           user='generic',
                                           password='SecurePass1!',
                                           auth_plugin='mysql_native_password')

            if conn.is_connected():
                print('Connected to MySQL database')
                mycursor = conn.cursor()

                # INSERT TO DB
                if len(name) != 0:
                    write_sql = "INSERT INTO actors_db.groups (name, groupType) VALUES (%s, %s)"
                    val = (name, choice)
                    mycursor.execute(write_sql, val)
                    conn.commit()

                    print("1 record inserted, ID:", mycursor.lastrowid)
                else:
                    print("Please enter the name.")

                # READ from DB

                myreadcursor = conn.cursor()
                read_sql = "SELECT id, name, groupType from actors_db.groups WHERE name = %s"
                query_value = (name,)
                myreadcursor.execute(read_sql, query_value)

                s = "<table align='center'><tr><th>Id</th><th>Name</th><th>GroupType</th>"
                for row in myreadcursor:
                    s = s + "<tr>"
                for x in row:
                    s = s + "<td>" + str(x) + "</td>"
                s = s + "</tr>"

                return "<html><head>" \
                         "<style>" \
                            "img {display:block; margin-left:auto; margin-right:auto;}" \
                            "h1 {text-align:center; color:darkmagenta; margin:30px;}" \
                            "table,th,td {border:2px solid teal}" \
                         "</style>" \
                       "</head><body>" \
                            "<h1>Use the 'Id', to connect account on AMS.</h1><br>" \
                            + s + "</table>"\
                            "<br><br><br><br> <img src='static/trix.jpg' width='10%'>" \
                       "</body></html>"

        except Error as e:
            print(e)

        finally:
            if conn is not None and conn.is_connected():
                conn.close()

    return render_template('index.html')


if __name__ == "__main__":
    application.run()
