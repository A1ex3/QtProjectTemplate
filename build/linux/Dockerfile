FROM ubuntu:22.04

USER root
ENV USER=root

RUN useradd -m -s /bin/bash user

WORKDIR /home/user/project/
COPY . /home/user/project/

RUN ./build/linux/ubuntu/prepare.sh
RUN python3 configure.py

RUN cd /tmp \
    && git clone -b continuous https://github.com/probonopd/linuxdeployqt.git \
    && cd linuxdeployqt \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_PREFIX_PATH="/usr/lib/Qt/6.10.0/lib/cmake/Qt6" ../ \
    && cmake --build . --parallel \
    && cp tools/linuxdeployqt/linuxdeployqt /usr/local/bin \
    && cd /tmp \
    && rm -rf linuxdeployqt/

RUN cd /tmp \
    && git clone -b continuous https://github.com/AppImage/appimagetool.git \
    && cd appimagetool \
    && cmake -B build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build --target appimagetool --parallel \
    && cp build/src/appimagetool /usr/local/bin \
    && cd /tmp \
    && rm -rf appimagetool/

USER user
ENV USER=user

CMD [ "bash", "-c", "source /etc/profile && cmake -B out -G Ninja . && cmake --build out --config Release" ]