import requests
import time
import datetime

from send_mail import send_email


def get_device_status(sim_id: str, token: str):
    url = "https://appapi.lvcchong.com/portDetail?channelMessage=LVCC-WP-PH_2.0.0_Tencent-G9"

    # 请求头（关键是 token，要从 Fiddler 抓到的复制过来）
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/132.0.0.0 Safari/537.36 "
                      "MicroMessenger/7.0.20.1781(0x6700143B) "
                      "NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254101e) XWEB/16389",
        "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJmYmE3ZjNkZGQ3YTRlMmI4NjJjZDIyMGY3NWZhMWI5In0..."
    }

    # 表单参数（POST body）
    data = {
        # 863343061584686 867552065400956
        "simId": "863343061584686",
        "mapType": "2",
        "chargeTypeTag": "0",
        "appEntrance": "2",
        "version": "new"
    }

    try:
        resp = requests.post(url, headers=headers, data=data, timeout=10, verify=False)
        if resp.status_code == 200:
            result = resp.json()
            return result
        else:
            return {"error": f"status_code {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def run_monitor(sim_id, token, interval=300):
    while True:
        result = get_device_status(sim_id, token)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] 查询结果: ")

        if "error" in result:
            print("❌ 出错:", result["error"])
        else:
            try:
                device = result["data"]["device"]
                free_ports = device.get("freePortCount", "未知")
                port_number = device.get("portNumber", 10)
                print(f"设备: {device['name']} | 空闲口: {free_ports} / {device['portNumber']}")
                ports = result["data"]["ports"]
                if free_ports - len(fake_id) == 0:
                    print("暂无可用设备")
                else:
                    msg = ""
                    for i in range(1, len(ports)):
                        if ports[i] == 0 and i not in fake_id:
                            msg += f'{device["name"]} {i} 号充电桩空闲了！快去占位 🚲\n'
                    print(msg)
                    # 示例调用
                    send_email("⚡充电桩提醒", msg)
            except Exception:
                print(result)

        time.sleep(interval)  # 等待 interval 秒，再查询


fake_id = []

if __name__ == "__main__":
    # 替换为你的 simId 和最新 token
    SIM_ID = "867552065400956"
    TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImJmYm..."

    run_monitor(SIM_ID, TOKEN, interval=300)  # 每 5 分钟查一次
