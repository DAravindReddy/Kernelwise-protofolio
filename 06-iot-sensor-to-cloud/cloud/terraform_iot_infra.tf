# Terraform AWS IoT Infrastructure for Kernelwise Connected Fleet
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

# 1. DynamoDB Table for Time-Series Telemetry
resource "aws_dynamodb_table" "telemetry_table" {
  name         = "kernelwise_device_telemetry"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "device_id"
  range_key    = "timestamp"

  attribute {
    name = "device_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  ttl {
    attribute_name = "ttl_expiration"
    enabled        = true
  }

  tags = {
    Environment = "Production"
    ManagedBy   = "KernelwiseLabs"
  }
}

# 2. AWS IoT Topic Rule
resource "aws_iot_topic_rule" "telemetry_rule" {
  name        = "KernelwiseTelemetryRule"
  description = "Routes device telemetry to DynamoDB"
  enabled     = true
  sql         = "SELECT *, topic(3) as device_id FROM 'kernelwise/devices/+/telemetry'"
  sql_version = "2016-03-23"

  dynamodbv2 {
    role_arn = aws_iam_role.iot_dynamodb_role.arn
    put_item {
      table_name = aws_dynamodb_table.telemetry_table.name
    }
  }
}

# 3. IAM Role for AWS IoT Core
resource "aws_iam_role" "iot_dynamodb_role" {
  name = "KernelwiseIoTDynamoDBRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "iot.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "iot_dynamodb_policy" {
  name = "KernelwiseIoTDynamoDBPolicy"
  role = aws_iam_role.iot_dynamodb_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:UpdateItem"
      ]
      Resource = aws_dynamodb_table.telemetry_table.arn
    }]
  })
}
