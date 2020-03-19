# -*- mode: ruby -*-
# vi: set ft=ruby :

aws_region = ENV['AWS_DEFAULT_REGION']
aws_access_key_id = ENV['AWS_ACCESS_KEY_ID']
aws_secret_access_key = ENV['AWS_SECRET_ACCESS_KEY']
username = "#{ENV['USERNAME'] || `whoami`}"

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
SERVER_IP='10.140.0.70'
VAULT_IP='10.140.0.60'
CLIENT_COUNT = 1
SERVER_COUNT = 1
Vagrant.configure("2") do |config|
  # Configure consul servers
  (1..SERVER_COUNT).each do |i|
    config.vm.define "server" do |server|
      # Load env variables
      server.vm.provision "shell", inline: $set_environment_variables, run: "always"
      server.vm.box = SERVER_IMAGE
      #server.vm.box_url = "http://cloud.centos.org/centos/8/x86_64/images/CentOS-8-Vagrant-8.1.1911-20200113.3.x86_64.vagrant-virtualbox.box"
      server.vm.hostname = SERVER_HOSTNAME
      if i == 1
        server.vm.network "private_network", ip: SERVER_IP
        server.vm.network "public_network", ip: "192.168.0.17"
        server.vm.network :forwarded_port, guest: 8500, host: 8500
        server.vm.provision "ansible" do |ansible|
          ansible.playbook = "./ansible/server.yml"
          ansible.limit = "all,localhost"
          ansible.verbose = true
          ansible.extra_vars = {
            consul_leader_addr: SERVER_IP,
            consul_advertise_addr: SERVER_IP,
            consul_expected_servers: SERVER_COUNT,
            # AWS ENV Vars
            AWS_REGION: aws_region,
            AWS_ACCESS_KEY_ID: aws_access_key_id,
            AWS_SECRET_ACCESS_KEY: aws_secret_access_key,
            AWS_HOST_USER: username
          }
        end
      else
        server.vm.provision "ansible" do |ansible|
          ansible.limit = "all,localhost"
          ansible.playbook = "./ansible/server.yml"
          ansible.verbose = true
          ansible.limit = "vault"
          ansible.extra_vars = {
            consul_leader_addr: "SERVER_IP#{i - 1}",
            consul_advertise_addr: SERVER_IP,
            consul_expected_servers: SERVER_COUNT,
            # AWS ENV Vars
            AWS_REGION: aws_region,
            AWS_ACCESS_KEY_ID: aws_access_key_id,
            AWS_SECRET_ACCESS_KEY: aws_secret_access_key,
            AWS_HOST_USER: username
          }
        end
        server.vbguest.auto_update = false
        server.vbguest.no_remote = true
      end
      server.vm.provider "virtualbox" do |v|
        v.memory = 512
        v.name = "SERVER_HOSTNAME#{i}"
      end

    end
  end


  #### VAULT ####
  config.vm.define "vault" do |vault|
    vault.vm.box = SERVER_IMAGE
    vault.vm.hostname = "vault"
    vault.vm.network "private_network", ip: VAULT_IP
    vault.vbguest.auto_update = false
    vault.vbguest.no_remote = true
    vault.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/vault.yml"
      ansible.verbose = true
      ansible.extra_vars = {
        consul_address: SERVER_IP,
        # AWS ENV Vars
        aws_region: aws_region,
        access_key_id: aws_access_key_id,
        secret_access_key: aws_secret_access_key,
        AWS_HOST_USER: username
      }
    end
  end

    #Configure workers
  #(1..CLIENT_COUNT).each do |i|
    #config.vm.define "consul_client_#{i}" do |node|
      #node.vm.box = CLIENT_IMAGE
      #node.vm.network "private_network", ip: "10.140.0.7#{i}"
      #node.vm.provider "virtualbox" do |v|
        #v.name = "consul_client#{i}"
      #end

      #node.vbguest.auto_update = false
      #node.vbguest.no_remote = true

      #node.vm.provision "ansible" do |ansible|
        #ansible.playbook = "./ansible/client.yml"
        #ansible.extra_vars = {
          #CONSUL_SERVER: SERVER_IP
          #CONSUL_CURR_CLIENT: 
        #}
      #end
    #end
  #end
end

