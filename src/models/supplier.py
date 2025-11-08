from datetime import datetime
from src.models.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.orm import relationship

class Supplier(Base):
    __tablename__ = 'suppliers'
    
    id = Column(Integer, primary_key=True)
    supplier_code = Column(String(50), unique=True, nullable=False)
    supplier_name = Column(String(200), nullable=False)
    contact_person = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    contact_email = Column(String(120), nullable=True)
    address = Column(Text, nullable=True)
    business_license = Column(String(255), nullable=True)  # 营业执照图片路径
    qualification_certificates = Column(JSON, nullable=True)  # 资质证书图片路径列表
    supply_materials = Column(JSON, nullable=True)  # 供应材料列表
    rating = Column(Float, nullable=True)  # 供应商评级
    status = Column(String(20), nullable=False, default='active')  # active, inactive, suspended
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """将供应商信息转换为字典"""
        return {
            'id': self.id,
            'supplier_code': self.supplier_code,
            'supplier_name': self.supplier_name,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'address': self.address,
            'rating': self.rating,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Supplier {self.supplier_code}: {self.supplier_name}>'