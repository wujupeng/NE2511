from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from src.models.database import db_session
from src.models.user import User

class Register(Resource):
    def post(self):
        data = request.get_json()

        # 验证输入
        if not data or not all(key in data for key in ['username', 'email', 'password', 'role']):
            return {'message': '缺少必要的注册信息'}, 400

        # 检查用户名是否已存在
        if db_session.query(User).filter_by(username=data['username']).first():
            return {'message': '用户名已存在'}, 400

        # 检查邮箱是否已存在
        if db_session.query(User).filter_by(email=data['email']).first():
            return {'message': '邮箱已被注册'}, 400

        # 创建新用户
        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data['role'],
            department=data.get('department')
        )
        new_user.set_password(data['password'])

        try:
            db_session.add(new_user)
            db_session.commit()
            return {'message': '注册成功', 'user_id': new_user.id}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '注册失败', 'error': str(e)}, 500

class Login(Resource):
    def post(self):
        data = request.get_json()

        # 验证输入
        if not data or not all(key in data for key in ['username', 'password']):
            return {'message': '请提供用户名和密码'}, 400

        # 查找用户
        user = db_session.query(User).filter_by(username=data['username']).first()

        # 验证用户和密码
        if not user or not user.check_password(data['password']):
            return {'message': '用户名或密码错误'}, 401

        # 检查用户是否激活
        if not user.is_active:
            return {'message': '用户账号已被禁用'}, 403

        # 创建访问令牌 - 这里移除了对app.config的直接依赖
        access_token = create_access_token(identity=user.id)

        return {
            'message': '登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200

class Logout(Resource):
    @jwt_required()
    def post(self):
        # 在实际应用中，可以将令牌加入黑名单
        return {'message': '登出成功'}, 200