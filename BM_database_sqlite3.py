import sqlite3


class BM_database:
    """
    A brownian motion database constructor

    """
    def __init__(self, database_name="example_database.db"):
        """
        Init class
        :param database_name: name of the database file
        """
        try:
            self.connexion = sqlite3.connect(database_name, timeout=60)
            print("SQLite version ::: {}".format(sqlite3.version))
        except IOError as error:
            print(error)
        finally:
            if self.connexion:
                self.connexion.close()
        self.database_name_ = database_name

    def connect(self):
        """
        SQLite3 connexion to database
        """
        self.connexion = sqlite3.connect(self.database_name_)

    def disconnect(self):
        """
        Close connexion to database
        """
        self.connexion.close()

    def create_table_data(self):
        """
        Creates a table called data, which contains:
            traj_id: trajectory identification number
            time:    timestamp for the jump
            value:   position of the brownian motion at time time
        """
        self.connexion = sqlite3.connect(self.database_name_, timeout=10)
        c = self.connexion.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS data(
                    traj_id integer, 
                    time float, 
                    value float
                   )""")
        self.connexion.commit()
        self.connexion.close()

    def reinitialize_table_data(self):
        """
        Reinitialize the table data by deleting whatever was previously in there
        """
        self.connexion = sqlite3.connect(self.database_name_, timeout=10)
        c = self.connexion.cursor()
        c.execute("Delete from data")
        self.connexion.commit()
        self.connexion.close()

    def add_trajectory_to_table_data(self, id, times, values, m):
        """
        Inserts a trajectory to the table data.

        :param id:      Trajectory identification number
        :param times:   Timestamps vector for the jumps
        :param values:  Position of the brownian motion,
                        values[i] is where the motion is at time times[i]
        :param m:       Total number of jumps
        """
        self.connexion = sqlite3.connect(self.database_name_, timeout=10)
        for i in range(m + 1):
            self.connexion.execute("INSERT INTO data VALUES (:traj_id, :time, :value)",
                                   {'traj_id': id,
                                    'time': times[i],
                                    'value': values[i]}
                                   )
        self.connexion.commit()
        self.connexion.close()

    def fetch_all_data(self):
        """
        Gets all data from the data base.
        :return: a list of all data
        """
        self.connexion = sqlite3.connect(self.database_name_, timeout=10)
        cursor = self.connexion.cursor()
        cursor.execute("SELECT * FROM data")
        all_res = cursor.fetchall()
        self.connexion.close()
        return all_res

    def display_data(self, how=None):
        """
        Displays data from the database, by default only 10 rows.

        :param how: If it's a number(integer) only that many rows
                    from the database will be printed
                    If it's "all" everything will be printed.
        """
        res_all = self.fetch_all_data()
        cpt = 10
        if type(how) == int:
            cpt = how
        elif how == 'all':
            cpt = len(res_all)
        for line in res_all:
            print(line)
            if cpt < 0:
                break
            cpt = cpt - 1
