#!/bin/sh
set -x
set -e

sudo apt-get update && sudo apt-get upgrade

# Re-configure soundcard
sudo install pulseaudio





# Notes:
# This is how I was able to get a working kivy + ffpyplayer on my Rpi 3 (I can launch a mp4 video, at least)
# 
# This script was not ran on a fresh distribution, so details might change.
# It was mainly copied from https://github.com/matham/ffpyplayer/blob/master/.travis.yml#L20
# Other steps required: Increasing the GPU memory (see https://github.com/kivy/kivy/issues/4662)


#sudo apt-get update;
#sudo apt-get -y install libegl1-mesa-dev libgles2-mesa-dev;
#sudo apt-get -y install libsdl2-dev libsdl2-mixer-dev python-dev;
#sudo pip install --upgrade cython

mkdir -p /tmp/ffmpeg_sources;
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/tmp/ffmpeg_build/lib;

sudo apt-get -y install yasm nasm libx264-dev libmp3lame-dev libass-dev libfreetype6-dev


cd /tmp/ffmpeg_sources;
wget http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz;
tar xzf yasm-1.3.0.tar.gz;
cd yasm-1.3.0;
./configure --prefix="/usr/local" --bindir="/usr/local/bin";
make -j4;
make install;
make distclean;

cd /tmp/ffmpeg_sources;
wget http://www.nasm.us/pub/nasm/releasebuilds/2.13.01/nasm-2.13.01.tar.xz;
tar xf nasm-2.13.01.tar.xz;
cd nasm-2.13.01;
./configure --prefix="/usr/local" --bindir="/usr/local/bin";
make -j4;
make install;
make distclean;

cd /tmp/ffmpeg_sources;
wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2;
tar xjf last_x264.tar.bz2;
cd x264-snapshot*;
PATH="/usr/local/bin:$PATH" ./configure --prefix="/usr/local" --bindir="/usr/local/bin" --enable-shared --extra-cflags="-fPIC";
PATH="/usr/local/bin:$PATH" make -j4;
make install;
make distclean;

cd /tmp/ffmpeg_sources;
wget http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz;
tar xzf lame-3.99.5.tar.gz;
cd lame-3.99.5;
./configure --prefix="/usr/local" --enable-nasm --enable-shared;
make -j4;
make install;
make distclean;

cd /tmp/ffmpeg_sources;
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2;
tar xjf ffmpeg-snapshot.tar.bz2;
cd ffmpeg;
#PATH="$HOME/ffmpeg_build/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --extra-cflags="-I$HOME/ffmpeg_build/include -fPIC" --extra-ldflags="-L$HOME/ffmpeg_build/lib" --bindir="$HOME/ffmpeg_build/bin" --enable-gpl --enable-libass --enable-libfreetype --enable-libmp3lame --enable-libtheora --enable-libvorbis --enable-libx264 --enable-shared;
PATH="/usr/local/bin:$PATH" PKG_CONFIG_PATH="/usr/local/lib/pkgconfig" ./configure --prefix="/usr/local" --extra-cflags="-I/usr/local/include -fPIC" --extra-ldflags="-L/usr/local/lib" --bindir="/usr/local/bin" --enable-gpl --enable-libass --enable-libfreetype --enable-libmp3lame --enable-libx264 --enable-shared;
PATH="/usr/local/bin:$PATH" make -j4;
make install;
make distclean;
hash -r;

export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
pip3 install https://github.com/matham/ffpyplayer/archive/master.zip
echo "Add 'export LD_LIBRARY_PATH=/usr/local/lib/:\$LD_LIBRARY_PATH' to your env"


