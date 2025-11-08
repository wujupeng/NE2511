import sys
from datetime import datetime
from src.models.database import engine, SessionLocal, Base
from src.models.user import User

db = SessionLocal()
try:
    # 确保数据库表存在
    print("确保数据库表存在...")
    
    # 检查是否已存在kiss用户
    print("检查kiss用户是否存在...")
    existing_user = db.query(User).filter_by(username='kiss').first()
    
    if existing_user:
        print("⚠️ kiss用户已存在")
        print(f"用户ID: {existing_user.id}")
        print(f"激活状态: {existing_user.is_active}")
        print(f"角色: {existing_user.role}")
        
        # 更新用户信息
        print("\n更新kiss用户信息...")
        existing_user.is_active = True
        existing_user.set_password('Kis9090')  # 使用环境变量中的密码
        existing_user.role = 'operator'  # 设置为操作员角色
        existing_user.department = '生产部门'
        existing_user.updated_at = datetime.utcnow()
        
        db.commit()
        print("✅ kiss用户信息已更新")
        print("用户名: kiss")
        print("密码: Kis9090")
        print("角色: operator")
        print("激活状态: True")
    else:
        # 创建新的kiss用户
        print("\n创建新的kiss用户...")
        new_user = User(
            username='kiss',
            email='kiss@example.com',
            role='operator',  # 设置为操作员角色
            department='生产部门',
            is_active=True
        )
        new_user.set_password('Kis9090')  # 使用环境变量中的密码
        
        db.add(new_user)
        db.commit()
        print("✅ kiss用户创建成功!")
        print("用户名: kiss")
        print("密码: Kis9090")
        print("角色: operator")
        print("部门: 生产部门")
        
except Exception as e:
    db.rollback()
    print(f"❌ 数据库操作失败: {str(e)}")
finally:
    db.close()
    print("\n✅ 脚本执行完成")
