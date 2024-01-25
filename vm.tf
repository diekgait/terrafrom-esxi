resource "esxi_guest" "web3" {
  guest_name         = "web3"
  disk_store         = "datastore1"
  boot_firmware      = "efi"
  clone_from_vm      = "alma_9_template"

  network_interfaces {
    virtual_network = "vlan8"
  }
  power = "on"
}
resource "null_resource" "ansible_provisioner_web3" {
  # Zorgt ervoor dat Ansible draait na het aanmaken van de VM
  triggers = {
    instance_ip = esxi_guest.web3.ip_address
  }

  provisioner "local-exec" {
    command = "ansible-playbook -u root -e 'ansible_ssh_pass=Welkom01! hostname_var=${esxi_guest.web3.guest_name}' -i '${esxi_guest.web3.ip_address},' ./playbooks/webserver.yml"
  }
}

