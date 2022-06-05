import traceback
import pyodbc


class DB:
    @staticmethod
    def connect_to_db(server_name, db_name, username, password):
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}' +
                              ';SERVER=' + server_name +
                              ';DATABASE=' + db_name +
                              ';UID=' + username +
                              ';PWD=' + password +
                              ';Trusted_Connection=yes;')
        cur = conn.cursor()
        return conn, cur

    @staticmethod
    def get_db_user_pass():
        items = []
        with open("db_user_pass.txt", 'r') as file:
            for line in file:
                # remove linebreak which is the last character of the string
                current_item = line[:-1]
                # add item to the list
                items.append(current_item)
            username = items[0].split(":")
            username = username[1]
            password = items[1].split(":")
            password = password[1]
        return username, password

    @staticmethod
    def my_to_sql(df, cursor, table_name, list_of_tbl_col_names, list_of_tbl_col_types, needs_key=False):
        if len(list_of_tbl_col_names) == len(list_of_tbl_col_names):
            creation_tpl = "("
            index = 0
            for item in list_of_tbl_col_names:
                creation_tpl = creation_tpl + item + " " + list_of_tbl_col_types[index] + " ,"
                index = index + 1
            creation_tpl = creation_tpl[:-2]
            creation_tpl = creation_tpl + ")"
            try:
                # print("create table " + table_name + creation_tpl + ";")
                cursor.execute("create table " + table_name + creation_tpl + ";")
                cursor.commit()
                print("table created.")
            except:
                print("table exist.")
        else:
            print("my_to_sql method's input is incorrect")

        insertion_tpl = "("
        for item in list_of_tbl_col_names:
            insertion_tpl = insertion_tpl + item + ", "
        insertion_tpl = insertion_tpl[:-2]
        insertion_tpl = insertion_tpl + ")"
        if not needs_key:
            try:
                for row in df.itertuples(index=False, name=None):
                    # print("insert into " + table_name + " values " + str(row) + ";")
                    row = str(row).replace("None", "NULL")
                    cursor.execute("insert into " + table_name + " values " + row + ";")
                    cursor.commit()
                print("data inserted into " + table_name + " successfully.")
            except pyodbc.ProgrammingError:
                traceback.print_exc()
                print("Inserting data to database failed.")
        else:
            try:
                for row in df.itertuples(index=False, name=None):
                    # print("insert into " + table_name + insertion_tpl + " values " + str(row) + ";")
                    row = str(row).replace("None", "NULL")
                    cursor.execute("insert into " + table_name + insertion_tpl + " values " + row + ";")
                    cursor.commit()
                print("data inserted into " + table_name + " successfully.")
            except pyodbc.ProgrammingError:
                traceback.print_exc()
                print("Inserting data to database failed.")
