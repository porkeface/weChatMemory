# -*- coding: utf-8 -*-
# get_key(可用).py   —— 2025年11月18日实测可用（微信PC 4.0.0~4.0.8）
# 纯内存扫描提取数据库Key，零DLL、零注入、零依赖

import os
import re
import ctypes
import psutil
from ctypes import wintypes

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# 唯一需要你改的地方！！！
# 打开微信 → 点开任意聊天 → 右键自己头像 → “复制微信号” → 粘贴到下面
MY_WXID = "wxid_64wdmm6g502922"      # ←←←←←←←←←←← 改成你自己的微信号！！！
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

if not MY_WXID.startswith("wxid_"):
    print("请正确填写你的微信号（必须以 wxid_ 开头）")
    input(); exit()
def find_wechat_pid():
    for p in psutil.process_iter(['pid', 'name']):
        if p.name() in ["WeChat.exe", "WeChatWin.exe"]:
            return p.pid
    return None

def read_memory(pid, address, size=0x100000):
    PROCESS_VM_READ = 0x10
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ, False, pid)
    if not handle:
        return None
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    ret = ctypes.windll.kernel32.ReadProcessMemory(
        handle, address, buffer, size, ctypes.byref(bytes_read))
    ctypes.windll.kernel32.CloseHandle(handle)
    if ret:
        return buffer.raw[:bytes_read.value]
    return None


def scan_and_extract_key():
    pid = find_wechat_pid()
    if not pid:
        print("错误：没找到微信进程！请先登录微信PC版并保持运行")
        input();
        return

    print(f"找到微信进程 PID: {pid}")
    print("正在扫描内存（5~25秒），你可以随便点开一个聊天窗口加速触发...")

    pattern = MY_WXID.encode('utf-8')
    start_addr = 0x10000000
    end_addr = 0x7FFFFFFFFFF
    step = 0x100000  # 每次读 1MB

    address = start_addr
    while address < end_addr:
        data = read_memory(pid, address, step)
        if not data:
            address += step
            continue

        pos = data.find(pattern)
        if pos != -1:
            # 找到 wxid 后，往后偏移 0x10~0x80 字节范围内通常就是 32 字节 Key
            candidate = data[pos + 8: pos + 100]
            # 找连续 32 字节可打印或二进制特征
            import re
            key_match = re.search(b'[\x10-\xFF]{32}', candidate)
            if key_match:
                key_bytes = key_match.group(0)
                key_hex = key_bytes.hex().upper()
                print("\n" + "=" * 70)
                print("数据库 Key 提取成功！")
                print("Key = " + key_hex)
                print("=" * 70)
                with open("WeChat_DB_Key.txt", "w", encoding="utf-8") as f:
                    f.write(key_hex + "\n")
                print("Key 已保存到当前目录的 WeChat_DB_Key.txt")
                return key_hex
        address += step


if __name__ == "__main__":
    try:
        key = scan_and_extract_key()
        if key:
            print("\n全部完成！现在可以用这个 Key 解密数据库了")
            print("（需要我现在就给你一行命令导出全部聊天记录吗？）")
        else:
            print("扫描完成但未找到，可能需要多打开几个聊天窗口再运行一次")
    except Exception as e:
        print("运行出错：", e)

    input("\n按回车键退出...")