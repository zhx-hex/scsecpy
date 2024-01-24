# coding:utf-8
# 多线程主机存活&端口探测 - ping/socket
# date:2024-1-7

import threading
import subprocess
import socket

class PortScanner:
    def __init__(self, subnet, start_host, end_host, start_port, end_port):
        self.subnet = subnet
        self.start_host = start_host
        self.end_host = end_host
        self.start_port = start_port
        self.end_port = end_port

    def is_host_alive(self, host, alive_hosts):
        try:
            command = ['ping', '-n', '1', host]
            result = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result == 0:
                print(f"host {host} is up")
                alive_hosts.append(host)
        except Exception as e:
                print(f"error: {e}")

    def scan_ports(self, host):
        for port in range(self.start_port, self.end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            try:
                result = sock.connect_ex((host, port))
                if result == 0:
                    print(f"{host} \tport {port} \t open")
            except Exception as e:
                print(f"error: {e}")
            finally:
                sock.close()

    def scan_hosts(self):
        alive_hosts = []

        print(f"scan host from {subnet}.{start_host} to {subnet}.{end_host} ...")
        for host in range(self.start_host, self.end_host + 1):
            ip = f"{self.subnet}.{host}"
            alive_thread = threading.Thread(target=self.is_host_alive, args=(ip, alive_hosts))
            alive_thread.start()
        print(f"the list of live hosts {alive_hosts}")

        print(f"scan live hosts on ports {start_port} to {end_port} ...")
        for alive_ip in alive_hosts:
            port_thread = threading.Thread(target=self.scan_ports, args=(alive_ip,))
            port_thread.start()


if __name__ == '__main__':

    # IPv4地址的网络号部分，格式如："192.168.123"
    subnet = '192.168.123'

    # 起始ip地址和结束ip地址，如：192.168.123.1 ~ 192.168.123.255
    start_host = 1
    end_host = 255

    # 起始端口号和结束端口号，如：1 ~ 1024
    start_port = 1
    end_port = 1024
    
    scanner = PortScanner(subnet, start_host, end_host, start_port, end_port)
    scanner.scan_hosts()
