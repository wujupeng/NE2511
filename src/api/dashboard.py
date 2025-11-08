from flask import jsonify
from flask_restful import Resource
from src.models.database import db_session
from src.models.product import Product
from src.models.tracking import TrackingData, QualityCheck
from src.models.device import Device
from src.api.auth_middleware import jwt_required
from datetime import datetime, timedelta

class DashboardStats(Resource):
    @jwt_required
    def get(self):
        """获取仪表盘统计数据"""
        try:
            # 获取时间范围（默认过去7天）
            days = 7
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # 产品统计
            total_products = db_session.query(Product).count()
            new_products = db_session.query(Product).filter(Product.created_at >= start_date).count()
            
            # 按状态统计产品
            products_by_status = {}
            statuses = ['produced', 'shipped', 'sold', 'recalled']
            for status in statuses:
                count = db_session.query(Product).filter_by(status=status).count()
                products_by_status[status] = count
            
            # 质量检查统计
            total_quality_checks = db_session.query(QualityCheck).count()
            recent_checks = db_session.query(QualityCheck).filter(QualityCheck.check_time >= start_date).count()
            
            # 合格/不合格统计
            passed_checks = db_session.query(QualityCheck).filter_by(pass_status=True).count()
            failed_checks = db_session.query(QualityCheck).filter_by(pass_status=False).count()
            
            # 设备统计
            total_devices = db_session.query(Device).count()
            active_devices = db_session.query(Device).filter_by(status='active').count()
            maintenance_devices = db_session.query(Device).filter_by(status='maintenance').count()
            
            # 追踪数据统计
            total_tracking = db_session.query(TrackingData).count()
            
            # 近期活动（过去7天的质量检查记录）
            recent_activities = []
            recent_checks_data = db_session.query(QualityCheck).filter(
                QualityCheck.check_time >= start_date
            ).order_by(QualityCheck.check_time.desc()).limit(10).all()
            
            for check in recent_checks_data:
                product = db_session.query(Product).filter_by(id=check.product_id).first()
                recent_activities.append({
                    'type': 'quality_check',
                    'product_name': product.product_name if product else '未知产品',
                    'product_code': product.product_code if product else 'N/A',
                    'check_type': check.check_type,
                    'result': '合格' if check.pass_status else '不合格',
                    'time': check.check_time.isoformat()
                })
            
            # 生成统计数据
            stats = {
                'overview': {
                    'total_products': total_products,
                    'new_products_7d': new_products,
                    'total_quality_checks': total_quality_checks,
                    'total_devices': total_devices,
                    'total_tracking': total_tracking
                },
                'products': {
                    'by_status': products_by_status
                },
                'quality': {
                    'passed': passed_checks,
                    'failed': failed_checks,
                    'recent_checks_7d': recent_checks,
                    'pass_rate': passed_checks / total_quality_checks * 100 if total_quality_checks > 0 else 0
                },
                'devices': {
                    'active': active_devices,
                    'maintenance': maintenance_devices,
                    'inactive': total_devices - active_devices - maintenance_devices
                },
                'recent_activities': recent_activities
            }
            
            return {'stats': stats}, 200
            
        except Exception as e:
            return {'message': '获取统计数据失败', 'error': str(e)}, 500