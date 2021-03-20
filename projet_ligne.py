import numpy as np
import matplotlib.pyplot as plt
import sqlite3

def Brownian_trajectory(N, m):
    dt = 1/m
    Z = np.random.normal(0, 1, size=(N, m))
    W = np.zeros((N, m+1))
    space = np.linspace(0, 1, m+1)
    for i in range(m):
        W[:, i+1] = W[:, i] + (np.sqrt(dt)*Z[:,i])
    
    return space, W

def Brownian_trajectory_multidensional(N, m, correlation_matrix):
    dt = 1/m
    space = np.linspace(0, 1, m+1)
    results = list()
    d, trash = correlation_matrix.shape 
    Choleski = np.linalg.cholesky(correlation_matrix)
    for j in range(N):
        Z = np.random.normal(0, 1, size=(N, m))
        W = np.zeros((d, m+1))
        
        for i in range(m):
            W[:, i+1] = W[:, i] + (np.sqrt(dt)*Z[:,i])
        
        Wcorr = np.zeros((d, m+1))
        for i in range(1,m+1):
            Wcorr[:,i] = np.matmul(W[:,i], Choleski)
            
        results.append(Wcorr)
    return space, results

class BrownianTrajectory:

    def __init__(self, data_base_name="brown_5_database.db"):
        
        try:
            self.connexion = sqlite3.connect(data_base_name, timeout = 60)
            print("Sqllite version ::: {}".format(sqlite3.version))
        except Error as error:
            print(error)
        finally:
            if self.connexion:
                (self.connexion).close()
                
        self.data_path = data_base_name
 
        
    def create_table(self, sql_file_name):
        self.connexion = sqlite3.connect(self.data_path, timeout = 10)
        self.sql_script_path = sql_file_name
        cursor = self.connexion.cursor()
        sql_file = open(sql_file_name)
        sql_str = sql_file.read()
        try:
            cursor.executescript(sql_str)
        except Exception as error:
            print("error in in creating table")
            print(error)
        cursor.close()
        (self.connexion).close()
    
    def add_trajectory(self, space, B):
        self.connexion = sqlite3.connect(self.data_path, timeout = 10)
        N = np.size(space)
        for i in range(N):
            self.connexion.execute("INSERT INTO data (`time_`, `Brown1`, `Brown2`, `Brown3`, `Brown4`) VALUES (?,?,?,?,?)",
                                   (space[i], B[0,i], B[1,i], B[2,i], B[3,i]))
            
        self.connexion.commit()
        (self.connexion).close()
        
    def get_all_lines(self):
        self.connexion = sqlite3.connect(self.data_path, timeout = 10)
        cursor = self.connexion.cursor()
        cursor.execute("SELECT * FROM data")
        all_res = cursor.fetchall()
        (self.connexion).close()
        
        return all_res
    
    def display_db(self, N = None):
        res_all = self.get_all_lines()
        cpt = 10
        if N is not None:
            cpt = N
        for line in res_all:
            print(line)
            if cpt < 0:
                break
            cpt = cpt-1
            
    def initialization(self):
        self.connexion = sqlite3.connect(self.data_path, timeout = 10)
        cursor = self.connexion.cursor()
        cursor.execute("Delete from data")
        self.connexion.commit()


brownian_base = BrownianTrajectory()
brownian_base.create_table("sql_queries.sql")

space, B = Brownian_trajectory(5,1000)
_ = plt.plot(space, B[0,:])
_ = plt.plot(space, B[1,:])
_ = plt.plot(space, B[2,:])
_ = plt.plot(space, B[3,:])

print(np.shape(space))
print(np.shape(B))

# Initialization fo database
brownian_base.initialization()
length = 10
all_size = np.size(space)
# Insert brownian motion series into database
for i in range(np.size(space)//length):
    brownian_base.add_trajectory(space[i*length:(i+1)*length], B[:,i*length:(i+1)*length])

brownian_base.display_db()