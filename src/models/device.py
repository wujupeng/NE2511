from datetime import datetime
from src.models.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = 'devices'
    
    id = Column(Integer, primary_key=True)
    device_code = Column(String(50), unique=True, nullable=False)
    device_name = Column(String(200), nullable=False)
    device_type = Column(String(100), nullable=False)  # 生产线、检测设备、仓储设备等
    location = Column(String(255), nullable=True)
    status = Column(String(20), nullable=False, default='active')  # active, maintenance, inactive
    last_maintenance = Column(DateTime, nullable=True)
    next_maintenance = Column(DateTime, nullable=True)
    specifications = Column(JSON, nullable=True)  # 设备规格参数
    manufacturer = Column(String(100), nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系定义
    production_records = relationship('ProductionRecord', backref='equipment', lazy=True)
    
    def to_dict(self):
        """将设备信息转换为字典"""
        return {
            'id': self.id,
            'device_code': self.device_code,
            'device_name': self.device_name,
            'device_type': self.device_type,
            'location': self.location,
            'status': self.status,
            'last_maintenance': self.last_maintenance.isoformat() if self.last_maintenance else None,
            'next_maintenance': self.next_maintenance.isoformat() if self.next_maintenance else None,
            'specifications': self.specifications,
            'manufacturer': self.manufacturer,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Device {self.device_code}: {self.device_name}>'