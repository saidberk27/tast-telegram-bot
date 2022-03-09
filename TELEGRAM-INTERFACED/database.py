import sqlite3

def createTable():
    veriTabaniCursor.execute("CREATE TABLE users(username,saved_groups,saved_ads)")
    veriTabani.commit()
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertData(adName,adText):
    veriTabaniCursor.execute("insert into users values (?,?,?)",("Test User","Test Name","Ad Text Ad Text Ad Text Ad Text Ad TextAd Text"))
    veriTabani.commit()
if __name__ == '__main__':
    veriTabani = sqlite3.connect("mainDB.db")
    veriTabaniCursor = veriTabani.cursor()

    createTable()
    insertData("test-name one","Ad Text Ad Text Ad Text Ad Text Ad TextAd Text")