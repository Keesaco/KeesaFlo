wget -O devserver.zip https://commondatastorage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.2.zip
apt-get update
apt-get install -y zip
apt-get install -y unzip
apt-get install -y python-dev
unzip -qq devserver.zip
apt-get install -y python-setuptools
apt-get install -y python-pip
pip install pycrypto
cp /vagrant/vagrant-files/startserver.sh /home/vagrant/start.sh
chmod 777 /home/vagrant/start.sh