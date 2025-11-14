devices = [ ("192.168.1.10", [22, 80, 443]),
("192.168.1.11", [21, 22, 80]), ("192.168.1.12", [23,
80, 3389])]
risky_ports = [21, 23, 3389]
open_risky_ports_count = 0
print("Starting port scan...")
for device in devices:
    ip, ports = device
    open_risky_ports = []
    for port in ports:
        if port in risky_ports:
            open_risky_ports.append(port)
            open_risky_ports_count += 1
    if open_risky_ports:
        print(f"WARNING: Device {ip} has risky open ports: {', '.join(map(str, open_risky_ports))}")
print(f"Port scan complete! Total risky open ports found: {open_risky_ports_count}")