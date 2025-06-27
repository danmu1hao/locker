# import requests
# import json

# def test_api():
#     """测试API功能"""
    
#     base_url = 'http://localhost:5000'
    
#     print("=== 测试员工打卡系统API ===\n")
    
#     # 1. 测试根路径
#     print("1. 测试根路径:")
#     try:
#         response = requests.get(f'{base_url}/')
#         print(f"状态码: {response.status_code}")
#         if response.status_code == 200:
#             data = response.json()
#             print(f"API信息: {data['message']}")
#             print(f"版本: {data['version']}")
#             print(f"可用端点: {list(data['endpoints'].keys())}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"❌ 测试失败: {str(e)}")
    
#     # 2. 测试添加用户
#     print("2. 测试添加用户:")
#     try:
#         user_data = {
#             'name': '测试用户',
#             'role': '员工',
#             'card_id': '999999',
#             'card_name': '测试用户卡'
#         }
        
#         response = requests.post(
#             f'{base_url}/api/users/add_user',
#             json=user_data,
#             headers={'Content-Type': 'application/json'}
#         )
        
#         print(f"状态码: {response.status_code}")
#         if response.status_code == 200:
#             result = response.json()
#             print(f"✅ 添加用户成功: {result['message']}")
#             print(f"用户ID: {result['added_user']['id']}")
#             print(f"用户姓名: {result['added_user']['name']}")
#             print(f"用户角色: {result['added_user']['role']}")
#         else:
#             print(f"❌ 添加用户失败: {response.text}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"❌ 测试失败: {str(e)}")
    
#     # 3. 测试卡牌查找
#     print("3. 测试卡牌查找:")
#     try:
#         card_data = {
#             'card_id': '123456',  # 使用数据库中存在的卡牌ID
#             'timestamp': '2024-12-19 08:00:00'
#         }
        
#         response = requests.post(
#             f'{base_url}/api/card/lookup',
#             json=card_data,
#             headers={'Content-Type': 'application/json'}
#         )
        
#         print(f"状态码: {response.status_code}")
#         if response.status_code == 200:
#             result = response.json()
#             print(f"✅ 找到卡牌所有者: {result['message']}")
#             print(f"用户姓名: {result['user_info']['name']}")
#             print(f"用户角色: {result['user_info']['role']}")
#         elif response.status_code == 404:
#             result = response.json()
#             print(f"❌ 未找到卡牌所有者: {result['message']}")
#         else:
#             print(f"❌ 查找失败: {response.text}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"❌ 测试失败: {str(e)}")
    
#     # 4. 测试获取用户列表
#     print("4. 测试获取用户列表:")
#     try:
#         response = requests.get(f'{base_url}/api/users')
#         print(f"状态码: {response.status_code}")
#         if response.status_code == 200:
#             users = response.json()
#             print(f"✅ 成功获取 {len(users)} 个用户")
#             for user in users:
#                 print(f"   - ID: {user['id']}, 姓名: {user['name']}, 角色: {user['role']}")
#         else:
#             print(f"❌ 获取用户失败: {response.text}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"❌ 测试失败: {str(e)}")

# if __name__ == '__main__':
#     test_api() 