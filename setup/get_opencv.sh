sudo apt-get purge wolfram-engine minecraft-pi -y
sudo apt-get autoremove -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgphoto2-dev libgtk2.0-dev tesseract-ocr libeigen3-dev libatlas-base-dev gfortran python2.7-dev python3-dev libtesseract-dev pylint 
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.1.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.1.zip
unzip opencv_contrib.zip
#rm *.zip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py
sudo pip3 install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip
printf "# virtualenv and virtualenvwrapper\n" >> ~/.profile
printf "export WORKON_HOME=$HOME/.virtualenvs\n" >> ~/.profile
printf "source /usr/local/bin/virtualenvwrapper.sh\n" >> ~/.profile
source ~/.profile
mkvirtualenv cv -p python3
source ~/.profile
workon cv
pip3 install numpy
cd ~/opencv-3.4.1/
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules -D BUILD_EXAMPLES=ON -D BUILD_opencv_python3=ON -D ENABLE_NEON=ON ..
sudo make -j3
sudo make install
sudo ldconfig
printf "/usr/local/lib\n\n" >> /etc/ld.so.conf.d/opencv.conf
sudo ldconfig
printf "PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig\n" >> ~/.bashrc
printf "export PKG_CONFIG_PATH\n" >> ~/.bash_rc

#fix python 3 name error
cd /usr/local/lib/python3.4/site-packages/
sudo mv cv2.cpython-34m.so cv2.so
cd ~/.virtualenvs/cv/lib/python3.4/site-packages/
ln -s /usr/local/lib/python3.4/site-packages/cv2.so cv2.so

#testing
cd
# rm -rf opencv-3.4.1 opencv_contrib-3.4.1 
sudo apt-get dist-upgrade
