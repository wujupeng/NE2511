from flask import request, jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.tracking import TrackingData, ProductionRecord, QualityCheck
from src.models.product import Product
from src.api.auth_middleware import jwt_required, roles_required
import qrcode
import hashlib
import os
from datetime import datetime

class TrackingDataList(Resource):
    @jwt_required
    def get(self):
        """获取追踪数据列表"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            status = request.args.get('status')
            
            query = TrackingData.query
            
            if status:
                query = query.filter_by(current_status=status)
            
            pagination = query.order_by(TrackingData.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            tracking_data = pagination.items
            total = pagination.total
            
            return {
                'tracking_data': [td.to_dict() for td in tracking_data],
                'total': total,
                'page': page,
                'per_page': per_page
            }, 200
        except Exception as e:
            return {'message': '获取追踪数据失败', 'error': str(e)}, 500
    
    @roles_required('admin', 'manager')
    def post(self):
        """创建追踪数据"""
        try:
            data = request.get_json()
            
            if not data or 'product_id' not in data:
                return {'message': '缺少产品ID'}, 400
            
            # 检查产品是否存在
            product = Product.query.get(data['product_id'])
            if not product:
                return {'message': '产品不存在'}, 404
            
            # 检查是否已有追踪数据
            if TrackingData.query.filter_by(product_id=data['product_id']).first():
                return {'message': '该产品已有追踪数据'}, 400
            
            # 生成二维码和区块链哈希
            qr_data = f"PRODUCT:{data['product_id']}:{datetime.utcnow().isoformat()}"
            blockchain_hash = hashlib.sha256(qr_data.encode()).hexdigest()
            
            # 保存二维码图片（在实际应用中实现）
            # generate_qr_code(qr_data, f"static/qrcodes/{product.product_code}.png")
            
            # 创建追踪数据
            new_tracking = TrackingData(
                product_id=data['product_id'],
                qr_code=qr_data,
                blockchain_hash=blockchain_hash,
                current_location=data.get('location', 'factory'),
                current_status=data.get('status', 'in_factory')
            )
            
            db_session.add(new_tracking)
            db_session.commit()
            
            return {'message': '追踪数据创建成功', 'tracking': new_tracking.to_dict()}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '追踪数据创建失败', 'error': str(e)}, 500

class TrackingDataDetail(Resource):
    @jwt_required
    def get(self, tracking_id):
        """获取追踪数据详情"""
        tracking = TrackingData.query.get(tracking_id)
        if not tracking:
            return {'message': '追踪数据不存在'}, 404
        
        return {'tracking': tracking.to_dict()}, 200
    
    @roles_required('admin', 'manager')
    def put(self, tracking_id):
        """更新追踪数据"""
        tracking = TrackingData.query.get(tracking_id)
        if not tracking:
            return {'message': '追踪数据不存在'}, 404
        
        try:
            data = request.get_json()
            
            # 更新追踪信息
            if 'current_location' in data:
                tracking.current_location = data['current_location']
            if 'current_status' in data:
                tracking.current_status = data['current_status']
            
            tracking.last_updated = datetime.utcnow()
            db_session.commit()
            
            return {'message': '追踪数据更新成功', 'tracking': tracking.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '追踪数据更新失败', 'error': str(e)}, 500

class QRCodeScan(Resource):
    @jwt_required
    def post(self):
        """扫描二维码获取追踪信息"""
        try:
            data = request.get_json()
            
            if not data or 'qr_code' not in data:
                return {'message': '缺少二维码数据'}, 400
            
            # 查找追踪数据
            tracking = TrackingData.query.filter_by(qr_code=data['qr_code']).first()
            if not tracking:
                return {'message': '未找到对应的产品信息'}, 404
            
            # 获取关联的产品信息
            product = Product.query.get(tracking.product_id)
            
            # 获取生产记录
            production_records = ProductionRecord.query.filter_by(product_id=tracking.product_id).all()
            
            return {
                'tracking': tracking.to_dict(),
                'product': product.to_dict() if product else None,
                'production_history': [record.to_dict() for record in production_records]
            }, 200
        except Exception as e:
            return {'message': '扫描失败', 'error': str(e)}, 500

class TrackingHistory(Resource):
    @jwt_required
    def get(self, product_id):
        """获取产品的完整追踪历史"""
        try:
            # 检查产品是否存在
            product = Product.query.get(product_id)
            if not product:
                return {'message': '产品不存在'}, 404
            
            # 获取追踪数据
            tracking = TrackingData.query.filter_by(product_id=product_id).first()
            
            # 获取生产记录
            production_records = ProductionRecord.query.filter_by(product_id=product_id).all()
            
            # 在实际应用中，这里还可以从MongoDB获取更详细的操作日志
            
            return {
                'product': product.to_dict(),
                'tracking': tracking.to_dict() if tracking else None,
                'production_history': [record.to_dict() for record in production_records]
            }, 200
        except Exception as e:
            return {'message': '获取追踪历史失败', 'error': str(e)}, 500