import hashlib
import qrcode
import os
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 生成唯一ID
def generate_unique_id(prefix=''):
    """生成唯一ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    unique_str = f"{prefix}_{timestamp}"
    return hashlib.md5(unique_str.encode()).hexdigest()[:12]

# 生成二维码
def generate_qr_code(data, output_path):
    """生成二维码并保存到指定路径"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    img.save(output_path)
    return output_path

# 数据验证
def validate_required_fields(data, required_fields):
    """验证数据中是否包含所有必需的字段"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, missing_fields
    return True, []

# 格式化日期时间
def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间"""
    if isinstance(dt, datetime):
        return dt.strftime(format_str)
    return dt

# 导出数据为Excel
def export_to_excel(data, filename, sheet_name='Sheet1'):
    """将数据导出为Excel文件"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 转换数据为DataFrame
    df = pd.DataFrame(data)
    
    # 保存为Excel文件
    df.to_excel(filename, index=False, sheet_name=sheet_name)
    return filename

# 生成数据可视化图表
def generate_chart(data, chart_type, filename, title='', x_label='', y_label=''):
    """生成数据可视化图表"""
    # 确保输出目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'bar':
        x_data = list(data.keys())
        y_data = list(data.values())
        plt.bar(x_data, y_data)
    elif chart_type == 'pie':
        labels = list(data.keys())
        sizes = list(data.values())
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
    elif chart_type == 'line':
        x_data = list(data.keys())
        y_data = list(data.values())
        plt.plot(x_data, y_data, marker='o')
    
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
    return filename

# 计算年龄（用于产品批次等）
def calculate_age(start_date, end_date=None):
    """计算两个日期之间的天数差"""
    if end_date is None:
        end_date = datetime.utcnow()
    
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    delta = end_date - start_date
    return delta.days

# 生成报告ID
def generate_report_id():
    """生成报告ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d')
    random_part = generate_unique_id()
    return f"REPORT_{timestamp}_{random_part}"

# 记录操作日志（在实际应用中会写入MongoDB）
def log_operation(user_id, operation_type, target_type, target_id, details=None):
    """记录操作日志"""
    log_entry = {
        'user_id': user_id,
        'operation_type': operation_type,
        'target_type': target_type,
        'target_id': target_id,
        'details': details or {},
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # 在实际应用中，这里会将日志写入MongoDB
    # mongo_client.logs.insert_one(log_entry)
    
    print(f"Operation logged: {json.dumps(log_entry, ensure_ascii=False)}")
    return log_entry

# 计算产品质量得分
def calculate_quality_score(check_items):
    """根据检查项计算质量得分"""
    if not check_items:
        return 0
    
    total_score = 0
    item_count = 0
    
    for item in check_items:
        if 'score' in item:
            total_score += item['score']
            item_count += 1
    
    return total_score / item_count if item_count > 0 else 0