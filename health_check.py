import requests
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_health():
    try:
        # 尝试访问应用根路径
        response = requests.get('http://192.168.1.12:5000/', timeout=5)
        logger.info(f"应用健康检查: 状态码 {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"应用健康检查失败: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("开始应用健康检查")
    success = check_health()
    logger.info(f"健康检查{'成功' if success else '失败'}")
