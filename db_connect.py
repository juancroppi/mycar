import pymysql

def connect_to_database():
    try:
        connection = pymysql.connect(host='roundhouse.proxy.rlwy.net', user='root', passwd='htZJrwSaApIDPhxYlXQyUdLeiMHrxcOl', db='railway', port=47586)

        cursor = connection.cursor()

        return connection, cursor

    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None, None