import pandas as pd
import db_connection.ihub as ihub
import db_connection.alice as alice

conn = ihub.iHub_engine('expedia').connection
conn2 = alice.alice_engine('hqlive').connection


try:
    with conn2.cursor() as cursor:
        query = """
            select * from hotel limit 5
        """
        cursor.execute(query)
        conn.commit()
        df = pd.read_sql(query, conn2)
finally:
        conn2.close()
