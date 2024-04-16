import qrcode as qc
import mysql.connector
#import psycopg2 as mysql

class GenerateTicket():
    def __init__(self, nomeEvento, PrMatrix):
        #costruttore
        self.PrMat = PrMatrix
        self.nomeEvento = nomeEvento
        #engine e cursor per mysql
        self.engine = mysql.connector.connect(host = "vrossi6.mysql.pythonanywhere-services.com",
        username = "vrossi6", password = "Vins1811!", database = "vrossi6$ticket_line")
        self.crs = self.engine.cursor()

    def generate(self):
        #genero qr code e salvo in jpg
        MT = self._getMatricolaBiglietto()
        self.codiceBiglietto = str(self.nomeEvento) + "_" + str(self.PrMat) + "_" + str(MT) #data
        self.qr = qc.QRCode(version=5, box_size=10, border=2)   #creo attributo qr

        self.qr.add_data(self.codiceBiglietto)
        self.qr.make(fit = True)

        img = self.qr.make_image(fill='black', back_color='white')
        img_path = "/home/vrossi6/mysite" +"/ticket" + str(MT) + ".jpeg"
        img.save(img_path)
        self._putDataOnDB()

        return img_path

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

if __name__ == "__main__":
    gen = GenerateTicket("adimentional", "778272")
    img = gen.generate()
    print(img)