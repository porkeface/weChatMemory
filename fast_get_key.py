from wechat_key_extractor import WeChatKey
import time

print("正在启动（3～8秒出Key）...")
key = WeChatKey().get()          # 这一行就是全部魔法
print("\n" + "="*70)
print("数据库 Key =", key)
print("="*70)
with open("WeChat_DB_Key.txt","w") as f: f.write(key)
print("已保存到 WeChat_DB_Key.txt")
input("按回车退出")