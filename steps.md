RUN apt install default-jdk
RUN apt install default-jre
RUN apt-get install libc6-dev-i386 lib32z1
RUN apt-get install wget
RUN cd /flutter/bin
RUN mkdir andriod-sdk
RUN cd andriod-sdk
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
RUN unzip commandlinetools-linux-11076708_latest.zip
RUN cmdline-tools/bin/sdkmanager --update --sdk_root=.
RUN cmdline-tools/bin/sdkmanager "platforms;android-25" "build-tools;25.0.2" "extras;google;m2repository" "extras;android;m2repository" --sdk_root=.
RUN cmdline-tools/bin/sdkmanager --licenses --sdk_root=.
RUN export ANDROID_SDK_ROOT=/flutter/bin/andriod-sdk
RUN export PATH=$PATH:$ANDROID_SDK_ROOT/tools
RUN source /etc/environment
RUN apt install python3
RUN apt install python3.11-venv