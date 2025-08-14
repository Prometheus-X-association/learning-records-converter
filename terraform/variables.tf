# Platform selection
variable "deploy_to_aws" {
  description = "Deploy to AWS App Runner"
  type        = bool
  default     = false
}

variable "deploy_to_scaleway" {
  description = "Deploy to Scaleway Container"
  type        = bool
  default     = false
}

# Scaleway configuration
variable "scaleway_region" {
  description = "Scaleway region"
  type        = string
  default     = "fr-par"
}

variable "scaleway_zone" {
  description = "Scaleway zone"
  type        = string
  default     = "fr-par-2"
}

# AWS configuration
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-3"
}

# Application configuration
variable "app_name" {
  description = "Application name"
  type        = string
  default     = "lrc"
}

variable "environment" {
  description = "Environment (development/production)"
  type        = string
  default     = "production"
}

variable "docker_image" {
  description = "Docker image to deploy (ex: ghcr.io/username/lrc:latest)"
  type        = string
}

# Container configuration
variable "port" {
  description = "Container port"
  type        = number
  default     = 8000
}

variable "memory_limit" {
  description = "Memory limit in MB"
  type        = number
  default     = 512
}

variable "cpu_limit" {
  description = "CPU limit (mCPU for Scaleway, vCPU for AWS)"
  type        = number
  default     = 250
}

variable "timeout" {
  description = "Request timeout in seconds"
  type        = number
  default     = 90
}

variable "log_level" {
  description = "Log level"
  type        = string
  default     = "info"
}

variable "min_instances" {
  description = "Minimal number of instances"
  type        = number
  default     = 1
}

variable "max_instances" {
  description = "Maximal number of instances"
  type        = number
  default     = 3
}
