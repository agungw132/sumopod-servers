#!/usr/bin/env python3
import os
import json
import re

def get_inventory():
    inventory = {
        'cloud_servers': {
            'hosts': [],
            'vars': {
                'ansible_python_interpreter': '/usr/bin/python3',
                'k8s_domain': os.environ.get('K8S_DOMAIN', 'localhost'),
                'firewall_trusted_ip': os.environ.get('FIREWALL_TRUSTED_IP', '127.0.0.1')
            }
        },
        '_meta': {
            'hostvars': {}
        }
    }

    # Pola untuk mencari IP (misal: SERVER_PUBLIC_IP_ADDRESS, SERVER_PUBLIC_IP_ADDRESS_2, dst)
    ip_pattern = re.compile(r'^SERVER_PUBLIC_IP_ADDRESS(?:_(\d+))?$')

    # Map cluster domains - format: K8S_DOMAIN_CLUSTER_NAME_N and K8S_DOMAIN_CLUSTER_IP_ADDRESS_N
    # We will map "Cluster Name" -> "Domain" and "Cluster Name" -> "IP"
    cluster_name_to_domain = {}
    cluster_name_to_ip = {}
    
    cluster_pattern = re.compile(r'^K8S_DOMAIN_CLUSTER_NAME_(\d+)$')
    for env_var, domain in os.environ.items():
        match = cluster_pattern.match(env_var)
        if match:
            idx = match.group(1)
            # Get the corresponding IP for this cluster domain
            ip_var = f"K8S_DOMAIN_CLUSTER_IP_ADDRESS_{idx}"
            domain_ip = os.environ.get(ip_var, '')
            
            # Extract cluster name from domain (assuming format clustername.domain.tld)
            # Or simplified: if the domain starts with the cluster name
            parts = domain.split('.')
            if len(parts) > 0:
                c_name = parts[0]
                cluster_name_to_domain[c_name] = domain
                cluster_name_to_ip[c_name] = domain_ip

    for env_var, ip in os.environ.items():
        match = ip_pattern.match(env_var)
        if match and ip:
            suffix = match.group(1)
            # ... (logika sebelumnya)
            index = suffix if suffix else "1"
            hostname = f"server_{index}"
            
            # Cari user, password, hostname, dan role yang sesuai berdasarkan suffix
            user_var = f"SERVER_USERNAME{'_' + suffix if suffix else ''}"
            pass_var = f"SERVER_PASSWORD{'_' + suffix if suffix else ''}"
            name_var = f"SERVER_HOSTNAME{'_' + suffix if suffix else ''}"
            role_var = f"SERVER_ROLE{'_' + suffix if suffix else ''}"
            
            user = os.environ.get(user_var, os.environ.get('SERVER_USERNAME', 'root'))
            password = os.environ.get(pass_var, os.environ.get('SERVER_PASSWORD', ''))
            custom_hostname = os.environ.get(name_var)
            
            role_raw = os.environ.get(role_var, 'none')
            role_parts = [p.strip() for p in role_raw.split(',')]
            
            server_mode = role_parts[0] if len(role_parts) > 0 else 'none'
            cluster_name = role_parts[1] if len(role_parts) > 1 else 'default'
            node_function = role_parts[2] if len(role_parts) > 2 else 'standalone'

            inventory['cloud_servers']['hosts'].append(hostname)
            
            if cluster_name not in inventory:
                inventory[cluster_name] = {'hosts': [], 'vars': {}}
            inventory[cluster_name]['hosts'].append(hostname)
            
            # Assign domain to host based on cluster_name
            cluster_domain = cluster_name_to_domain.get(cluster_name, '')
            cluster_domain_ip = cluster_name_to_ip.get(cluster_name, '')
            
            # ... (sisanya sama)
            func_group = f"role_{node_function}"
            if func_group not in inventory:
                inventory[func_group] = {'hosts': [], 'vars': {}}
            inventory[func_group]['hosts'].append(hostname)

            inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': ip,
                'ansible_user': user,
                'ansible_ssh_pass': password,
                'custom_system_hostname': custom_hostname,
                'server_mode': server_mode,
                'cluster_name': cluster_name,
                'node_function': node_function,
                'cluster_domain': cluster_domain,
                'cluster_domain_ip': cluster_domain_ip
            }

    return inventory

if __name__ == "__main__":
    print(json.dumps(get_inventory()))
