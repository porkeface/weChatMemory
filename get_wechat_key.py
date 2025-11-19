import ctypes
import psutil
import re
import struct

PROCESS_ALL_ACCESS = 0x1F0FFF
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40  # 增加对可执行内存的支持
MEM_COMMIT = 0x1000


# 读取进程内存
def read_process_memory(hProcess, address, size):
    data = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t()
    ctypes.windll.kernel32.ReadProcessMemory(hProcess, ctypes.c_void_p(address), data, size, ctypes.byref(bytesRead))
    return data.raw


# 判断是否像32字节AES key
def looks_like_key(chunk):
    if len(chunk) != 32:
        return False

    # 至少有 10 个以上非零字节
    if sum(1 for b in chunk if b != 0) < 10:
        return False

    # 不全是同一个值
    if len(set(chunk)) < 4:
        return False

    return True


def find_wechat_key():
    # 找 WeChat.exe 进程
    pid = None
    for p in psutil.process_iter(['name', 'pid']):
        if p.info['name'] and "WeChat.exe" in p.info['name']:
            pid = p.info['pid']
            break

    if not pid:
        print("没有找到微信进程，请先登录微信再运行！")
        return

    print(f"[+] 检测到微信进程 PID = {pid}")

    # 打开进程
    hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    # 获取系统内存信息
    SYSTEM_INFO = ctypes.create_string_buffer(48)
    ctypes.windll.kernel32.GetSystemInfo(SYSTEM_INFO)
    min_addr = struct.unpack("P", SYSTEM_INFO.raw[:ctypes.sizeof(ctypes.c_void_p)])[0]
    max_addr = struct.unpack("P", SYSTEM_INFO.raw[ctypes.sizeof(ctypes.c_void_p):2 * ctypes.sizeof(ctypes.c_void_p)])[0]

    print(f"[+] 开始扫描内存范围：0x{min_addr:X} - 0x{max_addr:X}")

    address = min_addr
    found_keys = []

    while address < max_addr:
        mem_info = ctypes.create_string_buffer(48)
        result = ctypes.windll.kernel32.VirtualQueryEx(hProcess, ctypes.c_void_p(address), mem_info, ctypes.sizeof(mem_info))

        if result == 0:
            print(f"[!] VirtualQueryEx 失败，地址：0x{address:X}")
            address += 0x1000  # 跳过一页内存
            continue

        baseAddress = struct.unpack("P", mem_info.raw[:ctypes.sizeof(ctypes.c_void_p)])[0]
        regionSize = struct.unpack("P", mem_info.raw[ctypes.sizeof(ctypes.c_void_p):2 * ctypes.sizeof(ctypes.c_void_p)])[0]
        state = struct.unpack("I", mem_info.raw[16:20])[0]
        protect = struct.unpack("I", mem_info.raw[24:28])[0]

        # 查找可读的内存
        if state == MEM_COMMIT and (protect & PAGE_READWRITE or protect & PAGE_EXECUTE_READWRITE):
            try:
                data = read_process_memory(hProcess, baseAddress, regionSize)

                # 搜索 32 字节片段
                for i in range(len(data) - 32):
                    chunk = data[i:i + 32]

                    if looks_like_key(chunk):
                        key_hex = chunk.hex().upper()
                        if key_hex not in found_keys:
                            found_keys.append(key_hex)
                            print(f"[可能的 KEY] {key_hex}")

            except Exception as e:
                print(f"[!] 内存读取失败：0x{address:X}，错误：{e}")

        address += regionSize

    print("\n扫描结束。")
    return found_keys


if __name__ == "__main__":
    keys = find_wechat_key()
    print("\n可能的 KEY 列表：")
    for k in keys:
        print(k)

