# -*- coding: utf-8 -*-
# get_key_2025_fixed.py  —— 完美解决 OverflowError
# 适用于 Python 3.9/3.10/3.11 + 微信PC 4.0.x

import os
import re
import ctypes
import psutil
from ctypes import wintypes

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# 唯一需要改的地方！！！
MY_WXID = "wxid_64wdmm6g502922"  # ←←←←←←←←←←← 改成你自己的微信号
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

if not MY_WXID.startswith("wxid_"):
    print("请正确填写微信号（必须以 wxid_ 开头）")
    input();
    exit()


def find_wechat_pid():
    for p in psutil.process_iter(['pid', 'name']):
        if p.name() in ["WeChat.exe", "WeChatWin.exe"]:
            return p.pid
    return None


def read_memory(pid, address, size=0x100000):
    PROCESS_VM_READ = 0x0010
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ, False, pid)
    if not handle:
        return None
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    # 关键修复：把 address 强制转成 c_void_p
    ret = ctypes.windll.kernel32.ReadProcessMemory(
        handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read))
    ctypes.windll.kernel32.CloseHandle(handle)
    if ret:
        return buffer.raw[:bytes_read.value]
    return None


def scan_and_extract_key():
    pid = find_wechat_pid()
    if not pid:
        print("错误：没找到微信进程！请先登录微信PC版")
        input();
        return None

    print(f"找到微信进程 PID: {pid}")
    print("正在扫描内存（5~20秒），可以随便点开几个聊天窗口加速触发...")

    pattern = MY_WXID.encode('utf-8')
    start_addr = 0x0000000100000000  # 64位进程常用起始范围
    end_addr = 0x00007FFFFFF00000  # 安全上限，避免Overflow
    step = 0x100000  # 每次读1MB

    address = start_addr
    while address < end_addr:
        data = read_memory(pid, address, step)
        if data:
            pos = data.find(pattern)
            if pos != -1:
                # wxid 后面 0x10~0xA0 字节范围内找 32 字节高熵数据
                candidate = data[pos:pos + 0x200]
                import binascii
                # 找熵最高的 32 字节连续块（微信Key特征）
                best_entropy = 0
                best_key = None
                for i in range(len(candidate) - 32):
                    block = candidate[i:i + 32]
                    # 简单熵计算
                    entropy = len(set(block)) / 32.0
                    if entropy > best_entropy and 0x20 <= min(block) <= max(block) <= 0xFF:
                        best_entropy = entropy
                        best_key = block.hex().upper()
                if best_key and best_entropy > 0.8:
                    print("\n" + "=" * 80)
                    print("数据库 Key 提取成功！")
                    print("Key = " + best_key)
                    print("=" * 80)
                    with open("WeChat_DB_Key.txt", "w") as f:
                        f.write(best_key)
                    print("Key 已保存到 WeChat_DB_Key.txt")
                    return best_key
        address += step
    return None


if __name__ == "__main__":
    try:
        key = scan_and_extract_key()
        if key:
            print("\n完成！你现在可以用这个 Key 解密数据库了")
        else:
            print("本次未扫描到Key，多打开几个聊天窗口（尤其是老聊天）再运行一次")
    except Exception as e:
        print("运行出错：", e)
        import traceback

        traceback.print_exc()

    input("\n按回车退出...")