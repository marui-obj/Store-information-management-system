import mysql.connector as mysql

class Command():
    def __init__(self):
        self.connect()
        self.cursor = self.database.cursor()

    def connect(self):
        self.database = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "Smoking8949_",
            database = "rsp_database"
        )
    def getItem(self, barcode):
        ''' this function use for get item data by using barcode '''

        query = "SELECT name, price, type FROM goods_table WHERE bar_code = %s"

        barcode = str(barcode)

        self.cursor.execute(query, (barcode, ))

        for name, price, item_type in self.cursor:
            return name, price, item_type


if __name__ == "__main__":

    database = Command()
