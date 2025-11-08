from flask_restful import Resource
from flask import Blueprint, render_template
from src.api.auth import Login, Register, Logout
from src.api.products import ProductList, ProductDetail, ProductSearch
from src.api.tracking import TrackingDataList, TrackingDataDetail, QRCodeScan, TrackingHistory
from src.api.quality import QualityCheckList, QualityCheckDetail
from src.api.suppliers import SupplierList, SupplierDetail
from src.api.devices import DeviceList, DeviceDetail
from src.api.dashboard import DashboardStats
from src.api.auth_middleware import jwt_required, roles_required

# 创建Blueprint用于前端页面
web_bp = Blueprint('web', __name__, template_folder='../../src/templates')

def register_routes(api, app):
    """注册所有API路由"""
    # 认证相关路由
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Logout, '/api/auth/logout')
    
    # 产品相关路由
    api.add_resource(ProductList, '/api/products')
    api.add_resource(ProductDetail, '/api/products/<int:product_id>')
    api.add_resource(ProductSearch, '/api/products/search')
    
    # 追踪相关路由
    api.add_resource(TrackingDataList, '/api/tracking')
    api.add_resource(TrackingDataDetail, '/api/tracking/<int:tracking_id>')
    api.add_resource(QRCodeScan, '/api/tracking/scan')
    api.add_resource(TrackingHistory, '/api/tracking/<int:product_id>/history')
    
    # 质量检查相关路由
    api.add_resource(QualityCheckList, '/api/quality-checks')
    api.add_resource(QualityCheckDetail, '/api/quality-checks/<int:check_id>')
    
    # 供应商相关路由
    api.add_resource(SupplierList, '/api/suppliers')
    api.add_resource(SupplierDetail, '/api/suppliers/<int:supplier_id>')
    
    # 设备相关路由
    api.add_resource(DeviceList, '/api/devices')
    api.add_resource(DeviceDetail, '/api/devices/<int:device_id>')
    
    # 仪表盘相关路由
    api.add_resource(DashboardStats, '/api/dashboard/stats')
    
    # 注册前端页面路由
    app.register_blueprint(web_bp)

# 前端页面路由
@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@web_bp.route('/products')
def products():
    return render_template('products.html')

@web_bp.route('/tracking')
def tracking():
    return render_template('tracking.html')

@web_bp.route('/quality')
def quality():
    return render_template('quality.html')

@web_bp.route('/suppliers')
def suppliers():
    return render_template('suppliers.html')

@web_bp.route('/devices')
def devices():
    return render_template('devices.html')

@web_bp.route('/login')
def login_page():
    return render_template('login.html')

@web_bp.route('/register')
def register_page():
    return render_template('register.html')