print(正在修复database.py文件...)
with open(src/models/database.py, w) as f:
    f.write("
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv(DB_HOST, 192.168.1.12)
DB_USER = os.getenv(DB_USER, kis)
DB_PASSWORD = os.getenv(DB_PASSWORD, Kis9090)
DB_NAME = os.getenv(DB_NAME, kis)

DATABASE_URL = fmysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}

engine = create_engine(
 DATABASE_URL,
 echo=True,
 pool_pre_ping=True,
 pool_recycle=3600,
 pool_size=5,
 max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db_session = SessionLocal()

def init_db():
 from src.models import user, product, tracking, supplier, device
 Base.metadata.create_all(bind=engine)

def get_db():
 db = SessionLocal()
 try:
 yield db
 finally:
 db.close()
")
print(文件创建完成，检查语法...)
try:
    import py_compile
    py_compile.compile(src/models/database.py)
    print(语法检查通过！)
except Exception as e:
    print(f语法错误: {e})
