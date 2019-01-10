# geomdl Dockerfile for PyPy3
FROM pypy:3

USER root
WORKDIR /nurbs

RUN apt-get update \
    && apt-get install -y gcc git \
    && apt-get clean

RUN git clone https://github.com/orbingol/NURBS-Python.git library \
    && git clone https://github.com/orbingol/NURBS-Python_Examples.git examples \
    && git clone https://github.com/orbingol/geomdl-cli.git app

WORKDIR /nurbs/library

RUN pypy3 -m ensurepip

RUN pypy3 -m pip install --no-cache-dir -r requirements.txt && pypy3 -m pip install --no-cache-dir tornado \
    && pypy3 setup.py bdist_wheel \
    && pypy3 -m pip install dist/* \
    && pypy3 setup.py clean --all \
    && pypy3 -c "import geomdl"

WORKDIR /nurbs/app

RUN pypy3 -m pip install --no-cache-dir -r requirements.txt \
    && pypy3 -m pip install --no-cache-dir . \
    && pypy3 -c "import geomdl.cli"

RUN useradd -ms /bin/bash nurbs \
    && chown -R nurbs:nurbs /nurbs

USER nurbs
WORKDIR /home/nurbs

COPY --chown=nurbs:nurbs matplotlibrc .config/matplotlib/matplotlibrc
COPY --chown=nurbs:nurbs README.md .

RUN echo "cat README.md" >> .bashrc

ENTRYPOINT ["/bin/bash", "-i"]

EXPOSE 8000
