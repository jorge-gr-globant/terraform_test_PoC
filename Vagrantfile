# -*- mode: ruby -*-
# vi: set ft=ruby :

SERVER_IMAGE = "centos/7"
CLIENT_IMAGE = "centos/7"
SERVER_HOSTNAME = "consul-server"
SERVER_IP='10.140.0.70'
CLIENT_COUNT = 1
Vagrant.configure("2") do |config|
  # Configure consul server
  config.vm.define "server" do |server|
    server.vm.box = SERVER_IMAGE
    #server.vm.box_url = "http://cloud.centos.org/centos/8/x86_64/images/CentOS-8-Vagrant-8.1.1911-20200113.3.x86_64.vagrant-virtualbox.box"
    server.vm.hostname = SERVER_HOSTNAME
    server.vm.network "private_network", ip: SERVER_IP
    server.vm.network "public_network", ip: "192.168.0.17"
    server.vm.network :forwarded_port, guest: 8500, host: 8500

    server.vbguest.auto_update = false
  	server.vbguest.no_remote = true
    #server.vm.provision :hosts do |provisioner|
      #provisioner.sync_hosts = true
      #provisioner.add_host SERVER_IP, ['consul_server']
    #end
    server.vm.provider "virtualbox" do |v|
      v.memory = 1024
      v.name = SERVER_HOSTNAME
    end

    server.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/server.yml"
    end
  end

   # Configure workers
  (1..CLIENT_COUNT).each do |i|
    config.vm.define "consul_client_#{i}" do |node|
      node.vm.box = CLIENT_IMAGE
      node.vm.network "private_network", ip: "10.140.0.7#{i}"
      #node.vm.provision :hosts do |provisioner|
        #provisioner.sync_hosts = true
        #provisioner.add_host "10.140.0.7#{i+1}", ["consul_client_#{i+1}"]
      #end
      node.vm.provider "virtualbox" do |v|
        v.name = "consul_client#{i}"
      end

      node.vbguest.auto_update = false
  		node.vbguest.no_remote = true

      node.vm.provision "ansible" do |ansible|
        ansible.playbook = "./ansible/client.yml"
      end
    end
  end
end

