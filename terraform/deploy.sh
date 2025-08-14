#!/bin/bash
# ==============================================================================
# deploy.sh - Ultra-simple deployment script for LRC
# ==============================================================================

set -e

# Help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    cat << EOF
🚀 Ultra-Simple LRC Deployment

Usage:
    ./deploy.sh          Deploy infrastructure
    ./deploy.sh destroy  Destroy infrastructure

Setup:
    1. cp terraform.tfvars.example terraform.tfvars
    2. Edit terraform.tfvars with your values
    3. ./deploy.sh
EOF
    exit 0
fi

echo "🚀 LRC Ultra-Simple Deployment"

# Destroy mode
if [[ "$1" == "destroy" ]]; then
    echo "💥 Destroying infrastructure..."
    terraform destroy -auto-approve
    echo "✅ Infrastructure destroyed!"
    exit 0
fi

# Basic checks
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed"
    exit 1
fi

if [ ! -f "terraform.tfvars" ]; then
    echo "❌ Copy terraform.tfvars.example to terraform.tfvars and edit it"
    exit 1
fi

# Check credentials (only if deploying to that platform)
if grep -q "deploy_to_aws.*=.*true" terraform.tfvars; then
    if ! aws sts get-caller-identity &> /dev/null; then
        echo "❌ AWS credentials not configured"
        echo "   export AWS_ACCESS_KEY_ID=your-key"
        echo "   export AWS_SECRET_ACCESS_KEY=your-secret"
        exit 1
    fi
fi

if grep -q "deploy_to_scaleway.*=.*true" terraform.tfvars; then
    if [[ -z "${SCW_ACCESS_KEY:-}" ]]; then
        echo "❌ Scaleway credentials not configured"
        echo "   export SCW_ACCESS_KEY=your-key"
        echo "   export SCW_SECRET_KEY=your-secret"
        echo "   export SCW_DEFAULT_PROJECT_ID=your-project-id"
        exit 1
    fi
fi

# Deploy
echo "📋 Initializing..."
terraform init

echo "📋 Planning..."
terraform plan

echo "🚀 Deploying..."
terraform apply -auto-approve

echo "✅ Deployment completed!"
echo ""

# Show URLs
echo "🌐 Your URLs:"
if terraform output scaleway_url &> /dev/null; then
    echo "Scaleway: $(terraform output -raw scaleway_url)"
fi
if terraform output aws_url &> /dev/null; then
    echo "AWS:      $(terraform output -raw aws_url)"
fi

echo ""
echo "🧪 Test your deployment:"
if terraform output scaleway_url &> /dev/null; then
    echo "curl $(terraform output -raw scaleway_url)/health"
fi
if terraform output aws_url &> /dev/null; then
    echo "curl $(terraform output -raw aws_url)/health"
fi
