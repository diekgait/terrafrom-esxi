vm_dict = {
    "dc1": {
        "template": "windows_2022_template",
        "playbook": "domaincontroller.yml"
    },
	"print1": {
        "template": "windows_2022_template",
        "playbook": "printserver.yml"
    },
	"kms1": {
        "template": "windows_2022_template",
        "playbook": "kmsserver.yml"
    },
	"web1": {
        "template": "alma_9_template",
        "playbook": "webserver.yml"
    },
	"web2": {
        "template": "alma_9_template",
        "playbook": "webserver.yml"
    },
	"web3": {
        "template": "alma_9_template",
        "playbook": "webserver.yml"
    }
}
terraform_config = ''
for vm_name, config in vm_dict.items():
    template = config.get("template") 
    playbook = config.get("playbook")
    terraform_config += f'''
resource "esxi_guest" "{vm_name}" {{
  guest_name         = "{vm_name}"
  disk_store         = "datastore1"
  boot_firmware      = "efi"
  clone_from_vm      = "{template}"

  network_interfaces {{
    virtual_network = "vlan8"
  }}
  power = "on"
}}
resource "null_resource" "ansible_provisioner_{vm_name}" {{
  # Zorgt ervoor dat Ansible draait na het aanmaken van de VM
  triggers = {{
    instance_ip = esxi_guest.{vm_name}.ip_address
  }}

  provisioner "local-exec" {{
    command = "ansible-playbook -u root -e 'ansible_ssh_pass=Welkom01! hostname_var=${{esxi_guest.{vm_name}.guest_name}}' -i '${{esxi_guest.{vm_name}.ip_address}},' ./playbooks/{playbook}"
  }}
}}
'''
print(terraform_config)