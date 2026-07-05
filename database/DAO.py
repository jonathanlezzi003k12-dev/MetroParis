from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result



    @staticmethod
    def hasconn(u,v):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazp=%s and c.id_stazA=%s"
        #devo dare i due paramentri e li posso dare attraverso il comando execute
        #in questo caso io devo passare l'id della fermata e quindi per farlo
        #devo richiamare il parametro id fermata dall'oggetto di tipo stazione
        cursor.execute(query,(u.id_fermata,v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result)>0

    @staticmethod
    def getvicini(u):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP=%s"

        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #DEVO ESERCITARMI SULLE QUERY
        query = "SELECT id_stazP,id_stazA, count(*) as peso FROM connessione c group by id_stazP,idstazA order by peso desc"
        cursor.execute(query)

        for row in cursor:
            #DEVO ESERCITARMI SULLO SPACCHETTARE I RISULTATI DA UNA QUERY
            result.append((row["id_stazP"],row["id_stazA"],row["peso"]))
        cursor.close()
        conn.close()
        return result


