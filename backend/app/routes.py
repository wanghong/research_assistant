from flask import Response, stream_with_context
from app import app
import time
import random

@app.route('/api')
def index():
    def generate():
        while True:
            # 模拟生成一些数据，这里可以替换为实际业务逻辑获取的数据
            data = random.randint(1, 100)
            # 按照 SSE 格式生成响应数据
            yield f"data:{data}\n\n"
            time.sleep(1)  # 每秒发送一次数据

    return Response(generate(), mimetype='text/event-stream')