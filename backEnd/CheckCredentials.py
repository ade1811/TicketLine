#import mysql.connector
import psycopg2 as mysql

class CheckCredential():
    def __init__(self, matricola, password, nomeEvento) -> None:
        self.engine = mysql.connect(username = "root", password = "Vins1811!", database = "ticket_line")
        self.crs = self.engine.cursor()

        self.matricola = matricola
        self.password = password
        self.nomeEvento = nomeEvento

    def logIn(self)->bool:
        query = "SELECT password FROM promoter WHERE PrMatricola = '"+str(self.matricola)+"'"

        self.crs.execute(query)
        password = self.crs.fetchone()

        if self.password == password[0]:
            return True
        else:
            return False