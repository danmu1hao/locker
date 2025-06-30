#!/usr/bin/env python3
"""
修复数据库问题
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import DB

def fix_database():
    """修复数据库问题"""
    print("=== 修复数据库 ===")
    
    # 1. 重新初始化数据库
    print("1. 重新初始化数据库...")
    DB.init_db()
    print("   数据库表结构已重新创建")
    
    # 2. 插入测试数据
    print("2. 插入测试数据...")
    DB.insert_sample_data()
    print("   测试数据已插入")
    
    # 3. 更新出勤汇总
    print("3. 更新出勤汇总...")
    DB.update_attendance_summary()
    print("   出勤汇总已更新")
    
    # 4. 验证数据
    print("4. 验证数据...")
    try:
        users = DB.get_users()
        print(f"   用户数量: {len(users)}")
        if users:
            print(f"   第一个用户: {users[0]}")
        
        logs = DB.get_access_logs()
        print(f"   打刻记录数量: {len(logs)}")
        if logs:
            print(f"   第一条打刻记录: {logs[0]}")
        
        summary = DB.get_attendance_summary()
        print(f"   出勤汇总数量: {len(summary)}")
        if summary:
            print(f"   第一条出勤汇总: {summary[0]}")
        
        print("   数据验证成功！")
        
    except Exception as e:
        print(f"   数据验证失败: {e}")
        return False
    
    print("=== 数据库修复完成 ===")
    return True

if __name__ == "__main__":
    fix_database() 