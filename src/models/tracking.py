from datetime import datetime
from src.models.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import relationship

class TrackingData(Base):
    __tablename__ = 'tracking_data'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # 创建者ID
    qr_code = Column(String(255), unique=True, nullable=False)  # 二维码信息
    blockchain_hash = Column(String(255), nullable=True)  # 区块链哈希值
    current_location = Column(String(255), nullable=True)
    current_status = Column(String(50), nullable=False, default='in_factory')
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 操作记录列表（存储在MongoDB中，这里只存储引用ID）
    operation_logs_ref = Column(String(255), nullable=True)
    
    def to_dict(self):
        """将追踪数据转换为字典"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'qr_code': self.qr_code,
            'blockchain_hash': self.blockchain_hash,
            'current_location': self.current_location,
            'current_status': self.current_status,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProductionRecord(Base):
    __tablename__ = 'production_records'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    process_step = Column(String(100), nullable=False)
    equipment_id = Column(Integer, ForeignKey('devices.id'), nullable=True)
    operator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    parameters = Column(JSON, nullable=True)  # 生产参数
    notes = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default='completed')  # pending, in_progress, completed, failed
    
    def to_dict(self):
        """将生产记录转换为字典"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'process_step': self.process_step,
            'equipment_id': self.equipment_id,
            'operator_id': self.operator_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'parameters': self.parameters,
            'notes': self.notes,
            'status': self.status
        }

class QualityCheck(Base):
    __tablename__ = 'quality_checks'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    inspector_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    check_time = Column(DateTime, default=datetime.utcnow)
    check_type = Column(String(50), nullable=False)  # incoming, in_process, final
    check_items = Column(JSON, nullable=False)  # 检查项和结果
    pass_status = Column(Boolean, nullable=False)
    comments = Column(Text, nullable=True)
    images = Column(JSON, nullable=True)  # 检查图片路径列表
    
    def to_dict(self):
        """将质量检查记录转换为字典"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'inspector_id': self.inspector_id,
            'check_time': self.check_time.isoformat() if self.check_time else None,
            'check_type': self.check_type,
            'check_items': self.check_items,
            'pass_status': self.pass_status,
            'comments': self.comments,
            'images': self.images
        }