from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class KvartiryBase:
    def __init__(self, base, base_url):
        engine = create_engine(base_url)
        session_db = sessionmaker(bind=engine)
        self.session = session_db()
