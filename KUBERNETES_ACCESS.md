# Kubernetes Access Guide (Decryption)

This guide explains how to decrypt and use the `kubeconfig` to access your HA cluster.

## Prerequisites

- **Mozilla SOPS**: Installed on Windows or WSL.
  - Windows (PowerShell): `winget install Mozilla.SOPS`
- **kubectl**: Installed locally.
- **SOPS_AGE_KEY**: Available in your `.env` file.

## Decryption Command (Windows PowerShell)

```powershell
# 1. Set the key
$env:SOPS_AGE_KEY = "<YOUR_AGE_SECRET_KEY>"

# 2. Decrypt
sops -d ansible/kubeconfigs/<CLUSTER_NAME>.enc.yaml > ~/.kube/config
```

## HA Cluster Connection

The kubeconfig is configured to use the cluster domain:
`server: https://<YOUR_CLUSTER_DOMAIN>:6443`

For High Availability to work:
- Your local machine must be able to resolve the domain.
- The domain should point to **all** Master IPs in your DNS settings.
- `kubectl` will automatically fallback to the next IP if one Master is down.

## Verify Connection

```bash
kubectl get nodes -o wide
```
Nodes should show their **Tailscale IPs** as INTERNAL-IP.
