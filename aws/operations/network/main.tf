resource "aws_vpc" "main" {
  cidr_block = local.cfg["network"]["cidr"]

  tags = {
    Name    = "main"
    Owner   = var.owner
    EnvName = terraform.workspace
    Project = var.project_name
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Owner   = var.owner
    EnvName = terraform.workspace
    Project = var.project_name
  }
}

resource "aws_eip" "nat" {
  vpc = true
  depends_on = [
  aws_internet_gateway.main]

  tags = {
    Owner   = var.owner
    EnvName = terraform.workspace
    Project = var.project_name
  }
}

resource "aws_nat_gateway" "main" {
  subnet_id     = aws_subnet.public[0].id
  allocation_id = aws_eip.nat.id

  depends_on = [
    aws_internet_gateway.main,
  aws_eip.nat]

  tags = {
    Owner   = var.owner
    EnvName = terraform.workspace
    Project = var.project_name
  }
}


