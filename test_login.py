import requests
import json

# 测试登录API
try:
    url = 'http://localhost:5001/api/auth/login'
    headers = {'Content-Type': 'application/json'}
    data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    print(f"发送登录请求到: {url}")
    print(f"请求数据: {data}")
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    # 尝试解析JSON响应
    try:
        json_response = response.json()
        print(f"解析后的JSON响应: {json.dumps(json_response, indent=2)}")
        print("\n✅ 登录API返回有效的JSON响应!")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON解析错误: {e}")
        print("这可能是返回HTML而非JSON的问题")
        
    # 检查响应是否包含HTML标签
    if '<html>' in response.text.lower() or '<!doctype' in response.text.lower():
        print("\n⚠️ 警告: 响应中包含HTML内容")

except Exception as e:
    print(f"测试过程中出错: {e}")