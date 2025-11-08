#!/bin/bash

echo 正在修复database.py文件...

# 创建临时文件
tmp_file=/tmp/tmp.MoexE1gkF5

# 写入正确的内容
cat >  <<  PYTHON_CODE
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取MySQL数据库配置
DB_HOST = os.getenv(DB_HOST, 192.168.1.12)
DB_USER = os.getenv(DB_USER, kis)
DB_PASSWORD = os.getenv(DB_PASSWORD, Kis9090)
DB_NAME = os.getenv(DB_NAME, kis)

# 构建MySQL连接URL
DATABASE_URL = fmysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()

# 数据库会话实例
db_session = SessionLocal()

def init_db():
    "初始化数据库，创建所有表"
    # 导入所有模型，确保它们被注册到Base.metadata
    from src.models import user, product, tracking, supplier, device

    # 创建所有表
    Base.metadata.create_all(bind=engine)

def get_db():
    "获取数据库会话的依赖项"
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
PYTHON_CODE

# 复制到目标位置
cp  src/models/database.py

# 清理临时文件
rm -f 

echo 文件已修复，验证内容和语法: 
cat src/models/database.py
python3 -m py_compile src/models/database.py && echo 语法检查通过 || echo 语法错误
