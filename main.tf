terraform {
  required_version = ">= 0.13"
  required_providers {
    esxi = {
      source = "registry.terraform.io/josenk/esxi"
    }
  }
}
provider "esxi" {
  esxi_hostname      = "10.4.0.36"
  esxi_hostport      = "22"
  esxi_hostssl       = "443"
  esxi_username      = "root"
  esxi_password      = "Welkom01!"
}