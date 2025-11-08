from flask import request, jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.device import Device
from src.api.auth_middleware import jwt_required, roles_required
from datetime import datetime

class DeviceList(Resource):
    @jwt_required
    def get(self):
        """获取设备列表"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            device_type = request.args.get('type')
            status = request.args.get('status')
            location = request.args.get('location')
            
            query = db_session.query(Device)
            
            if device_type:
                query = query.filter_by(device_type=device_type)
            
            if status:
                query = query.filter_by(status=status)
            
            if location:
                query = query.filter_by(location=location)
            
            pagination = query.order_by(Device.device_name).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            devices = pagination.items
            total = pagination.total
            
            return {
                'devices': [device.to_dict() for device in devices],
                'total': total,
                'page': page,
                'per_page': per_page
            }, 200
        except Exception as e:
            return {'message': '获取设备列表失败', 'error': str(e)}, 500
    
    @roles_required('admin', 'manager')
    def post(self):
        """创建设备"""
        try:
            data = request.get_json()
            
            # 验证输入
            if not data or not all(key in data for key in ['device_code', 'device_name', 'device_type']):
                return {'message': '缺少必要的设备信息'}, 400
            
            # 检查设备编码是否已存在
            if db_session.query(Device).filter_by(device_code=data['device_code']).first():
                return {'message': '设备编码已存在'}, 400
            
            # 创建设备
            new_device = Device(**data)
            db_session.add(new_device)
            db_session.commit()
            
            return {'message': '设备创建成功', 'device': new_device.to_dict()}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '设备创建失败', 'error': str(e)}, 500

class DeviceDetail(Resource):
    @jwt_required
    def get(self, device_id):
        """获取设备详情"""
        device = db_session.query(Device).filter_by(id=device_id).first()
        if not device:
            return {'message': '设备不存在'}, 404
        
        return {'device': device.to_dict()}, 200
    
    @roles_required('admin', 'manager')
    def put(self, device_id):
        """更新设备信息"""
        device = db_session.query(Device).filter_by(id=device_id).first()
        if not device:
            return {'message': '设备不存在'}, 404
        
        try:
            data = request.get_json()
            
            # 更新设备信息
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    if hasattr(device, key):
                        setattr(device, key, value)
            
            device.updated_at = datetime.utcnow()
            db_session.commit()
            
            return {'message': '设备信息更新成功', 'device': device.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '设备信息更新失败', 'error': str(e)}, 500
    
    @roles_required('admin')
    def delete(self, device_id):
        """删除设备"""
        device = db_session.query(Device).filter_by(id=device_id).first()
        if not device:
            return {'message': '设备不存在'}, 404
        
        try:
            db_session.delete(device)
            db_session.commit()
            return {'message': '设备删除成功'}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '设备删除失败', 'error': str(e)}, 500