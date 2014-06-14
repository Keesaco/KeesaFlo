wget -O devserver.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.6.zip
apt-get update
apt-get install -y zip
apt-get install -y unzip
apt-get install -y python-dev
apt-get install -y recode
unzip -qq devserver.zip
apt-get install -y python-setuptools
apt-get install -y python-pip
pip install pycrypto
cp /vagrant/vagrant-files/startserver.sh /home/vagrant/start.sh
chmod 744 /home/vagrant/start.sh
recode ibmpc..lat start.sh