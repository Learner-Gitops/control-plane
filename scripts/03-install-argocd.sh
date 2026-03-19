#!/bin/bash
# Script 3: Install Argo CD on the hub cluster

set -e

echo "=== Creating argocd namespace ==="
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -

echo "=== Installing Argo CD ==="
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "=== Waiting for Argo CD pods to be ready ==="
kubectl wait --for=condition=available --timeout=120s deployment/argocd-server -n argocd

echo "=== Getting initial admin password ==="
echo "Run this to get the password:"
echo "  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d"

echo ""
echo "=== Port-forward Argo CD UI ==="
echo "Run this to access the UI at https://localhost:8080"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
