from flask import request, jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.supplier import Supplier
from src.api.auth_middleware import jwt_required, roles_required
from datetime import datetime

class SupplierList(Resource):
    @jwt_required
    def get(self):
        """获取供应商列表"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            status = request.args.get('status')
            
            query = db_session.query(Supplier)
            
            if status:
                query = query.filter_by(status=status)
            
            pagination = query.order_by(Supplier.supplier_name).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            suppliers = pagination.items
            total = pagination.total
            
            return {
                'suppliers': [supplier.to_dict() for supplier in suppliers],
                'total': total,
                'page': page,
                'per_page': per_page
            }, 200
        except Exception as e:
            return {'message': '获取供应商列表失败', 'error': str(e)}, 500
    
    @roles_required('admin', 'manager')
    def post(self):
        """创建新供应商"""
        try:
            data = request.get_json()
            
            # 验证输入
            if not data or not all(key in data for key in ['supplier_code', 'supplier_name', 'contact_person', 'contact_phone']):
                return {'message': '缺少必要的供应商信息'}, 400
            
            # 检查供应商编码是否已存在
            if db_session.query(Supplier).filter_by(supplier_code=data['supplier_code']).first():
                return {'message': '供应商编码已存在'}, 400
            
            # 创建新供应商
            new_supplier = Supplier(**data)
            db_session.add(new_supplier)
            db_session.commit()
            
            return {'message': '供应商创建成功', 'supplier': new_supplier.to_dict()}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '供应商创建失败', 'error': str(e)}, 500

class SupplierDetail(Resource):
    @jwt_required
    def get(self, supplier_id):
        """获取供应商详情"""
        supplier = db_session.query(Supplier).filter_by(id=supplier_id).first()
        if not supplier:
            return {'message': '供应商不存在'}, 404
        
        return {'supplier': supplier.to_dict()}, 200
    
    @roles_required('admin', 'manager')
    def put(self, supplier_id):
        """更新供应商信息"""
        supplier = db_session.query(Supplier).filter_by(id=supplier_id).first()
        if not supplier:
            return {'message': '供应商不存在'}, 404
        
        try:
            data = request.get_json()
            
            # 更新供应商信息
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    if hasattr(supplier, key):
                        setattr(supplier, key, value)
            
            supplier.updated_at = datetime.utcnow()
            db_session.commit()
            
            return {'message': '供应商信息更新成功', 'supplier': supplier.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '供应商信息更新失败', 'error': str(e)}, 500
    
    @roles_required('admin')
    def delete(self, supplier_id):
        """删除供应商"""
        supplier = db_session.query(Supplier).filter_by(id=supplier_id).first()
        if not supplier:
            return {'message': '供应商不存在'}, 404
        
        try:
            db_session.delete(supplier)
            db_session.commit()
            return {'message': '供应商删除成功'}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '供应商删除失败', 'error': str(e)}, 500