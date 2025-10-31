from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from datetime import date
import json

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置
import os
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  # 请设置环境变量或修改此处
    'database': os.getenv('DB_NAME', 'test'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 自定义JSON编码器，处理日期类型
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

app.json_encoder = DateEncoder

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)

@app.route('/api/contractors', methods=['GET'])
def get_contractors():
    """获取外包人员列表（支持搜索和过滤）"""
    try:
        # 获取查询参数
        keyword = request.args.get('keyword', '')
        department = request.args.get('department', '')
        status = request.args.get('status', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        conn = get_db_connection()
        cursor = conn.cursor()

        # 构建查询条件
        where_clauses = []
        params = []

        if keyword:
            where_clauses.append("(name LIKE %s OR position LIKE %s OR department LIKE %s)")
            keyword_param = f'%{keyword}%'
            params.extend([keyword_param, keyword_param, keyword_param])

        if department:
            where_clauses.append("department = %s")
            params.append(department)

        if status:
            where_clauses.append("status = %s")
            params.append(status)

        where_sql = ' AND '.join(where_clauses) if where_clauses else '1=1'

        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM contractors WHERE {where_sql}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']

        # 查询数据
        offset = (page - 1) * page_size
        query_sql = f"""
            SELECT id, name, gender, birth_date, age, photo_url, education, degree,
                   university, major, join_date, employment_type, band, department,
                   position, status, phone, email
            FROM contractors
            WHERE {where_sql}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cursor.execute(query_sql, params)
        contractors = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'list': contractors,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/contractors/<int:contractor_id>', methods=['GET'])
def get_contractor_detail(contractor_id):
    """获取外包人员详细信息"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 查询基本信息
        cursor.execute("""
            SELECT * FROM contractors WHERE id = %s
        """, (contractor_id,))
        contractor = cursor.fetchone()

        if not contractor:
            return jsonify({'code': 404, 'message': '人员不存在'}), 404

        # 查询工作经历
        cursor.execute("""
            SELECT * FROM work_experience WHERE contractor_id = %s ORDER BY start_date DESC
        """, (contractor_id,))
        work_experience = cursor.fetchall()

        # 查询项目经历
        cursor.execute("""
            SELECT * FROM project_experience WHERE contractor_id = %s ORDER BY start_date DESC
        """, (contractor_id,))
        project_experience = cursor.fetchall()

        # 查询技能标签
        cursor.execute("""
            SELECT * FROM skills WHERE contractor_id = %s
        """, (contractor_id,))
        skills = cursor.fetchall()

        # 查询培训记录
        cursor.execute("""
            SELECT * FROM training_records WHERE contractor_id = %s ORDER BY training_date DESC
        """, (contractor_id,))
        training_records = cursor.fetchall()

        # 查询绩效评估
        cursor.execute("""
            SELECT * FROM performance_reviews WHERE contractor_id = %s ORDER BY review_date DESC
        """, (contractor_id,))
        performance_reviews = cursor.fetchall()

        # 查询合同信息
        cursor.execute("""
            SELECT * FROM contracts WHERE contractor_id = %s ORDER BY start_date DESC
        """, (contractor_id,))
        contracts = cursor.fetchall()

        cursor.close()
        conn.close()

        # 组装返回数据
        result = {
            'basic_info': contractor,
            'work_experience': work_experience,
            'project_experience': project_experience,
            'skills': skills,
            'training_records': training_records,
            'performance_reviews': performance_reviews,
            'contracts': contracts
        }

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/departments', methods=['GET'])
def get_departments():
    """获取所有部门列表"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT department FROM contractors WHERE department IS NOT NULL
        """)
        departments = [row['department'] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': departments
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 总人数
        cursor.execute("SELECT COUNT(*) as total FROM contractors")
        total = cursor.fetchone()['total']

        # 在职人数
        cursor.execute("SELECT COUNT(*) as total FROM contractors WHERE status = '在职'")
        active = cursor.fetchone()['total']

        # 按部门统计
        cursor.execute("""
            SELECT department, COUNT(*) as count
            FROM contractors
            WHERE department IS NOT NULL
            GROUP BY department
        """)
        by_department = cursor.fetchall()

        # 按职级统计
        cursor.execute("""
            SELECT band, COUNT(*) as count
            FROM contractors
            WHERE band IS NOT NULL
            GROUP BY band
        """)
        by_band = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'total': total,
                'active': active,
                'by_department': by_department,
                'by_band': by_band
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': 'Contractor Management System API is running'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
