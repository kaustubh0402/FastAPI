import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
load_dotenv()

database_url=os.getenv("database_url")
database_password=os.getenv("database_password")
engine= create_engine(database_url%quote_plus(database_password))

metadata= MetaData()

sessionlocal= sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base =declarative_base()
