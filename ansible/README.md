# Ansible Infrastructure

This directory contains the automated configuration for the SumoPod server fleet.

## Inventory System

Instead of a static file, we use a **Dynamic Inventory** script:
- `inventory/dynamic_env.py`: Parses environment variables with the prefix `SERVER_` and maps them to Ansible hosts.
- It also reads `INSTALL_ALSO_ON_K8S_MASTER` (default: `true`) to determine if master nodes should be tainted.

## Global Variables (`group_vars/all.yml`)

The following global parameters are managed centrally:
- `tailscale_version`: Target version for Tailscale installation/updates.
- `k3s_pod_cidr`: The IP range for Kubernetes Pods.
- `k3s_service_cidr`: The IP range for Kubernetes Services.

## Roles

| Role | Description |
|------|-------------|
| **common** | Sets system hostname and gathers system facts. |
| **tailscale** | Configures encrypted mesh networking with version control. |
| **k3s** | Installs K3s using Tailscale IPs and redundant masters. |
| **firewall** | Configures `firewalld`/`ufw` with rules for all cluster interfaces. |

## Kubernetes Configuration

Encrypted `kubeconfig` files are stored in `kubeconfigs/`. These are encrypted using **Mozilla SOPS** and the **Age** key defined in your `.env` file.

To decrypt, follow the instructions in [`KUBERNETES_ACCESS.md`](../KUBERNETES_ACCESS.md).