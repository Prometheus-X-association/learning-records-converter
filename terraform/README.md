# LRC Terraform - Simple Multi-Cloud Deployment

Simple Terraform infrastructure to deploy LRC on AWS App Runner and/or Scaleway
Container.

## 🚀 Quick Setup & Deployment

### 1. Copy and edit configuration

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:

```hcl
# Choose platforms
deploy_to_aws      = true
deploy_to_scaleway = false

# Docker image
docker_image = "ghcr.io/your-org/lrc:latest"
```

Note : for deployment on AWS, the image must be pushed publicly to ECR (AWS's
public Container Registry service).

### 2. Configure credentials

**Option A: CLI tools (recommended)**

```bash
aws configure   # For AWS - interactive setup
scw init        # For Scaleway - interactive setup
```

**Option B: Environment variables**

```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export SCW_ACCESS_KEY="your-key"  
export SCW_SECRET_KEY="your-secret"
export SCW_DEFAULT_PROJECT_ID="your-project-id"
```

### 3. Deploy

```bash
chmod +x ./deploy.sh
./deploy.sh
```

## 📁 Structure

```
terraform/
├── providers.tf          # Providers configuration
├── variables.tf          # Configuration variables
├── locals.tf             # Environment variables overriding
├── aws.tf                # AWS App Runner resources
├── scaleway.tf           # Scaleway Container resources
├── outputs.tf            # Output URLs
├── terraform.tfvars.example
└── deploy.sh             # Deployment script
```

### Alternative: Direct Terraform

In the directory `terraform`:

```bash
terraform init
terraform plan
terraform apply
```

## 🔧 Main Variables

| Variable             | Description                 | Default      |
|----------------------|-----------------------------|--------------|
| `deploy_to_aws`      | Deploy to AWS               | `false`      |
| `deploy_to_scaleway` | Deploy to Scaleway          | `false`      |
| `docker_image`       | Docker image to deploy      | *required*   |
| `environment`        | Environment name            | `production` |
| `memory_limit`       | Memory limit (MB)           | `1024`       |
| `cpu_limit`          | CPU limit                   | `250`        |
| `min_instances`      | Minimal number of instances | `1`          |
| `max_instances`      | Maximal number of instances | `3`          |
| `log_level`          | LRC log level               | `info`       |

## 📋 Prerequisites

- [Terraform](https://terraform.io) >= 1.0
- Published LRC Docker image
- [AWS CLI](https://aws.amazon.com/cli/) (if deploying to AWS)
- [Scaleway CLI](https://github.com/scaleway/scaleway-cli) (if deploying to
  Scaleway)

## 📊 Outputs

After deployment:

```bash
terraform output
```

```
aws_url = "https://xxxxx.eu-west-3.awsapprunner.com"
scaleway_url = "https://xxxxx-lrc-production.functions.fnc.fr-par.scw.cloud"
summary = {
  "aws" = "https://xxxxx.eu-west-3.awsapprunner.com"
  "environment" = "production"
  "scaleway" = "https://xxxxx-lrc-production.functions.fnc.fr-par.scw.cloud"
}
```

## 🏥 Health Check

```bash
# Verify service is responding
curl https://your-service-url/health
```

## 🔍 Troubleshooting

### "image not found" error

```bash
# Verify image exists
docker pull ghcr.io/your-org/lrc:latest
```

### "credentials not configured" error

```bash
# AWS
aws sts get-caller-identity

# Scaleway
scw config get
```

### Service won't start

```bash
# Check logs
# AWS: CloudWatch
# Scaleway: scw container logs <container-id>
```

## 🎛️ Multiple Environments

```bash
# Create different config files
cp terraform.tfvars.example terraform-prod.tfvars
cp terraform.tfvars.example terraform-staging.tfvars

# Edit each with different values
# terraform-prod.tfvars: environment = "production"
# terraform-staging.tfvars: environment = "staging"

# Deploy with specific config
cp terraform-prod.tfvars terraform.tfvars
./deploy.sh

# Or use terraform directly
terraform apply -var-file="terraform-prod.tfvars"
```

## 🧹 Cleanup

```bash
# Destroy infrastructure
./deploy.sh destroy

# or with terraform directly
terraform destroy
```

---

**Simple, effective, and it works! 🎉**
