import subprocess
import socket
import ipaddress
import json

def generate_ipv4_addresses():
    # Generate all possible IPv4 addresses
    for ip_int in range(0x01000000, 0xFFFFFFFF):
        yield str(ipaddress.IPv4Address(ip_int))

def nslookup(ip):
    try:
        # Use nslookup to get the domain name associated with the IP address
        result = subprocess.check_output(["nslookup", ip], universal_newlines=True)
        lines = result.split('\n')
        for line in lines:
            if "name =" in line:
                return line.split("name =")[1].strip()
    except Exception as e:
        pass
    return None

if __name__ == "__main__":
    ip_url_dict = {}  # Dictionary to store IP/URL pairs
    
    for ip in generate_ipv4_addresses():
        try:
            # Try to resolve the IP address to a domain name
            url = nslookup(ip)
            if url:
                ip_url_dict[ip] = url
                print(f"IP: {ip} | URL: {url}")
        except KeyboardInterrupt:
            print("Scan interrupted by user")
            break
        except Exception as e:
            pass
    
    # Write the IP/URL dictionary to a JSON file
    with open("ip_url_pairs.json", "w") as json_file:
        json.dump(ip_url_dict, json_file, indent=4)
    
    print("IP/URL pairs saved to ip_url_pairs.json")
