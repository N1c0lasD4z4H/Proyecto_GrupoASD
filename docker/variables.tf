variable "region" {
  description = "Región de AWS"
  default     = "us-east-1"
}

variable "public_key_path" {
  type = string
}

variable "private_key_path" {
  type = string
}

variable "key_pair_name" {
  type = string
}

variable "elastic_password" {
  type        = string
  sensitive   = true
}

variable "kibana_password" {
  type        = string
  sensitive   = true
}

variable "encryption_key" {
  type        = string
  sensitive   = true
}

variable "stack_version" {
  default = "8.18.0"
}

variable "cluster_name" {
  default = "docker-cluster"
}

variable "license" {
  default = "basic"
}

variable "docker_compose_version" {
  default = "v2.27.0"
}

variable "ami_id" {
  description = "AMI de Amazon Linux 2"
  default     = "ami-0c02fb55956c7d316" # válida para us-east-1
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  default     = "t3.medium"
}

