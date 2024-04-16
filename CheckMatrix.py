import mysql.connector
#import psycopg2 as mysql

class CheckMatrix():
    def __init__(self, matricola) -> None:
        self.engine = mysql.connector.connect(host = "vrossi6.mysql.pythonanywhere-services.com",
        username = "vrossi6", password = "Vins1811!", database = "vrossi6$ticket_line")
        self.crs = self.engine.cursor()

        self.matricola = matricola

    def check(self)->bool:
        query = "SELECT CodiceBiglietto FROM adimentional WHERE CodiceBiglietto  = '"+str(self.matricola)+"'"

        self.crs.execute(query)
        matrix = self.crs.fetchall()

        if len(matrix) == 1:
            return True
        else:
            return False