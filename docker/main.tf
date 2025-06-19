provider "aws" {
  region = var.region
}

resource "aws_instance" "elastic_stack" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.elastic_sg.id]

  user_data = templatefile("ec2-user-data.sh", {
    elastic_password       = var.elastic_password,
    kibana_password        = var.kibana_password,
    stack_version          = var.stack_version,
    cluster_name           = var.cluster_name,
    license                = var.license,
    encryption_key         = var.encryption_key,
    DOCKER_COMPOSE_VERSION  = var.docker_compose_version
  })

  root_block_device {
    volume_size = 30
  }

  tags = {
    Name = "ElasticStack-Secure"
  }
}

resource "aws_security_group" "elastic_sg" {
  name = "elasticstack-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9200
    to_port     = 9200
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5601
    to_port     = 5601
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
