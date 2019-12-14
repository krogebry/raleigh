terraform {
  backend "s3" {
    key    = "environments/operations.tfstate"
    bucket = "edos-terraform-state"
    region = "us-east-1"
  }
}

