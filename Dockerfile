# Run Chrome in a container
#
# docker run -it \
#	--net host \ # may as well YOLO
#	--cpuset-cpus 0 \ # control the cpu
#	--memory 512mb \ # max memory it can use
#	-v /tmp/.X11-unix:/tmp/.X11-unix \ # mount the X11 socket
#	-e DISPLAY=unix$DISPLAY \
#	-v $HOME/Downloads:/home/chrome/Downloads \
#	-v $HOME/.config/google-chrome/:/data \ # if you want to save state
#	--security-opt seccomp=$HOME/chrome.json \
#	--device /dev/snd \ # so we have sound
#	-v /dev/shm:/dev/shm \
#	--name planarRad \
#	dan/planarRad



# Base docker image
FROM marrabld/planarrad:0.1
LABEL maintainer "Daniel Marrable  <marrabld+planarrad@gmail.com>"

USER root

# ADD http://www.planarrad.com/downloads/planarrad_free_src_0.9.5beta_2015_07_17.tar.gz /src/planarrad_free_src_0.9.5beta_2015_07_17.tar.gz

# RUN tar xfvz /src/planarrad_free_src_0.9.5beta_2015_07_17.tar.gz -C /src

# Install planarrad dependencies
RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/marrabld/planarradpy.git

# RUN export JUDE2DIR=$HOME/jude2_install \
#        && export LD_LIBRARY_PATH=$JUDE2DIR/lib:$LD_LIBRARY_PATH \
#        && export PATH=$JUDE2DIR/bin:$PATH \
#	&& echo $JUDE2DIR

# Compile the source doce
# RUN     cd /src/planarrad_free_src_0.9.5beta_2015_07_17 \
#        && /src/planarrad_free_src_0.9.5beta_2015_07_17/example_build


# Cleanup
RUN apt-get purge --auto-remove -y curl \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /src/*.deb 

# Add chrome user
# RUN groupadd -r chrome && useradd -r -g chrome -G audio,video chrome \
#    && mkdir -p /home/chrome/Downloads && chown -R chrome:chrome /home/chrome

# COPY local.conf /etc/fonts/local.conf

# Run Chrome as non privileged user
# RUN useradd -s /bin/bash planarrad
# USER planarrad

# Autorun chrome
# ENTRYPOINT [ "planarradpy" ]
CMD [ "planarrad.run" ]