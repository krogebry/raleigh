resource "aws_subnet" "public" {
  count             = length(data.aws_availability_zones.available.names)
  vpc_id            = aws_vpc.main.id
  availability_zone = element(data.aws_availability_zones.available.names, count.index)

  cidr_block = cidrsubnet(
    aws_vpc.main.cidr_block,
    ceil(log(local.public_subnet_count * 2, 2)),
    local.public_subnet_count + count.index
  )

  map_public_ip_on_launch = true

  tags = {
    Role    = "Public"
    Owner   = var.owner
    Project = var.project_name
    EnvName = terraform.workspace
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = {
    Role    = "Public"
    Owner   = var.owner
    Project = var.project_name
    EnvName = terraform.workspace
  }
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}

resource "aws_route_table_association" "public" {
  count          = length(data.aws_availability_zones.available.names)
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

