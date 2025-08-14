output "scaleway_url" {
  description = "URL Scaleway Container"
  value       = var.deploy_to_scaleway ? "https://${scaleway_container.lrc[0].domain_name}" : null
}

output "aws_url" {
  description = "URL AWS App Runner"
  value       = var.deploy_to_aws ? "https://${aws_apprunner_service.lrc[0].service_url}" : null
}

output "summary" {
  description = "Deployments infos"
  value = {
    environment = var.environment
    scaleway    = var.deploy_to_scaleway ? "https://${scaleway_container.lrc[0].domain_name}" : "not deployed"
    aws         = var.deploy_to_aws ? "https://${aws_apprunner_service.lrc[0].service_url}" : "not deployed"
  }
}
