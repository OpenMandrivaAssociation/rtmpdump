rm -rf rtmpdump && git clone git://git.ffmpeg.org/rtmpdump && cd rtmpdump/
git archive --prefix=rtmpdump-$(date +%Y%m%d)/ --format=tar HEAD | xz > ../rtmpdump-$(date +%Y%m%d).tar.xz
