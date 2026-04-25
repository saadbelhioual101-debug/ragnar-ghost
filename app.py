import requests
import os
import psutil
import sys
import jwt
import pickle
import json
import binascii
import time
import urllib3
import base64
import datetime
import re
import socket
import threading
import asyncio
import random
import signal
import atexit
import errno
import select
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify
from google.protobuf.timestamp_pb2 import Timestamp
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============ إعدادات التشفير والبروتوكول ============

# دوال مساعدة للتشفير (يجب إضافة دوال التشفير الفعلية هنا)
def encrypt_api(data):
    """دالة تشفير مؤقتة - استبدلها بدالتك الفعلية"""
    return data

def decrypt_api(data):
    """دالة فك تشفير مؤقتة - استبدلها بدالتك الفعلية"""
    return data

def encrypt_packet(data, key, iv):
    """تشفير الباكيت"""
    return data

def DeCode_PackEt(hex_data):
    """فك تشفير الباكيت"""
    return json.dumps({"test": "data"})

def get_available_room(hex_data):
    """معالجة بيانات الروم"""
    return json.dumps({"32": {"data": "192.168.1.1:8080"}, "14": {"data": "192.168.1.2:8081"}})

def GenJoinSquadsPacket(team_code, key, iv):
    """إنشاء باكيت الانضمام للفريق"""
    return b"test_packet"

def ExiT(code, key, iv):
    """باكيت الخروج"""
    return b"exit_packet"

def ghost_pakcet(idT, name, sq, key, iv):
    """باكيت الشبح"""
    return b"ghost_packet"

def get_packet2(key, iv):
    """باكيت إضافي"""
    return b"packet2"

# البايلود الأساسي
Payload1A13 = "0a" * 100  # بايلود تجريبي - استبدل بالبايلود الفعلي
FreeFireVersion = "1.105.1"
MajorLoginRegionMena = "https://loginbp.common.ggbluefox.com/MajorLogin"
GetLoginDataRegionMena = "https://clientbp.common.ggbluefox.com/GetLoginData"

# ============ كلاس معالجة الرسائل ============

class MajorLoginRes:
    """كلاس مؤقت لمعالجة رسائل الدخول"""
    def ParseFromString(self, data):
        self.kts = 1234567890
        self.ak = b"test_key"
        self.aiv = b"test_iv"
        self.token = "test_token"

class MyMessage:
    """كلاس مؤقت للرسائل"""
    pass

# ============ إعدادات التطبيق ============

app = Flask(__name__)
clients = {}
shutting_down = False
restarting_now = False
client_lock = threading.Lock()
restart_timer = None

shared_0500_info = {
    'got': False,
    'idT': None,
    'squad': None,
    'AutH': None
}

MASTER_ACCOUNT_ID = '4248103380'
RESTART_INTERVAL = 600  # 10 دقائق بالثواني (10 * 60 = 600)

# ============ كلاس الاتصال الرئيسي ============

class TcpBotConnectMain:
    def __init__(self, account_id, password):
        self.account_id = account_id
        self.password = password
        self.key = None
        self.iv = None
        self.socket_client = None
        self.clientsocket = None
        self.running = False
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        self.AutH = None
        self.DaTa2 = None
        self.thread = None
        self.restarting = False
    
    def run(self):
        if shutting_down or restarting_now:
            return
            
        with client_lock:
            if self.restarting:
                return
            self.restarting = True
            
        self.running = True
        self.connection_attempts = 0
        
        try:
            while self.running and not shutting_down and not restarting_now and self.connection_attempts < self.max_connection_attempts:
                try:
                    self.connection_attempts += 1
                    print(f"[{self.account_id}] محاولة الاتصال {self.connection_attempts}/{self.max_connection_attempts}")
                    self.get_tok()
                    break
                except Exception as e:
                    print(f"[{self.account_id}] خطأ في التشغيل: {e}")
                    if self.connection_attempts >= self.max_connection_attempts:
                        print(f"[{self.account_id}] تم الوصول للحد الأقصى للمحاولات")
                        break
                    time.sleep(5)
        finally:
            with client_lock:
                self.restarting = False
    
    def stop(self):
        self.running = False
        try:
            if self.clientsocket:
                self.clientsocket.close()
        except:
            pass
        try:
            if self.socket_client:
                self.socket_client.close()
        except:
            pass
        print(f"[{self.account_id}] تم إيقاف العميل")
    
    def is_socket_connected(self, sock):
        try:
            if sock is None:
                return False
            readable, writable, exceptional = select.select([sock], [sock], [sock], 0.1)
            if sock in writable:
                return True
            if sock in exceptional:
                return False
            return True
        except:
            return False
    
    def parse_my_message(self, serialized_data):
        MajorLogRes_instance = MajorLoginRes()
        MajorLogRes_instance.ParseFromString(serialized_data)
        timestamp = MajorLogRes_instance.kts
        key = MajorLogRes_instance.ak
        iv = MajorLogRes_instance.aiv
        BASE64_TOKEN = MajorLogRes_instance.token
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp, key, iv, BASE64_TOKEN
    
    def dec_to_hex(self, ask):
        ask_result = hex(ask)
        final_result = str(ask_result)[2:]
        if len(final_result) == 1:
            final_result = "0" + final_result
        return final_result
    
    def guest_token(self, uid, password):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 10;en;EN;)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
        }
        data = {
            "uid": f"{uid}",
            "password": f"{password}",
            "response_type": "token",
            "client_type": "2",
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_id": "100067",
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response_data = response.json()
            
            if 'access_token' not in response_data or 'open_id' not in response_data:
                print(f"[{self.account_id}] فشل في الحصول على التوكن")
                return False
            
            NEW_ACCESS_TOKEN = response_data['access_token']
            NEW_OPEN_ID = response_data['open_id']
            
            OLD_ACCESS_TOKEN = "c69ae208fad72738b674b2847b50a3a1dfa25d1a19fae745fc76ac4a0e414c94"
            OLD_OPEN_ID = "4306245793de86da425a52caadf21eed"
            
            time.sleep(0.2)
            result = self.TOKEN_MAKER(OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid)
            return result
            
        except Exception as e:
            print(f"[{self.account_id}] خطأ في guest_token: {e}")
            return False
    
    def TOKEN_MAKER(self, OLD_ACCESS_TOKEN, NEW_ACCESS_TOKEN, OLD_OPEN_ID, NEW_OPEN_ID, uid):
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': FreeFireVersion,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.common.ggbluefox.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        
        try:
            data = bytes.fromhex(Payload1A13)
            data = data.replace(OLD_OPEN_ID.encode(), NEW_OPEN_ID.encode())
            data = data.replace(OLD_ACCESS_TOKEN.encode(), NEW_ACCESS_TOKEN.encode())
            hex_data = data.hex()
            encrypted_data = encrypt_api(hex_data)
            Final_Payload = bytes.fromhex(encrypted_data)
            
            RESPONSE = requests.post(MajorLoginRegionMena, headers=headers, data=Final_Payload, verify=False, timeout=30)
            
            if RESPONSE.status_code == 200 and len(RESPONSE.content) >= 10:
                combined_timestamp, key, iv, BASE64_TOKEN = self.parse_my_message(RESPONSE.content)
                whisper_ip, whisper_port, online_ip, online_port = self.GET_PAYLOAD_BY_DATA(BASE64_TOKEN, NEW_ACCESS_TOKEN, 1)
                self.key = key
                self.iv = iv
                print(f"[{self.account_id}] تم الحصول على المفاتيح")
                return (BASE64_TOKEN, key, iv, combined_timestamp, whisper_ip, whisper_port, online_ip, online_port)
            else:
                return False
                
        except Exception as e:
            print(f"[{self.account_id}] خطأ في TOKEN_MAKER: {e}")
            return False
    
    def GET_PAYLOAD_BY_DATA(self, JWT_TOKEN, NEW_ACCESS_TOKEN, date):
        try:
            token_payload_base64 = JWT_TOKEN.split('.')[1]
            token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
            decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
            decoded_payload = json.loads(decoded_payload)
            NEW_EXTERNAL_ID = decoded_payload['external_id']
            SIGNATURE_MD5 = decoded_payload['signature_md5']
            now = datetime.now()
            now = str(now)[:len(str(now))-7]
            formatted_time = date
            
            payload = bytes.fromhex(Payload1A13)
            payload = payload.replace(b"2025-07-30 11:02:51", str(now).encode())
            payload = payload.replace(b"c69ae208fad72738b674b2847b50a3a1dfa25d1a19fae745fc76ac4a0e414c94", NEW_ACCESS_TOKEN.encode("UTF-8"))
            payload = payload.replace(b"4306245793de86da425a52caadf21eed", NEW_EXTERNAL_ID.encode("UTF-8"))
            payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", SIGNATURE_MD5.encode("UTF-8"))
            PAYLOAD = payload.hex()
            PAYLOAD = encrypt_api(PAYLOAD)
            PAYLOAD = bytes.fromhex(PAYLOAD)
            whisper_ip, whisper_port, online_ip, online_port = self.GET_LOGIN_DATA(JWT_TOKEN, PAYLOAD)
            return whisper_ip, whisper_port, online_ip, online_port
            
        except Exception as e:
            print(f"[{self.account_id}] خطأ في GET_PAYLOAD_BY_DATA: {e}")
            return None, None, None, None
    
    def GET_LOGIN_DATA(self, JWT_TOKEN, PAYLOAD):
        url = GetLoginDataRegionMena
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JWT_TOKEN}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': FreeFireVersion,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, data=PAYLOAD, verify=False, timeout=30)
                response.raise_for_status()
                x = response.content.hex()
                json_result = get_available_room(x)
                parsed_data = json.loads(json_result)
                whisper_address = parsed_data['32']['data']
                online_address = parsed_data['14']['data']
                online_ip = online_address[:len(online_address) - 6]
                whisper_ip = whisper_address[:len(whisper_address) - 6]
                online_port = int(online_address[len(online_address) - 5:])
                whisper_port = int(whisper_address[len(whisper_address) - 5:])
                return whisper_ip, whisper_port, online_ip, online_port
            except Exception as e:
                print(f"[{self.account_id}] محاولة {attempt + 1} فشلت: {e}")
                time.sleep(2)
        
        return None, None, None, None
    
    def sockf1(self, tok, online_ip, online_port, packet, key, iv):
        while self.running and not shutting_down and not restarting_now:
            try:
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_client.settimeout(30)
                
                print(f"[{self.account_id}] الاتصال بـ {online_ip}:{online_port}...")
                self.socket_client.connect((online_ip, int(online_port)))
                self.socket_client.send(bytes.fromhex(tok))
                
                while self.running and not shutting_down and not restarting_now:
                    try:
                        readable, _, _ = select.select([self.socket_client], [], [], 1.0)
                        if self.socket_client in readable:
                            self.DaTa2 = self.socket_client.recv(99999)
                            if not self.DaTa2:
                                break
                            
                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                try:
                                    self.packet = json.loads(DeCode_PackEt(f'08{self.DaTa2.hex().split("08", 1)[1]}'))
                                    self.AutH = self.packet['5']['data']['7']['data']
                                    
                                    if self.account_id == MASTER_ACCOUNT_ID:
                                        shared_0500_info['got'] = True
                                        shared_0500_info['idT'] = self.packet['5']['data']['1']['data']
                                        shared_0500_info['squad'] = self.packet['5']['data']['31']['data']
                                        shared_0500_info['AutH'] = self.AutH
                                        print(f"[{self.account_id}] تم حفظ معلومات 0500")
                                    
                                    elif shared_0500_info['got']:
                                        idT = shared_0500_info['idT']
                                        sq = shared_0500_info['squad']
                                        for _ in range(3):
                                            if self.is_socket_connected(self.socket_client):
                                                self.socket_client.send(GenJoinSquadsPacket(idT, key, iv))
                                                time.sleep(0.5)
                                                self.socket_client.send(ExiT('000000', key, iv))
                                                time.sleep(0.1)
                                                self.socket_client.send(ghost_pakcet(idT, "Ghost", sq, key, iv))
                                                time.sleep(0.5)
                                                
                                except Exception as parse_err:
                                    print(f"[{self.account_id}] خطأ في معالجة 0500: {parse_err}")
                                    
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f"[{self.account_id}] خطأ في socket: {e}")
                        break
                        
            except Exception as e:
                print(f"[{self.account_id}] خطأ في الاتصال: {e}")
                
            finally:
                try:
                    if self.socket_client:
                        self.socket_client.close()
                except:
                    pass
            
            if self.running and not shutting_down and not restarting_now:
                time.sleep(5)
    
    def connect(self, tok, packet, key, iv, whisper_ip, whisper_port, online_ip, online_port):
        while self.running and not shutting_down and not restarting_now:
            try:
                self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientsocket.settimeout(30)
                print(f"[{self.account_id}] الاتصال بـ whisper {whisper_ip}:{whisper_port}...")
                self.clientsocket.connect((whisper_ip, int(whisper_port)))
                self.clientsocket.send(bytes.fromhex(tok))
                self.data = self.clientsocket.recv(1024)
                self.clientsocket.send(get_packet2(self.key, self.iv))
                
                socket_thread = threading.Thread(
                    target=self.sockf1,
                    args=(tok, online_ip, online_port, "anything", key, iv),
                    daemon=True
                )
                socket_thread.start()
                
                while self.running and not shutting_down and not restarting_now:
                    try:
                        dataS = self.clientsocket.recv(1024)
                        if not dataS:
                            break
                    except socket.timeout:
                        continue
                    except Exception:
                        break
                        
            except Exception as e:
                print(f"[{self.account_id}] خطأ في connect whisper: {e}")
                
            finally:
                if self.clientsocket:
                    try:
                        self.clientsocket.close()
                    except:
                        pass
            
            if self.running and not shutting_down and not restarting_now:
                time.sleep(5)
    
    def get_tok(self):
        token_data = self.guest_token(self.account_id, self.password)
        if not token_data:
            print(f"[{self.account_id}] فشل في الحصول على التوكن")
            return
        
        token, key, iv, Timestamp, whisper_ip, whisper_port, online_ip, online_port = token_data
        print(f"[{self.account_id}] Whisper: {whisper_ip}:{whisper_port}")
        
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            account_id = decoded.get('account_id')
            encoded_acc = hex(account_id)[2:]
            hex_value = self.dec_to_hex(Timestamp)
            time_hex = hex_value
            BASE64_TOKEN_ = token.encode().hex()
        except Exception as e:
            print(f"[{self.account_id}] خطأ في معالجة التوكن: {e}")
            return
        
        try:
            head = hex(len(encrypt_packet(BASE64_TOKEN_, key, iv)) // 2)[2:]
            length = len(encoded_acc)
            zeros = '00000000'
            if length == 9:
                zeros = '0000000'
            elif length == 8:
                zeros = '00000000'
            elif length == 10:
                zeros = '000000'
            elif length == 7:
                zeros = '000000000'
            
            head = f'0115{zeros}{encoded_acc}{time_hex}00000{head}'
            final_token = head + encrypt_packet(BASE64_TOKEN_, key, iv)
        except Exception as e:
            print(f"[{self.account_id}] خطأ في إنشاء التوكن النهائي: {e}")
            return
        
        self.connect(final_token, 'anything', key, iv, whisper_ip, whisper_port, online_ip, online_port)
    
    def execute_command(self, command, *args):
        global shared_0500_info
        
        if '/AlliFF' in command[:7]:
            try:
                team_code = args[0] if len(args) > 0 else None
                account_name = args[1] if len(args) > 1 else f"Ghost_{self.account_id}"
                
                if not team_code:
                    return "لا يوجد كود فريق"
                
                if self.account_id == MASTER_ACCOUNT_ID:
                    shared_0500_info['got'] = False
                    shared_0500_info['idT'] = None
                    shared_0500_info['squad'] = None
                    
                    got_0500 = False
                    attempt_counter = 0
                    max_attempts = 3
                    
                    while not got_0500 and attempt_counter < max_attempts and not restarting_now:
                        attempt_counter += 1
                        print(f"[{self.account_id}] محاولة {attempt_counter}/{max_attempts}...")
                        
                        if self.is_socket_connected(self.socket_client):
                            self.socket_client.send(GenJoinSquadsPacket(team_code, self.key, self.iv))
                            time.sleep(0.5)
                            self.socket_client.send(ExiT('000000', self.key, self.iv))
                            time.sleep(0.1)
                            
                            if shared_0500_info['got']:
                                idT = shared_0500_info['idT']
                                sq = shared_0500_info['squad']
                                
                                if self.is_socket_connected(self.socket_client):
                                    self.socket_client.send(ExiT('000000', self.key, self.iv))
                                    time.sleep(0.2)
                                    for _ in range(2):
                                        self.socket_client.send(ghost_pakcet(idT, account_name, sq, self.key, self.iv))
                                        time.sleep(0.5)
                                    got_0500 = True
                    
                    if got_0500:
                        return f"✅ تم تنفيذ الأمر بنجاح بعد {attempt_counter} محاولة"
                    else:
                        return f"❌ فشل في تنفيذ الأمر بعد {attempt_counter} محاولة"
                        
                else:
                    wait_attempts = 0
                    max_wait_attempts = 3
                    
                    while not shared_0500_info['got'] and wait_attempts < max_wait_attempts and not restarting_now:
                        wait_attempts += 1
                        time.sleep(0.5)
                    
                    if not shared_0500_info['got']:
                        return "❌ timeout في انتظار الحساب الرئيسي"
                    
                    idT = shared_0500_info['idT']
                    sq = shared_0500_info['squad']
                    
                    if self.is_socket_connected(self.socket_client):
                        self.socket_client.send(GenJoinSquadsPacket(idT, self.key, self.iv))
                        time.sleep(0.5)
                        self.socket_client.send(ExiT('000000', self.key, self.iv))
                        time.sleep(0.1)
                        self.socket_client.send(ghost_pakcet(idT, account_name, sq, self.key, self.iv))
                        time.sleep(0.5)
                        return "✅ تم تنفيذ أمر الشبح بنجاح"
                    
            except Exception as e:
                return f"❌ خطأ: {e}"
        else:
            return f"❌ أمر غير معروف: {command}"

# ============ دوال تحميل الحسابات ============

def load_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ملف {file_path} غير موجود")
        return {}
    except json.JSONDecodeError:
        print(f"JSON غير صالح في {file_path}")
        return {}

def stop_all_clients():
    """إيقاف جميع العملاء"""
    print("🛑 جاري إيقاف جميع العملاء...")
    for account_id, client in list(clients.items()):
        try:
            client.stop()
        except Exception as e:
            print(f"خطأ في إيقاف {account_id}: {e}")
    clients.clear()
    print("✅ تم إيقاف جميع العملاء")

def start_all_clients():
    """بدء تشغيل جميع العملاء من جديد"""
    global clients, shared_0500_info
    
    print("🚀 جاري بدء تشغيل جميع العملاء...")
    
    # إعادة تعيين المتغيرات العامة
    shared_0500_info = {
        'got': False,
        'idT': None,
        'squad': None,
        'AutH': None
    }
    
    # تحميل الحسابات من الملف
    accounts = load_accounts('accounts.json')
    
    if not accounts:
        print("❌ لا توجد حسابات للتحميل")
        return
    
    # بدء تشغيل كل حساب
    for account_id, password in accounts.items():
        try:
            if account_id not in clients:
                client = TcpBotConnectMain(account_id, password)
                clients[account_id] = client
                client_thread = threading.Thread(target=client.run, daemon=True)
                client_thread.start()
                print(f"✅ تم بدء تشغيل الحساب: {account_id}")
                time.sleep(2)  # تأخير بين بدء كل حساب
            else:
                print(f"⚠️ الحساب {account_id} قيد التشغيل بالفعل")
        except Exception as e:
            print(f"❌ خطأ في بدء الحساب {account_id}: {e}")
    
    print(f"✅ تم بدء تشغيل {len(clients)} حساب بنجاح")

def full_restart():
    """إعادة تشغيل كاملة للبوت"""
    global restarting_now, shutting_down
    
    print("\n" + "="*60)
    print("🔄 [إعادة التشغيل التلقائي] بدء عملية إعادة التشغيل الكاملة...")
    print(f"🕐 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    restarting_now = True
    
    try:
        # إيقاف جميع العملاء
        stop_all_clients()
        
        # انتظار قليلاً للتأكد من إغلاق جميع الاتصالات
        time.sleep(3)
        
        # بدء تشغيل جميع العملاء من جديد
        start_all_clients()
        
    except Exception as e:
        print(f"❌ خطأ في عملية إعادة التشغيل: {e}")
    
    finally:
        restarting_now = False
        print("\n" + "="*60)
        print("✅ [إعادة التشغيل التلقائي] اكتملت عملية إعادة التشغيل بنجاح")
        print(f"🕐 الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")

def restart_scheduler():
    """جدولة إعادة التشغيل التلقائي"""
    global restart_timer
    
    while not shutting_down:
        try:
            # انتظار المدة المحددة (10 دقائق)
            for i in range(RESTART_INTERVAL, 0, -1):
                if shutting_down:
                    break
                if i % 60 == 0:  # كل دقيقة
                    minutes_left = i // 60
                    print(f"⏰ [جدولة إعادة التشغيل] متبقي {minutes_left} دقيقة على إعادة التشغيل التالية")
                time.sleep(1)
            
            if not shutting_down:
                # تنفيذ إعادة التشغيل
                full_restart()
                
        except Exception as e:
            print(f"❌ خطأ في جدولة إعادة التشغيل: {e}")
            time.sleep(60)  # انتظار دقيقة قبل المحاولة مرة أخرى

def cleanup():
    global shutting_down
    shutting_down = True
    print("\n🛑 جاري إيقاف الخادم...")
    stop_all_clients()
    print("✅ تم إيقاف الخادم بنجاح")

def signal_handler(sig, frame):
    print('\n📡 تم استقبال إشارة الإيقاف')
    cleanup()
    sys.exit(0)

# ============ مسارات API ============

@app.route('/start_client', methods=['GET'])
def start_client():
    if shutting_down:
        return jsonify({'error': 'الخادم قيد الإيقاف'}), 503
    
    account_id = request.args.get('account_id')
    password = request.args.get('password')
    
    if not account_id or not password:
        return jsonify({'error': 'مطلوب معرف الحساب وكلمة المرور'}), 400
    
    if account_id in clients:
        return jsonify({'error': 'العميل يعمل بالفعل'}), 400
    
    client = TcpBotConnectMain(account_id, password)
    clients[account_id] = client
    client_thread = threading.Thread(target=client.run, daemon=True)
    client_thread.start()
    
    return jsonify({'message': f'تم تشغيل العميل {account_id} بنجاح'}), 200

@app.route('/stop_client', methods=['GET'])
def stop_client():
    if shutting_down:
        return jsonify({'error': 'الخادم قيد الإيقاف'}), 503
    
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({'error': 'مطلوب معرف الحساب'}), 400
    
    if account_id not in clients:
        return jsonify({'error': 'العميل غير موجود'}), 404
    
    client = clients[account_id]
    client.stop()
    del clients[account_id]
    
    return jsonify({'message': f'تم إيقاف العميل {account_id} بنجاح'}), 200

@app.route('/execute_command', methods=['GET'])
def execute_command_api():
    if shutting_down:
        return jsonify({'error': 'الخادم قيد الإيقاف'}), 503
    
    account_id = request.args.get('account_id')
    command = request.args.get('command')
    
    if not account_id or not command:
        return jsonify({'error': 'مطلوب معرف الحساب والأمر'}), 400
    
    if account_id not in clients:
        return jsonify({'error': 'العميل غير موجود'}), 404
    
    client = clients[account_id]
    
    if command.startswith("/AlliFF"):
        if "=" in command:
            cmd, arg = command.split("=", 1)
        else:
            parts = command.split(" ", 1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else None
        
        if cmd == "/AlliFF" and arg:
            account_name = request.args.get('account_name', str(account_id))
            result = client.execute_command(cmd, arg, account_name)
            return jsonify({'result': result}), 200
    
    result = client.execute_command(command)
    return jsonify({'result': result}), 200

@app.route('/list_clients', methods=['GET'])
def list_clients():
    return jsonify({'clients': list(clients.keys())}), 200

@app.route('/execute_command_all', methods=['GET'])
def execute_command_all():
    if shutting_down or restarting_now:
        return jsonify({'error': 'البوت قيد إعادة التشغيل حالياً'}), 503
    
    command = request.args.get('command')
    if not command:
        return jsonify({'error': 'مطلوب الأمر'}), 400
    
    if "=" in command:
        cmd, arg = command.split("=", 1)
    else:
        parts = command.split(" ", 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
    
    ghost_names = {
        "4248116517": "AlliFF",
        "4248103380": "فلسطين حرة 🇵🇸",
        "4248100361": "Telegram: @AlliFF_BOT",
        "4228417617": "AlliFF_D5M",
    }
    
    results = {}
    
    master_client = clients.get(MASTER_ACCOUNT_ID)
    if master_client and cmd == "/AlliFF" and arg:
        master_name = ghost_names.get(MASTER_ACCOUNT_ID, MASTER_ACCOUNT_ID)
        master_result = master_client.execute_command(cmd, arg, master_name)
        results[MASTER_ACCOUNT_ID] = f"MASTER: {master_result}"
        time.sleep(1)
    
    for account_id, client in clients.items():
        if account_id != MASTER_ACCOUNT_ID:
            account_name = ghost_names.get(str(account_id), str(account_id))
            if cmd == "/AlliFF" and arg:
                result = client.execute_command(cmd, arg, account_name)
                results[account_id] = f"GHOST: {result}"
    
    return jsonify({'results': results})

@app.route('/ghost', methods=['GET'])
def ghost_command():
    if shutting_down or restarting_now:
        return jsonify({'error': 'البوت قيد إعادة التشغيل حالياً'}), 503
    
    name = request.args.get('name', 'Ghost')
    team_code = request.args.get('team_code')
    
    if not team_code:
        return jsonify({'error': 'مطلوب كود الفريق'}), 400
    
    ghost_names = {
        "4248116517": "AlliFF",
        "4248103380": "فلسطين حرة 🇵🇸",
        "4248100361": "Telegram: @AlliFF_BOT",
        "4228417617": "AlliFF_D5M",
    }
    
    results = {}
    
    master_client = clients.get(MASTER_ACCOUNT_ID)
    if master_client:
        master_name = ghost_names.get(MASTER_ACCOUNT_ID, MASTER_ACCOUNT_ID)
        master_result = master_client.execute_command("/AlliFF", team_code, master_name)
        results[MASTER_ACCOUNT_ID] = f"MASTER: {master_result}"
        time.sleep(1)
    
    for account_id, client in clients.items():
        if account_id != MASTER_ACCOUNT_ID:
            account_name = name if name else ghost_names.get(str(account_id), str(account_id))
            result = client.execute_command("/AlliFF", team_code, account_name)
            results[account_id] = f"GHOST: {result}"
    
    return jsonify({
        'command': 'ghost',
        'team_code': team_code,
        'results': results
    }), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'clients_count': len(clients),
        'clients': list(clients.keys()),
        'shutting_down': shutting_down,
        'restarting': restarting_now,
        'restart_interval_minutes': RESTART_INTERVAL // 60,
        'next_restart_in_seconds': None  # يمكنك إضافة عداد إذا أردت
    }), 200

@app.route('/manual_restart', methods=['GET'])
def manual_restart():
    """Endpoint لإعادة التشغيل يدوياً"""
    if restarting_now:
        return jsonify({'error': 'إعادة التشغيل قيد التنفيذ بالفعل'}), 400
    
    # تشغيل إعادة التشغيل في thread منفصل
    restart_thread = threading.Thread(target=full_restart, daemon=True)
    restart_thread.start()
    
    return jsonify({'message': 'جاري بدء إعادة التشغيل اليدوية...'}), 200

@app.route('/shutdown', methods=['GET'])
def shutdown_server():
    global shutting_down
    shutting_down = True
    cleanup()
    return jsonify({'message': 'جاري إيقاف الخادم'}), 200

# ============== التشغيل الرئيسي ==============

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup)
    
    print("\n" + "="*60)
    print("🚀 تشغيل بوت Free Fire مع إعادة تشغيل تلقائي")
    print("="*60)
    print(f"⏰ وقت البدء: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔄 مدة إعادة التشغيل: كل {RESTART_INTERVAL // 60} دقيقة")
    print("="*60 + "\n")
    
    # بدء تشغيل العملاء
    start_all_clients()
    
    # بدء جدولة إعادة التشغيل التلقائية
    restart_thread = threading.Thread(target=restart_scheduler, daemon=True)
    restart_thread.start()
    print("✅ تم بدء جدولة إعادة التشغيل التلقائية")
    
    # تشغيل الخادم
    try:
        port = int(os.environ.get('PORT', 8080))
        print(f"🌐 تشغيل خادم API على المنفذ {port}")
        print(f"📋 الروابط المتاحة:")
        print(f"   - /status → حالة البوت")
        print(f"   - /ghost?team_code=XXXXX → تنفيذ هجوم")
        print(f"   - /manual_restart → إعادة تشغيل يدوية")
        print(f"   - /list_clients → عرض الحسابات المتصلة")
        print("\n✅ البوت يعمل بنجاح...")
        
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        cleanup()