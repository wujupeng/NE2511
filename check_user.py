import sys
from src.models.database import engine, SessionLocal
from src.models.user import User

db = SessionLocal()
try:
    admin = db.query(User).filter_by(username="admin").first()
    print("用户存在:", bool(admin))
    if admin:
        print("用户ID:", admin.id)
        print("激活状态:", admin.is_active)
        print("角色:", admin.role)
        # 直接使用admin作为密码
        test_password = "admin"
        print("密码验证结果:", admin.check_password(test_password))
finally:
    db.close()
