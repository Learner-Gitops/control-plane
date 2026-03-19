#!/bin/bash
# Script 6: Collect and display results for the research paper

set -e

echo "============================================"
echo "  GitOps Control Plane - Results Summary"
echo "============================================"
echo ""

echo "--- Cluster Nodes ---"
kubectl get nodes -o wide

echo ""
echo "--- Argo CD Applications ---"
kubectl get applications -n argocd -o custom-columns=\
"NAME:.metadata.name,\
SYNC:.status.sync.status,\
HEALTH:.status.health.status,\
REPO:.spec.source.repoURL,\
PATH:.spec.source.path"

echo ""
echo "--- Production Namespace Resources ---"
kubectl get all -n production

echo ""
echo "--- Deployment Replica Status ---"
kubectl get deployment sample-app -n production -o jsonpath=\
'{"\nDesired: "}{.spec.replicas}{"\nReady:   "}{.status.readyReplicas}{"\nAvailable: "}{.status.availableReplicas}{"\n"}'

echo ""
echo "--- Argo CD Sync History (last 5) ---"
kubectl get application sample-app -n argocd \
  -o jsonpath='{range .status.history[-5:]}{.deployedAt}{"  rev:"}{.revision}{"  "}{.source.path}{"\n"}{end}'

echo ""
echo "--- RBAC Roles Applied ---"
kubectl get roles,rolebindings -n production
kubectl get clusterroles | grep platform-team

echo ""
echo "--- ConfigMap (Desired State) ---"
kubectl get configmap sample-app-config -n production -o yaml

echo ""
echo "============================================"
echo "  Results collection complete"
echo "============================================"
