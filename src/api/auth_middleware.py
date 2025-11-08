from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.models.user import User
from src.models.database import db_session

def jwt_required(fn):
    """验证JWT令牌的装饰器"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            # 返回字典而不是jsonify对象，以兼容Flask-RESTful
            return {'message': '未授权访问', 'error': str(e)}, 401
    return wrapper

def roles_required(*required_roles):
    """验证用户角色的装饰器"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = db_session.query(User).filter_by(id=user_id).first()
                
                if not user:
                    # 返回字典而不是jsonify对象，以兼容Flask-RESTful
                    return {'message': '用户不存在'}, 404
                
                # 检查用户角色是否在允许的角色列表中
                if user.role not in required_roles:
                    # 返回字典而不是jsonify对象，以兼容Flask-RESTful
                    return {'message': '权限不足'}, 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                # 返回字典而不是jsonify对象，以兼容Flask-RESTful
                return {'message': '授权失败', 'error': str(e)}, 401
        return wrapper
    return decorator

def get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    return db_session.query(User).filter_by(id=user_id).first()