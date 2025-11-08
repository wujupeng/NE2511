from flask import request, jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.product import Product
from src.api.auth_middleware import jwt_required, roles_required

class ProductList(Resource):
    @jwt_required
    def get(self):
        """获取产品列表"""
        try:
            # 获取查询参数
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            product_type = request.args.get('type')
            status = request.args.get('status')
            
            # 构建查询
            query = db_session.query(Product)
            
            if product_type:
                query = query.filter_by(product_type=product_type)
            
            if status:
                query = query.filter_by(status=status)
            
            # 分页
            pagination = query.order_by(Product.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            products = pagination.items
            total = pagination.total
            
            return {
                'products': [product.to_dict() for product in products],
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }, 200
        except Exception as e:
            return {'message': '获取产品列表失败', 'error': str(e)}, 500
    
    @roles_required('admin', 'manager')
    def post(self):
        """创建新产品"""
        try:
            data = request.get_json()
            
            # 验证输入
            if not data or not all(key in data for key in ['product_code', 'product_name', 'product_type', 'manufacturer', 'production_date']):
                return {'message': '缺少必要的产品信息'}, 400
            
            # 检查产品编码是否已存在
            if db_session.query(Product).filter_by(product_code=data['product_code']).first():
                return {'message': '产品编码已存在'}, 400
            
            # 创建新产品
            new_product = Product(**data)
            db_session.add(new_product)
            db_session.commit()
            
            return {'message': '产品创建成功', 'product': new_product.to_dict()}, 201
        except Exception as e:
            db_session.rollback()
            return {'message': '产品创建失败', 'error': str(e)}, 500

class ProductDetail(Resource):
    @jwt_required
    def get(self, product_id):
        """获取产品详情"""
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            return {'message': '产品不存在'}, 404
        
        return {'product': product.to_dict()}, 200
    
    @roles_required('admin', 'manager')
    def put(self, product_id):
        """更新产品信息"""
        product = Product.query.get(product_id)
        if not product:
            return {'message': '产品不存在'}, 404
        
        try:
            data = request.get_json()
            
            # 更新产品信息
            for key, value in data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            db_session.commit()
            return {'message': '产品更新成功', 'product': product.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '产品更新失败', 'error': str(e)}, 500
    
    @roles_required('admin')
    def delete(self, product_id):
        """删除产品"""
        product = db_session.query(Product).filter_by(id=product_id).first()
        if not product:
            return {'message': '产品不存在'}, 404
        
        try:
            db_session.delete(product)
            db_session.commit()
            return {'message': '产品删除成功'}, 200
        except Exception as e:
            db_session.rollback()
            return {'message': '产品删除失败', 'error': str(e)}, 500

class ProductSearch(Resource):
    @jwt_required
    def get(self):
        """搜索产品"""
        try:
            keyword = request.args.get('keyword', '')
            if not keyword:
                return {'message': '搜索关键词不能为空'}, 400
            
            # 搜索产品名称、编码等字段
            products = db_session.query(Product).filter(
                (Product.product_name.contains(keyword)) |
                (Product.product_code.contains(keyword)) |
                (Product.product_type.contains(keyword))
            ).all()
            
            return {
                'products': [product.to_dict() for product in products],
                'total': len(products)
            }, 200
        except Exception as e:
            return {'message': '搜索失败', 'error': str(e)}, 500