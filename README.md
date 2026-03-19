# GitOps-Based Deployment Control Plane

Research implementation for: "Designing a GitOps-Based Deployment Control Plane for Scalable Kubernetes Platforms"

## Prerequisites (Install from Google)

Before running anything, install these manually:

1. **Docker Desktop** (required by kind)
   - https://www.docker.com/products/docker-desktop/

2. **WSL2** (if on Windows)
   - Run in PowerShell as Admin: `wsl --install`
   - Then use Ubuntu terminal for all commands below

## Run Order

Open a terminal (WSL/Ubuntu on Windows) and run scripts in order:

```bash
cd gitops-control-plane/scripts

# Step 1: Install kubectl, kind, helm
bash 01-install-tools.sh

# Step 2: Create local Kubernetes cluster
bash 02-create-cluster.sh

# Step 3: Install Argo CD
bash 03-install-argocd.sh

# Step 4: Push this repo to GitHub first, then deploy apps
# git remote add origin https://github.com/Learner-Gitops/control-plane.git
# git branch -M main
# git add . && git commit -m "initial" && git push -u origin main
bash 04-deploy-apps.sh

# Step 5: Simulate drift and auto-reconciliation
bash 05-simulate-drift-and-rollback.sh

# Step 6: Collect results
bash 06-collect-results.sh
```

## Architecture

```
GitHub Repo (Source of Truth)
        |
        v
   Argo CD (Hub)
   /           \
Cluster        Cluster
(production)  (staging)
```

- App teams push code → triggers CI
- Platform team manages gitops-control-plane/ → Argo CD syncs
- Any manual cluster change is auto-reverted (selfHeal: true)
- Rollback = git revert + push
