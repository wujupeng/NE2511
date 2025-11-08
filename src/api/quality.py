from flask import request, jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.tracking import QualityCheck
from src.models.product import Product
from src.api.auth_middleware import jwt_required, roles_required
from src.api.auth_middleware import get_current_user
from datetime import datetime

class QualityCheckList(Resource):
    @jwt_required
    def get(self):
        """获取质量检查列表"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            product_id = request.args.get('product_id', type=int)
            check_type = request.args.get('type')
            pass_status = request.args.get('pass', type=bool)
            
            query = db_session.query(QualityCheck)
            
            if product_id:
                query = query.filter_by(product_id=product_id)
            
            if check_type:
                query = query.filter_by(check_type=check_type)
            
            if pass_status is not None:
                query = query.filter_by(pass_status=pass_status)
            
            pagination = query.order_by(QualityCheck.check_time.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            quality_checks = pagination.items
            total = pagination.total
            
            return {
                'quality_checks': [qc.to_dict() for qc in quality_checks],
                'total': total,
                'page': page,
                'per_page': per_page
            }, 200
        except Exception as e:
            return {'message': '获取质量检查列表失败', 'error': str(e)}, 500
    
    @roles_required('admin', 'manager', 'inspector')
    def post(self):
        """创建质量检查记录"""
        try:
            data = request.get_json()
            
            # 验证输入
            if not data or not all(key in data for key in ['product_id', 'check_type', 'check_items', 'pass_status']):
                return {'message': '缺少必要的质量检查信息'}, 400
            
            # 检查产品是否存在
            product = db_session.query(Product).filter_by(id=data['product_id']).first()
            if not product:
                return {'message': '产品不存在'}, 404
            
            # 获取当前用户作为检查员
            inspector = get_current_user()
            
            # 创建质量检查记录
            new_quality_check = QualityCheck(
                product_id=data['product_id'],
                inspector_id=inspector.id,
                check_type=data['check_type'],
                check_items=data['check_items'],
                pass_status=data['pass_status'],
                comments=data.get('comments'),
                images=data.get('images')
            )
            
            db_session.add(new_quality_check)
            db_session.commit()
            
            return {'message': '质量检查记录创建成功', 'quality_check': new_quality_check.to_dict()}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '质量检查记录创建失败', 'error': str(e)}, 500

class QualityCheckDetail(Resource):
    @jwt_required
    def get(self, check_id):
        """获取质量检查详情"""
        quality_check = db_session.query(QualityCheck).filter_by(id=check_id).first()
        if not quality_check:
            return {'message': '质量检查记录不存在'}, 404
        
        return {'quality_check': quality_check.to_dict()}, 200
    
    @roles_required('admin', 'manager', 'inspector')
    def put(self, check_id):
        """更新质量检查记录"""
        quality_check = db_session.query(QualityCheck).filter_by(id=check_id).first()
        if not quality_check:
            return {'message': '质量检查记录不存在'}, 404
        
        try:
            data = request.get_json()
            
            # 更新检查信息
            for key, value in data.items():
                if key not in ['id', 'product_id', 'inspector_id', 'check_time']:
                    if hasattr(quality_check, key):
                        setattr(quality_check, key, value)
            
            db_session.commit()
            return {'message': '质量检查记录更新成功', 'quality_check': quality_check.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '质量检查记录更新失败', 'error': str(e)}, 500
    
    @roles_required('admin')
    def delete(self, check_id):
        """删除质量检查记录"""
        quality_check = db_session.query(QualityCheck).filter_by(id=check_id).first()
        if not quality_check:
            return {'message': '质量检查记录不存在'}, 404
        
        try:
            db_session.delete(quality_check)
            db_session.commit()
            return {'message': '质量检查记录删除成功'}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '质量检查记录删除失败', 'error': str(e)}, 500