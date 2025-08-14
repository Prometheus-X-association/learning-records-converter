locals {
  service_name = "${var.app_name}-${var.environment}"

  base_env_vars = merge(
    {
      ENVIRONMENT        = var.environment
      APP_INTERNAL_HOST  = "0.0.0.0"
      APP_INTERNAL_PORT  = tostring(var.port),

      # If you want to increase the number of workers for this service,
      # make sure to also increase the machine configuration (CPU and memory) accordingly.
      WORKERS_COUNT      = 2,
      THREADS_PER_WORKER = 2
    },
    var.log_level != null ? { LOG_LEVEL = var.log_level } : {}
  )
}
