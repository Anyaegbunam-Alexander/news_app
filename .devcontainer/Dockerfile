FROM dart

RUN apt-get update && \
    apt-get install -y curl git unzip xz-utils zip libglu1-mesa && \
    apt-get clean

RUN git clone https://github.com/flutter/flutter.git -b stable --depth 1 /flutter

ENV PATH="/flutter/bin:$PATH"

RUN flutter doctor

RUN apt install -y default-jdk && \
    apt install -y default-jre && \
    apt-get install -y libc6-dev-i386 lib32z1 && \
    apt-get install -y wget && \
    mkdir -p /flutter/bin/android-sdk && \
    wget -P /flutter/bin/android-sdk https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip && \
    unzip /flutter/bin/android-sdk/commandlinetools-linux-11076708_latest.zip -d /flutter/bin/android-sdk && \
    /flutter/bin/android-sdk/cmdline-tools/bin/sdkmanager --update --sdk_root=/flutter/bin/android-sdk && \
    /flutter/bin/android-sdk/cmdline-tools/bin/sdkmanager "platforms;android-25" "build-tools;25.0.2" "extras;google;m2repository" "extras;android;m2repository" --sdk_root=/flutter/bin/android-sdk && \
    yes | /flutter/bin/android-sdk/cmdline-tools/bin/sdkmanager --licenses --sdk_root=/flutter/bin/android-sdk

ENV ANDROID_SDK_ROOT=/flutter/bin/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/tools

RUN apt install -y python3 && \
    apt install -y python3.11-venv
