provider "aws" {
  region = local.cfg["region"]
}

provider "aws" {
  alias  = "transit"
  region = "us-west-2"
}
