output "elasticsearch_url" {
  value = "https://${aws_instance.elastic_stack.public_ip}:9200"
}

output "kibana_url" {
  value = "http://${aws_instance.elastic_stack.public_ip}:5601"
}

output "instance_ip" {
  value = aws_instance.elastic_stack.public_ip
}
