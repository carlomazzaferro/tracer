from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from tracer.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)