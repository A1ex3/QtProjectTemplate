FROM ubuntu:22.04

WORKDIR /usr/qtproject/
COPY . /usr/qtproject/

RUN ./build/linux/ubuntu/prepare.sh
RUN python3 configure.py

RUN cd /tmp \
    && git clone -b continuous https://github.com/probonopd/linuxdeployqt.git \
    && cd linuxdeployqt \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_PREFIX_PATH="/usr/lib/Qt/6.8.1/lib/cmake/Qt6" ../ \
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

CMD [ "bash", "-c", "source /etc/profile && cmake -S . -B out -G Ninja && cmake --build out --config Release" ]