# Server Configuration Documentation

This document tracks the automated configurations for the Kubernetes fleet.

## Fleet Status

| Cluster Name | Role | Node Name | Public IP | Tailscale IP | Function |
|--------------|------|-----------|-----------|--------------|----------|
| **<CLUSTER_NAME>** | Master | <MASTER_1_HOSTNAME> | <PUBLIC_IP_1> | <TAILSCALE_IP_1> | Primary Control Plane |
| **<CLUSTER_NAME>** | Master | <MASTER_2_HOSTNAME> | <PUBLIC_IP_2> | <TAILSCALE_IP_2> | HA Control Plane (Backup) |
| **<CLUSTER_NAME>** | Worker | <WORKER_1_HOSTNAME> | <PUBLIC_IP_3> | <TAILSCALE_IP_3> | Worker Node |
| **<CLUSTER_NAME>** | Worker | <WORKER_N_HOSTNAME> | <PUBLIC_IP_N> | <TAILSCALE_IP_N> | Worker Node |

---

## Configuration History

### 2026-02-10: Multi-Master HA with Tailscale & SSL

#### 1. Network Architecture (Tailscale Mesh)
- **Overlay Network**: All nodes communicate via **Tailscale** overlay IPs.
- **Encryption**: WireGuard encryption for all inter-node traffic.
- **K3s Flannel**: Configured to use `tailscale0` as the primary interface.
- **Centralized Networking**: CIDRs for Pods and Services are managed in `group_vars/all.yml`.

#### 2. High Availability (HA)
- **Multi-Master**: Multiple nodes serve as HA masters with clustered etcd.
- **Domain Access**: Cluster domain points to multiple Master IPs for DNS Round Robin redundancy.
- **Kubeconfig**: Uses the domain name for resilient cluster management.

#### 3. Security & Firewall
- **Post-Service Lockdown**: Firewall is configured *after* Tailscale and K3s are active.
- **Tailscale Trust**: The `tailscale0` interface and its overlay IPs are explicitly trusted.
- **Public Services**: HTTP (80) and HTTPS (443) open on Master nodes for Ingress traffic.

#### 4. Master Node Isolation
- **Configurable Workloads**: Master nodes can be configured to run or reject application workloads using `INSTALL_ALSO_ON_K8S_MASTER` in `.env`.
- **Default Behavior**: By default (`true`), master nodes act as both control plane and worker nodes.
- **Isolation Mode**: If set to `false`, master nodes are tainted (`CriticalAddonsOnly=true:NoSchedule`), ensuring they only run system components.
- **Revertable**: This setting can be toggled at any time by updating `.env` and re-running the Ansible playbook.

---

## Ansible Infrastructure

- **Role Execution Order**: `common` -> `tailscale` -> `k3s` -> `firewall`.
- **Inventory**: Dynamic Python script parses environment variables.
- **Secret Management**: Mozilla SOPS + Age for encrypted kubeconfigs.

## Quick Start (WSL Debian)

```powershell
# Run full playbook
wsl -d Debian bash -c "set -a && source <PROJECT_PATH>/.env && set +a && cd <PROJECT_PATH>/ansible && ansible-playbook -i inventory/dynamic_env.py site.yml"
```
