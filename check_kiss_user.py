import sys
from src.models.database import engine, SessionLocal
from src.models.user import User

db = SessionLocal()
try:
    # 检查kiss用户是否存在
    kiss_user = db.query(User).filter_by(username="kiss").first()
    print("kiss用户存在:", bool(kiss_user))
    
    if kiss_user:
        print("用户ID:", kiss_user.id)
        print("激活状态:", kiss_user.is_active)
        print("角色:", kiss_user.role)
        print("部门:", kiss_user.department)
        print("创建时间:", kiss_user.created_at)
        print("更新时间:", kiss_user.updated_at)
        
        # 尝试使用常见密码测试
        test_passwords = ["kiss", "Kis9090", "password", "admin"]
        print("\n测试密码:")
        for pwd in test_passwords:
            print(f"密码 '{pwd}' 验证结果:", kiss_user.check_password(pwd))
    else:
        print("\n建议操作:")
        print("1. 创建kiss用户")
        print("2. 检查数据库连接")
        print("3. 查看数据库users表中是否有该用户")
        
except Exception as e:
    print(f"查询过程中出错: {e}")
finally:
    db.close()
