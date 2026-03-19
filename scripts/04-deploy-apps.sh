#!/bin/bash
# Script 4: Deploy GitOps applications via Argo CD

set -e

echo "=== Applying RBAC policies ==="
kubectl apply -f ../infrastructure/rbac/

echo "=== Registering Argo CD Applications ==="
kubectl apply -f ../infrastructure/argocd-apps/

echo "=== Checking sync status ==="
sleep 5
kubectl get applications -n argocd
