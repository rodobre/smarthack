from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from redis_collections import Dict
import redislite

# database stored in a file (simplest way)
# TODO: change engine type if needed
db_uri = "sqlite:///database.sql"
engine = create_engine(db_uri)

Base = declarative_base()
Session = sessionmaker(bind = engine)

cache_uri = 'storage.rdb'
redis_connection = redislite.StrictRedis(cache_uri)
Cache = Dict(redis=redis_connection, key='storage')
