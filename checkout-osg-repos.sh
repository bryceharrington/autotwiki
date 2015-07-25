#!/bin/bash

cd /var/cache/autotwiki/repositories

clone() {
    repo=$1
    dest=$2

    if [ -z "$dest" ]; then
	dest=$(basename $repo)
    fi

    if [ -e $dest ]; then
	echo "$dest exists"
	return 1
    fi
    echo "$dest <-- $repo"
    git clone $repo $dest
    echo
    return 0
}

for repo in gstreamer \
gst-plugins-base \
gst-plugins-good \
gst-plugins-bad \
gst-plugins-ugly \
gst-libav \
gst-rtsp-server \
gst-editing-services \
; do 
    clone git://anongit.freedesktop.org/gstreamer/$pkg $pkg
done

clone git://source.ffmpeg.org/ffmpeg.git ffmpeg

clone http://llvm.org/git/llvm.git llvm
clone http://llvm.org/git/clang.git clang
