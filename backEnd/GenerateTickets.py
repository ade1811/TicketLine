import qrcode as qc
#import mysql.connector
import psycopg2 as mysql

class GenerateTicket():
    def __init__(self, nomeEvento, PrMatrix):     
        #costruttore 
        self.PrMat = PrMatrix     
        self.nomeEvento = nomeEvento
        #engine e cursor per mysql
        self.engine = mysql.connect(username = "root", password = "Vins1811!", database = "ticket_line")
        self.crs = self.engine.cursor()

    def generate(self,num):
        #genero qr code e salvo in jpg
        MT = self._getMatricolaBiglietto()
        self.codiceBiglietto = str(self.nomeEvento) + "_" + str(self.PrMat) + "_" + str(MT) #data
        self.qr = qc.QRCode(version=5, box_size=10, border=2)   #creo attributo qr 

        self.qr.add_data(self.codiceBiglietto)
        self.qr.make(fit = True)

        img = self.qr.make_image(fill='black', back_color='white')
        imgPath = "ticket" + str(num) + ".jpeg"
        img.save(imgPath)
        self._putDataOnDB()

    def _putDataOnDB(self):
        #creo record e aggiorno DB
        data = str(self.PrMat) +","+ "'"+ str(self.codiceBiglietto)+ "'"

        query = "INSERT INTO "+str(self.nomeEvento) +"(PrMatricola, CodiceBiglietto) VALUES ("+str(data)+");"
        
        self.crs.execute(query)
        self.engine.commit()

    def _getMatricolaBiglietto(self) -> int:
        #funzione che trova il MAX delle matricole e ritorna l'intero
        query = "SELECT MAX(MatricolaBiglietto) FROM " + str(self.nomeEvento)

        self._createIfNotExist()

        self.crs.execute(query)

        risultato = self.crs.fetchone()
        #print(risultato)
        if risultato[0] == None:
            return 1
        else:
            valore_massimo = risultato[0]

        return valore_massimo+1
    
    def _createIfNotExist(self):
        query = "CREATE TABLE IF NOT EXISTS " +str(self.nomeEvento)+" LIKE ticket;"
        self.crs.execute(query)