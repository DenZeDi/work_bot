from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///hookah.db', echo=True)
meta = MetaData()

clients = Table(
    'clients', meta,
    Column('client_id', Integer, primary_key=True),
    Column('client_username', String),
    Column('client_name', String),
    Column('phone_number', String),
    Column('reservation_time', String),
    Column('reservation_day', String),
    Column('amount_of_people', Integer)
)
feedback = Table(
    'feedback', meta,
    Column('client_id', Integer, primary_key=True),
    Column('client_username', String),
    Column('client_name', String),
    Column('feedback', String)
)
meta.create_all(engine)

# conn = engine.connect()
# conn.execute(clients.drop(engine))
# conn = engine.connect()
# conn.execute(feedback.drop(engine))
