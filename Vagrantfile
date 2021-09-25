# set up the default terminal
ENV["TERM"]="linux"

# After running vagrant up then install apparmor-parser
# vagrant ssh
# sudo zypper install apparmor-parser

Vagrant.configure("2") do |config|

  # set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  ## Set the image version
  # config.vm.box_version = "15.2.31.212"

  # st the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  config.vm.network "forwarded_port", guest: 6443, host: 9443

  # consifure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end

