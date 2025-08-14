resource "scaleway_container_namespace" "lrc" {
  count = var.deploy_to_scaleway ? 1 : 0

  name   = local.service_name
  region = var.scaleway_region

  environment_variables = local.base_env_vars
}

resource "scaleway_container" "lrc" {
  count = var.deploy_to_scaleway ? 1 : 0

  namespace_id   = scaleway_container_namespace.lrc[0].id
  name           = local.service_name
  registry_image = var.docker_image

  port         = var.port
  memory_limit = var.memory_limit
  cpu_limit    = var.cpu_limit
  timeout      = var.timeout

  environment_variables = local.base_env_vars

  min_scale = var.min_instances
  max_scale = var.max_instances

  privacy = "public"
  deploy  = true
}
