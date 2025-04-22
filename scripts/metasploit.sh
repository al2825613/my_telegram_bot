#!/bin/bash
# Metasploit installation script for Termux

apt update
apt upgrade
apt install wget curl
wget https://github.com/rapid7/metasploit-framework/archive/refs/heads/master.zip
unzip master.zip
cd metasploit-framework-master
gem install bundler
bundle install
echo "Metasploit has been installed successfully!"
