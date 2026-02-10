# Ansible WSL Debian Guide

## Overview

This guide explains how to run Ansible using WSL (Windows Subsystem for Linux) with Debian distribution instead of Docker.

## Setup WSL Debian

1.  **Install Debian**: `wsl --install -d Debian`
2.  **Install Ansible**:
    ```bash
    sudo apt update && sudo apt install -y python3-pip python3-venv sshpass
    pip3 install ansible --break-system-packages
    ```

## Running Ansible

### Load Environment & Run Playbook

All commands are run from Windows PowerShell in the project root:

```powershell
# 1. Load Environment Variables
wsl -d Debian bash -c "set -a && source <PROJECT_PATH>/.env && set +a"

# 2. Run Full Deployment
wsl -d Debian bash -c "set -a && source <PROJECT_PATH>/.env && set +a && cd <PROJECT_PATH>/ansible && export ANSIBLE_HOST_KEY_CHECKING=False && ansible-playbook -i inventory/dynamic_env.py site.yml"
```

## Playbook Structure (Role Order)

The `site.yml` follows a specific sequence for HA and Security:

1.  **common**: Basic setup and hostnames.
2.  **tailscale**: Establishes the encrypted mesh network.
3.  **k3s**: Deploys Kubernetes using Overlay IPs.
4.  **firewall**: Locks down the system *after* services are active.

## Centralized Configuration (`ansible/group_vars/all.yml`)

- **tailscale_version**: Managed version of Tailscale.
- **k3s_pod_cidr**: Managed Pod IP range.
- **k3s_service_cidr**: Managed Service IP range.