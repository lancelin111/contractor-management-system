import os

# 数据库配置
# 请根据实际情况修改数据库密码
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # 请设置你的MySQL密码
    'database': os.getenv('DB_NAME', 'test'),
    'charset': 'utf8mb4',
}

# Flask配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
DEBUG = True
