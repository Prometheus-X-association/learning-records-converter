resource "aws_apprunner_service" "lrc" {
  count = var.deploy_to_aws ? 1 : 0

  service_name = local.service_name

  source_configuration {
    image_repository {
      image_configuration {
        port = tostring(var.port)

        runtime_environment_variables = local.base_env_vars
      }

      image_identifier      = var.docker_image
      image_repository_type = "ECR_PUBLIC"
    }

    auto_deployments_enabled = false
  }

  instance_configuration {
    cpu    = "${var.cpu_limit / 1000} vCPU"
    memory = "${var.memory_limit / 1024} GB"
  }

  health_check_configuration {
    healthy_threshold   = 1
    interval            = 10
    path                = "/health"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 5
  }

  tags = {
    Name        = local.service_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_apprunner_auto_scaling_configuration_version" "lrc_scaling" {
  auto_scaling_configuration_name = "${local.service_name}-scaling"

  min_size        = var.min_instances
  max_size        = var.max_instances
}
