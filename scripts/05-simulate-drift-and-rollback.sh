#!/bin/bash
# Script 5: Simulate config drift and demonstrate auto-reconciliation + rollback

set -e

APP_NS="production"

echo "=== Current state ==="
kubectl get deployments -n $APP_NS

echo ""
echo "=== Simulating config drift: manually scaling down app ==="
kubectl scale deployment sample-app --replicas=0 -n $APP_NS

echo "Waiting 15 seconds for Argo CD to detect drift..."
sleep 15

echo ""
echo "=== Argo CD sync status (should show OutOfSync) ==="
kubectl get application sample-app -n argocd -o jsonpath='{.status.sync.status}'
echo ""

echo "=== Triggering manual sync to reconcile ==="
# Using kubectl patch to trigger sync (argocd CLI alternative)
kubectl patch application sample-app -n argocd \
  --type merge \
  -p '{"operation": {"initiatedBy": {"username": "admin"}, "sync": {"revision": "HEAD"}}}'

echo "Waiting for sync to complete..."
sleep 20

echo ""
echo "=== Post-reconciliation state ==="
kubectl get deployments -n $APP_NS

echo ""
echo "=== Rollback demo: revert to previous Git revision ==="
echo "In a real scenario, you would run:"
echo "  git revert HEAD && git push"
echo "  Argo CD will auto-sync to the reverted state"
