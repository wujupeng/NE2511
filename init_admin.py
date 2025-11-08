#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化管理员账号脚本
设置用户名为admin，密码为admin
"""

import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 加载环境变量
load_dotenv()

# 初始化数据库连接
try:
    # 使用MySQL数据库（从环境变量读取配置）
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    # 构建MySQL连接URL
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    
    print(f"使用MySQL数据库连接: {DATABASE_URL.replace(DB_PASSWORD, '****')}")

    # 创建数据库引擎
    engine = create_engine(DATABASE_URL, echo=True)

    # 创建会话工厂
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 创建Base类
    Base = declarative_base()

    # 定义User模型
    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        username = Column(String(80), unique=True, nullable=False)
        email = Column(String(120), unique=True, nullable=False)
        password_hash = Column(String(128), nullable=False)
        role = Column(String(20), nullable=False)
        department = Column(String(50))
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        is_active = Column(Boolean, default=True)

        def set_password(self, password):
            # 使用bcrypt进行密码哈希
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        def check_password(self, password):
            # 验证密码
            password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, self.password_hash.encode('utf-8'))

    # 创建数据库表（如果不存在）
    print("创建数据库表（如果不存在）...")
    Base.metadata.create_all(bind=engine)

    # 创建数据库会话
    db = SessionLocal()

    try:
        # 检查是否已存在admin用户
        print("检查admin用户是否存在...")
        admin_user = db.query(User).filter_by(username='admin').first()

        if admin_user:
            print("✅ 管理员账号 'admin' 已存在")
            print("\n更新管理员密码为 'admin'...")
            admin_user.set_password('admin')
            admin_user.is_active = True
            admin_user.updated_at = datetime.utcnow()
            db.commit()
            print("✅ 管理员密码已更新为 'admin'")
        else:
            # 创建新的管理员用户
            print("\n创建新的管理员用户...")
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin',  # 设置为管理员角色
                department='管理部门',
                is_active=True
            )
            admin_user.set_password('admin')  # 设置密码

            db.add(admin_user)
            db.commit()
            print("✅ 管理员账号创建成功!")
            print("用户名: admin")
            print("密码: admin")
            print("角色: admin")

    except Exception as e:
        db.rollback()
        print(f"❌ 数据库操作失败: {str(e)}")

    finally:
        db.close()
        print("\n数据库会话已关闭")

    print("\n✅ 管理员账号设置完成!")
    print("请使用以下凭据登录:")
    print("用户名: admin")
    print("密码: admin")

except ImportError as e:
    print(f"❌ 导入错误: {str(e)}")
    print("请确保已安装所有依赖包")
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
    print("请检查数据库连接是否正常")
    print(f"数据库URL: {DATABASE_URL.replace(DB_PASSWORD, '****')}")
finally:
    print("\n脚本执行完成")
