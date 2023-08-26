from sqlalchemy import create_engine
import pandas as pd

db_connection_str = "mysql+pymysql://root:tkdgnl213.!!@127.0.0.1/webbook"
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()
df = pd.read_sql("SELECT * FROM tb_book", con=conn)
