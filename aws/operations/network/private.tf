resource "aws_subnet" "private" {
  count             = length(data.aws_availability_zones.available.names)
  vpc_id            = aws_vpc.main.id
  availability_zone = element(data.aws_availability_zones.available.names, count.index)

  cidr_block = cidrsubnet(
    signum(length(aws_vpc.main.cidr_block)) == 1 ? aws_vpc.main.cidr_block : aws_vpc.main.cidr_block,
    ceil(log(local.private_subnet_count * 2, 2)),
    count.index
  )

  map_public_ip_on_launch = false

  tags = {
    Role    = "Private"
    Owner   = var.owner
    Project = var.project_name
    EnvName = terraform.workspace
  }
}

resource "aws_route_table" "private" {
  # count  = length(data.aws_availability_zones.available.names)
  vpc_id = aws_vpc.main.id

  tags = {
    Name    = "Private"
    Role    = "Private"
    Owner   = "Operations"
    Project = "Network"
    EnvName = terraform.workspace
  }

}

resource "aws_route_table_association" "private" {
  count = length(data.aws_availability_zones.available.names)

  subnet_id      = element(aws_subnet.private.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

