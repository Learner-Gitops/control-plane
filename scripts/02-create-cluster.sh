#!/bin/bash
# Script 2: Create local Kubernetes cluster using kind

set -e

echo "=== Creating kind cluster: gitops-hub ==="
kind create cluster --name gitops-hub --config ../clusters/kind-config.yaml

echo "=== Verifying cluster ==="
kubectl cluster-info --context kind-gitops-hub
kubectl get nodes
