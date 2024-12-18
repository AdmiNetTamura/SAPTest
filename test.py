import os 
from flask import Flask, request, jsonify 
from hdbcli import dbapi

app = Flask(__name__)
app.json.ensure_ascii = False
port = int(os.environ.get('PORT', 3000))

@app.route('/')
def ask_llm():
    if'query' in request.args:
        # マージテスト
        # 接続初期化tetete
        conn = dbapi.connect(
            address='82d35572-0195-4281-ab4f-e84eec0dca7c.hana.prod-us10.hanacloud.ondemand.com',
            port=443,
            user='DBADMIN',
            password='Administrator0',
            sslValidateCertificate=False,  # True for HANA Cloud, False for HANA Express.
        )
        # 接続成功時の処理
        print('connected\n')
        cursor = conn.cursor()
        sql_command = "SELECT * FROM DBADMIN.EMPLOYEE;"
        cursor.execute(sql_command)
        rows = cursor.fetchall()
        # 列名の取得
        columns = [desc[0] for desc in cursor.description]
        # データをJSON形式に変換
        employees_data = []
        for row in rows:
            employees_data.append(dict(zip(columns, row)))
        query = request.args['query']
        response = {
            "query":query,
            "sentiment":'successfull',
            "data": employees_data       
        }
        return jsonify(response)
    else:
        return 'faild'
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)
