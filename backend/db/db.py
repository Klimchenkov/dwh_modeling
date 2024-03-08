from sqlalchemy import create_engine

url = 'postgresql://postgres:postgres@localhost:5432/postgres'

engine = create_engine(url)