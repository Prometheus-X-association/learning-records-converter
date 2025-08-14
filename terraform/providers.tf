terraform {
  required_providers {
    scaleway = {
      source  = "scaleway/scaleway"
      version = "~> 2.58"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.6"
    }
  }
}

provider "scaleway" {
  region     = var.scaleway_region
  zone       = var.scaleway_zone
  # Use SCW_DEFAULT_PROJECT_ID, SCW_ACCESS_KEY and SCW_SECRET_KEY from environment
}

provider "aws" {
  region = var.aws_region
  # Use AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from environment
}
