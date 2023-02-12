import os
import platform
import subprocess


def get_local_dns_server(self):
    """Get the local DNS server for the local operating system"""
    os_name = platform.system().lower()
    dns_servers = []

    if os_name == "windows":
        def get_dns_servers():
            result = subprocess.run("ipconfig /all", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                for line in result.stdout.decode("utf-8").strip().split("\n"):
                    if "DNS Servers" in line:
                        dns = line.split(":")[1].strip()
                        yield dns
        dns_servers = list(get_dns_servers())

    elif os_name == "linux":
        def get_dns_servers():
            device = None
            result = subprocess.run("nmcli connection show --active", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                connections = result.stdout.decode("utf-8").strip().split("\n")
                for i, line in enumerate(connections):
                    if i == 1 and line.strip():
                        device = line.strip().split()[3]
                    if device is not None:
                        result = subprocess.run(f"nmcli device show {device}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        if result.returncode == 0:
                            for line in result.stdout.decode("utf-8").strip().split("\n"):
                                if line.startswith("IP4.DNS"):
                                    dns = line.split(":")[1].strip()
                                    yield dns
        dns_servers = list(get_dns_servers())
    elif os_name == "darwin":
        def get_dns_servers():
            result = subprocess.run("scutil --dns", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                for line in result.stdout.decode("utf-8").strip().split("\n"):
                    if line.startswith("nameserver"):
                        dns = line.split()[1]
                        yield dns
        dns_servers = list(get_dns_servers())
    else:
        # Handle other operating systems here
        print("Sorry, this operating system is not supported.")
        pass

    print("Local primary DNS server:", dns_servers[0])
    print("Local secondary DNS server:", dns_servers[1])
    self.dns_providers.append(("Local", dns_servers[0], dns_servers[1]))
