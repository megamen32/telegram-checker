
from models.user import User
from models.channel import Channel
from loader import database
def create_tables():
    with database:
        database.create_tables([ User, Channel])
if __name__=='__main__':
    create_tables()