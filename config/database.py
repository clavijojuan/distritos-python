from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

run_env = config('RUN_ENV', default='production')

if run_env == 'production':
    DATABASE_URL = config('DATABASE_URL_PRODUCTION')
elif run_env == 'test': 
    DATABASE_URL = config('DATABASE_URL_TEST')
elif run_env == 'development': 
    DATABASE_URL = config('DATABASE_URL_DEVELOPMENT')
else:
    raise ValueError("RUN ENV debe ser 'production','test' or 'development'")

engine = create_engine(DATABASE_URL)
print(run_env)
SessionLocal = sessionmaker(autocommit =False, autoflush=False, bind=engine)

Base = declarative_base()