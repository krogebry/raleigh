data "aws_availability_zones" "available" {
}

variable "project_name" {
  default = "Operations"
}

variable "owner" {
  default = "ops@edos.com"
}

locals {
  transit_config = {
    cidr                = "10.128.0.0/16"
    peer_region         = "us-west-2"
    peer_route_table_id = "rtb-b5e31fd3"
  }

  public_subnet_count  = length(data.aws_availability_zones.available.names)
  private_subnet_count = length(data.aws_availability_zones.available.names)

  operations_config_map = {

    "production" = {
      "region" = "us-east-1"
      "network" = {
        "cidr" = "172.100.0.0/16"
      }
      "aws_account" = "renovo-main"
    }

    "demo" = {
      "region" = "us-west-2"
      "network" = {
        "cidr" = "172.103.0.0/16"
      }
    }

    "dr" = {
      "region" = "us-east-2"
      "network" = {
        "cidr" = "172.102.0.0/16"
      }
    }

    "default" = {
      "region" = "us-west-2"
      "network" = {
        "cidr" = "172.101.0.0/16"
      }
    }

  }
}

locals {
  cfg = local.operations_config_map[terraform.workspace]
}

//data "aws_vpc" "transit_hub" {
//  provider = aws.transit
//  filter {
//    name = "tag:Name"
//    values = [
//    "TransitHub"]
//  }
//}

//data "aws_subnet_ids" "office" {
//  provider = aws.transit
//  vpc_id   = data.aws_vpc.transit_hub.id
//
//  filter {
//    name = "tag:Role"
//    values = [
//    "Transit"]
//  }
//}
