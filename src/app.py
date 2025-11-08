from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_key')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt_dev_secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 启用CORS
CORS(app)

# 初始化JWT管理器
jwt = JWTManager(app)

# 数据库配置
from src.models.database import init_db, db_session
init_db()

# 注册API路由
from flask_restful import Api
from src.api.auth import Register, Login, Logout
from src.api.products import ProductList, ProductDetail, ProductSearch
from src.api.tracking import TrackingDataList, TrackingDataDetail, QRCodeScan, TrackingHistory
from src.api.quality import QualityCheckList, QualityCheckDetail
from src.api.suppliers import SupplierList, SupplierDetail
from src.api.devices import DeviceList, DeviceDetail
from src.api.dashboard import DashboardStats
from src.api.auth_middleware import jwt_required, roles_required

# 初始化API
api = Api(app)

# 注册API资源
api.add_resource(Register, '/api/auth/register')
api.add_resource(Login, '/api/auth/login')
api.add_resource(Logout, '/api/auth/logout')
api.add_resource(ProductList, '/api/products')
api.add_resource(ProductDetail, '/api/products/<int:product_id>')
api.add_resource(ProductSearch, '/api/products/search')
api.add_resource(TrackingDataList, '/api/tracking')
api.add_resource(TrackingDataDetail, '/api/tracking/<int:tracking_id>')
api.add_resource(QRCodeScan, '/api/tracking/qrcode')
api.add_resource(TrackingHistory, '/api/tracking/history')
api.add_resource(QualityCheckList, '/api/quality')
api.add_resource(QualityCheckDetail, '/api/quality/<int:check_id>')
api.add_resource(SupplierList, '/api/suppliers')
api.add_resource(SupplierDetail, '/api/suppliers/<int:supplier_id>')
api.add_resource(DeviceList, '/api/devices')
api.add_resource(DeviceDetail, '/api/devices/<int:device_id>')
api.add_resource(DashboardStats, '/api/dashboard/stats')

# 前端页面路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/products')
def products_page():
    return render_template('products.html')

@app.route('/tracking')
def tracking_page():
    return render_template('tracking.html')

@app.route('/quality')
def quality_page():
    return render_template('quality.html')

@app.route('/suppliers')
def suppliers_page():
    return render_template('suppliers.html')

@app.route('/devices')
def devices_page():
    return render_template('devices.html')

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': '资源未找到', 'status': 404}), 404
    return render_template('error.html', error_code=404, error_message='页面未找到'), 404

@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify({'error': '服务器内部错误', 'status': 500}), 500
    return render_template('error.html', error_code=500, error_message='服务器内部错误'), 500

# JWT错误处理
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Token过期',
        'status_code': 401
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': '无效的Token',
        'status_code': 401
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': '缺少认证Token',
        'status_code': 401
    }), 401

# 应用上下文处理器
@app.context_processor
def inject_user():
    # 这里可以注入全局模板变量
    return {}

# 应用启动事件
@app.before_request
def before_request():
    # 请求前的处理
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    # 关闭数据库会话
    db_session.close()

# 启动应用
if __name__ == '__main__':
    # 确保静态文件目录存在
    os.makedirs('src/static/css', exist_ok=True)
    os.makedirs('src/static/js', exist_ok=True)
    os.makedirs('src/templates', exist_ok=True)
    
    # 启动开发服务器
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'True') == 'True')