# Platform Engineering Demo - Helm Chart

This Helm chart deploys the Flask-based Platform Engineering Demo application with PostgreSQL on Kubernetes.

## Chart Structure

```
helm/platform-engineering-demo/
├── Chart.yaml                 # Chart metadata
├── values.yaml               # Default values (production-like)
├── values-dev.yaml           # Development environment values
├── values-staging.yaml       # Staging environment values
├── values-prod.yaml          # Production environment values
└── templates/
    ├── _helpers.tpl          # Template helpers and labels
    ├── namespace.yaml        # Namespace resource
    ├── configmap.yaml        # Configuration data
    ├── secret.yaml           # Secrets (database password)
    ├── postgres-pvc.yaml     # PostgreSQL persistent volume claim
    ├── postgres-deployment.yaml  # PostgreSQL deployment
    ├── postgres-service.yaml # PostgreSQL service
    ├── backend-deployment.yaml   # Flask backend deployment
    ├── backend-service.yaml  # Backend service
    ├── ingress-class.yaml    # Ingress class
    └── ingress.yaml          # Ingress resource
```

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to access your cluster

## Installation

### 1. Add the chart to your local repository

```bash
# Navigate to the helm directory
cd helm/
```

### 2. Validate the chart

```bash
helm lint platform-engineering-demo/
```

### 3. Dry-run to preview manifests

```bash
# Development environment
helm template my-release platform-engineering-demo/ -f platform-engineering-demo/values-dev.yaml

# Staging environment
helm template my-release platform-engineering-demo/ -f platform-engineering-demo/values-staging.yaml

# Production environment
helm template my-release platform-engineering-demo/ -f platform-engineering-demo/values-prod.yaml
```

### 4. Install the chart

#### Development Environment
```bash
helm install platform-demo platform-engineering-demo/ \
  -f platform-engineering-demo/values-dev.yaml \
  --create-namespace
```

#### Staging Environment
```bash
helm install platform-demo platform-engineering-demo/ \
  -f platform-engineering-demo/values-staging.yaml \
  --create-namespace
```

#### Production Environment
```bash
helm install platform-demo platform-engineering-demo/ \
  -f platform-engineering-demo/values-prod.yaml \
  --create-namespace
```

## Upgrade

```bash
# Upgrade an existing release
helm upgrade platform-demo platform-engineering-demo/ \
  -f platform-engineering-demo/values-prod.yaml
```

## Uninstall

```bash
# Remove the Helm release
helm uninstall platform-demo

# Optional: Delete the namespace
kubectl delete namespace employee-prod
```

## Configuration

### Environment-Specific Values

#### Development (`values-dev.yaml`)
- Namespace: `employee-dev`
- Backend replicas: 1
- Image pull policy: `Always` (for development)
- Resources: Lower limits (128Mi memory, 100m CPU)
- Service type: `NodePort`
- PersistentVolume: 500Mi

#### Staging (`values-staging.yaml`)
- Namespace: `employee-staging`
- Backend replicas: 2
- Image pull policy: `IfNotPresent`
- Resources: Medium limits (256Mi memory, 250m CPU)
- Service type: `ClusterIP`
- PersistentVolume: 2Gi
- Rate limiting: 100 requests

#### Production (`values-prod.yaml`)
- Namespace: `employee-prod`
- Backend replicas: 3
- Image pull policy: `IfNotPresent`
- Resources: Higher limits (512Mi memory, 500m CPU)
- Service type: `ClusterIP`
- PersistentVolume: 10Gi
- Rate limiting: 500 requests
- SSL redirect enabled

### Key Parameters

- `namespace.name`: Kubernetes namespace
- `app.environment`: Environment name (development, staging, production)
- `backend.replicas`: Number of backend pods
- `backend.image.tag`: Docker image tag
- `postgresql.persistence.size`: Database storage size
- `database.name`: PostgreSQL database name

## Accessing the Application

### Get the service URL

```bash
# Development (NodePort)
kubectl get svc -n employee-dev
minikube service platform-demo-backend -n employee-dev

# Staging/Production (Ingress)
kubectl get ingress -n employee-staging
curl http://api-staging.minikube.local
```

### View logs

```bash
# Backend logs
kubectl logs -n employee-dev deployment/platform-demo-backend

# PostgreSQL logs
kubectl logs -n employee-dev deployment/platform-demo-postgres
```

### Access PostgreSQL

```bash
# Port forward to the PostgreSQL service
kubectl port-forward -n employee-dev svc/platform-demo-postgres 5432:5432

# Connect with psql
psql -h localhost -U postgres -d employee_dev
```

## Customization

### Override values at install time

```bash
helm install platform-demo platform-engineering-demo/ \
  -f values-dev.yaml \
  --set backend.replicas=2 \
  --set postgresql.persistence.size=2Gi
```

### Create custom values file

```bash
# Copy and modify an existing values file
cp platform-engineering-demo/values-staging.yaml values-custom.yaml

# Edit and install
helm install platform-demo platform-engineering-demo/ -f values-custom.yaml
```

## Managing Secrets

The chart includes a secret for the PostgreSQL password (base64 encoded: `mysecretpassword`).

To use a different password:

1. Generate base64 encoded password:
```bash
echo -n "your-new-password" | base64
```

2. Edit `templates/secret.yaml` and update the password values

3. Reinstall the chart or update the secret:
```bash
kubectl patch secret platform-demo-postgres-secret -p '{"data":{"DB_PASSWORD":"new-base64-value"}}'
```

## Health Checks

Both backend and PostgreSQL deployments include:
- **Liveness probe**: Ensures containers are restarted if they become unhealthy
- **Readiness probe**: Ensures traffic is only sent to ready pods

## Resource Management

Each environment has optimized resource requests and limits:

| Environment | Memory Request | CPU Request | Memory Limit | CPU Limit |
|-------------|----------------|------------|--------------|-----------|
| Development | 128Mi | 100m | 256Mi | 200m |
| Staging | 256Mi | 250m | 512Mi | 500m |
| Production | 512Mi | 500m | 1Gi | 1000m |

## Troubleshooting

### Check chart syntax
```bash
helm lint platform-engineering-demo/
```

### Dry-run to validate
```bash
helm install platform-demo platform-engineering-demo/ \
  -f values-dev.yaml \
  --dry-run --debug
```

### Describe resources
```bash
kubectl describe pod <pod-name> -n employee-dev
kubectl describe service <service-name> -n employee-dev
```

### View rendered templates
```bash
helm template platform-demo platform-engineering-demo/ \
  -f values-dev.yaml
```

## License

Same as the application

## Support

For issues or questions, contact platform-team@gmail.com
