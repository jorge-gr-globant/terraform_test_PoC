# -*- mode: ruby -*-
# vi: set ft=ruby :

aws_region = ENV['AWS_DEFAULT_REGION']
aws_access_key_id = ENV['AWS_ACCESS_KEY_ID']
aws_secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
username = "#{ENV['USERNAME'] || `whoami`}"
kms_key_id = ENV['AWS_KMS_KEY_ID']


$set_environment_variables = <<SCRIPT
tee "/etc/profile.d/myvars.sh" > "/dev/null" <<EOF
# Ansible environment variables.
export ANSIBLE_STDOUT_CALLBACK=debug

# AWS environment variables.
export AWS_DEFAULT_REGION=#{ENV['AWS_DEFAULT_REGION']}
export AWS_REGION=#{ENV['AWS_REGION']}
export AWS_ACCESS_KEY_ID=#{ENV['AWS_ACCESS_KEY_ID']}
export AWS_SECRET_ACCESS_KEY=#{ENV['AWS_SECRET_ACCESS_KEY']}
EOF
SCRIPT

SERVER_IMAGE = "centos/7"
CLIENT_IMAGE = "centos/7"
SERVER_HOSTNAME = "consul-server"
SERVER_COUNT = 2
CONSUL_1_IP='10.140.0.70'
CONSUL_2_IP='10.140.0.71'
VAULT_IP='10.140.0.60'
Vagrant.configure("2") do |config|
  # Configure consul server 1
  config.vm.define "consul_1" do |server|
    # Load env variables
    server.vm.provision "shell", inline: $set_environment_variables, run: "always"
    server.vm.box = SERVER_IMAGE
    server.vm.hostname = "consul-1"
    server.vm.network "private_network", ip: CONSUL_1_IP
    server.vm.network "public_network", ip: "192.168.0.17"
    server.vm.network :forwarded_port, guest: 8500, host: 8500
    server.vbguest.auto_update = false
    server.vbguest.no_remote = true
    server.vm.provision "ansible" do |ansible|
    ansible.playbook = "./ansible/server.yml"
    ansible.limit = "consul_1,localhost"
    ansible.verbose = true
    ansible.extra_vars = {
      consul_leader_addr: CONSUL_1_IP,
      consul_advertise_addr: CONSUL_1_IP,
      consul_expected_servers: SERVER_COUNT,
      # AWS ENV Vars
      aws_region: aws_region,
      aws_access_key_id: aws_access_key_id,
      aws_secret_access_key: aws_secret_access_key,
      aws_host_user: username
    }
    end
    server.vm.provider "virtualbox" do |v|
      v.memory = 512
      v.name = "consul-1"
    end
  end
  # Configure consul 2
  config.vm.define "consul_2" do |server|
    # Load env variables
    server.vm.provision "shell", inline: $set_environment_variables, run: "always"
    server.vm.box = SERVER_IMAGE
    server.vm.hostname = "consul-2"
    server.vm.network "private_network", ip: CONSUL_2_IP
    server.vbguest.auto_update = false
    server.vbguest.no_remote = true
    server.vm.provision "ansible" do |ansible|
    ansible.playbook = "./ansible/server.yml"
    ansible.limit = "consul_2,localhost"
    ansible.verbose = true
    ansible.extra_vars = {
      consul_leader_addr: CONSUL_1_IP,
      consul_advertise_addr: CONSUL_2_IP,
      consul_expected_servers: SERVER_COUNT,
      # AWS ENV Vars
      aws_region: aws_region,
      aws_access_key_id: aws_access_key_id,
      aws_secret_access_key: aws_secret_access_key,
      aws_host_user: username
    }
  end
  server.vm.provider "virtualbox" do |v|
    v.memory = 512
    v.name = "consul-2"
  end
end

  #### VAULT ####
  #config.vm.define "vault" do |vault|
    #vault.vm.box = SERVER_IMAGE
    #vault.vm.hostname = "vault"
    #vault.vm.network "private_network", ip: VAULT_IP
    #vault.vbguest.auto_update = false
    #vault.vbguest.no_remote = true
    #vault.vm.provision "ansible" do |ansible|
      #ansible.playbook = "./ansible/vault.yml"
      #ansible.verbose = true
      #ansible.extra_vars = {
        #consul_address: SERVER_IP,
        ## AWS ENV Vars
        #aws_region: aws_region,
        #access_key_id: aws_access_key_id,
        #secret_access_key: aws_secret_access_key,
        #AWS_HOST_USER: username,
        #kms_key_id: kms_key_id
      #}
    #end
  #end
end

