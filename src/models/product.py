from datetime import datetime
from src.models.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_code = Column(String(50), unique=True, nullable=False)
    product_name = Column(String(200), nullable=False)
    product_type = Column(String(100), nullable=False)  # 电池、电机、电控等
    specifications = Column(JSON, nullable=True)  # 产品规格参数
    manufacturer = Column(String(100), nullable=False)
    production_date = Column(DateTime, nullable=False)
    warranty_period = Column(Integer, nullable=True)  # 保修期限（天）
    status = Column(String(20), nullable=False, default='produced')  # produced, shipped, sold, recalled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系定义
    tracking_data = relationship('TrackingData', backref='product', lazy=True, uselist=False)
    production_records = relationship('ProductionRecord', backref='product', lazy=True)
    quality_checks = relationship('QualityCheck', backref='product', lazy=True)
    
    def to_dict(self):
        """将产品对象转换为字典"""
        return {
            'id': self.id,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'product_type': self.product_type,
            'specifications': self.specifications,
            'manufacturer': self.manufacturer,
            'production_date': self.production_date.isoformat() if self.production_date else None,
            'warranty_period': self.warranty_period,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.product_code}: {self.product_name}>'