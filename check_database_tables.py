#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查并初始化数据库所有表
"""

from sqlalchemy import inspect
from src.models.database import engine, Base
from src.models.user import User
from src.models.device import Device
from src.models.product import Product
from src.models.supplier import Supplier
from src.models.tracking import ProductionRecord, QualityCheck

def check_and_create_tables():
    print("检查数据库表...")
    
    # 获取所有已定义的模型
    models = [User, Device, Product, Supplier, ProductionRecord, QualityCheck]
    
    # 获取数据库中的表
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print(f"数据库中已存在的表: {existing_tables}")
    print("需要创建的模型表:")
    
    # 检查每个模型的表是否存在
    tables_to_create = []
    for model in models:
        table_name = model.__tablename__
        if table_name in existing_tables:
            print(f"✅ {table_name} 表已存在")
        else:
            print(f"❌ {table_name} 表不存在，需要创建")
            tables_to_create.append(table_name)
    
    # 创建不存在的表
    if tables_to_create:
        print(f"\n开始创建 {len(tables_to_create)} 个表...")
        Base.metadata.create_all(bind=engine)
        print("✅ 所有表创建完成")
    else:
        print("\n✅ 所有表都已存在，无需创建")

if __name__ == "__main__":
    try:
        check_and_create_tables()
    except Exception as e:
        print(f"❌ 检查数据库表时出错: {str(e)}")
