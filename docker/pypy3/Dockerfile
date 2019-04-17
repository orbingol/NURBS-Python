# geomdl Dockerfile for PyPy3
FROM pypy:3-slim

USER root

RUN apt-get update -qq \
    && apt-get install -qq gcc g++ gfortran git pkg-config libfreetype6-dev libpng-dev libopenblas-dev \
    && apt-get clean

RUN useradd -ms /bin/bash nurbs

USER nurbs
WORKDIR /home/nurbs

RUN git clone https://github.com/orbingol/NURBS-Python.git library \
    && git clone https://github.com/orbingol/NURBS-Python_Examples.git examples \
    && git clone https://github.com/orbingol/geomdl-cli.git app \
    && git clone https://github.com/orbingol/geomdl-shapes.git shapes

ENV PATH="/home/nurbs/.local/bin:${PATH}"

WORKDIR /home/nurbs/library

RUN pypy3 -m ensurepip

RUN pypy3 -m pip install --user --no-cache-dir -r requirements.txt \
    && pypy3 -m pip install --user --no-cache-dir tornado

RUN pypy3 setup.py bdist_wheel \
    && pypy3 -m pip install --user dist/* \
    && pypy3 setup.py clean --all

WORKDIR /home/nurbs/app

RUN pypy3 -m pip install --user --no-cache-dir -r requirements.txt

RUN pypy3 -m pip install --user --no-cache-dir .

WORKDIR /home/nurbs/shapes

RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir .

WORKDIR /home/nurbs

RUN pypy3 -c "import geomdl; import geomdl.cli; import geomdl.shapes"

COPY --chown=nurbs:nurbs matplotlibrc .config/matplotlib/matplotlibrc
COPY --chown=nurbs:nurbs README.md .

RUN echo "cat README.md" >> .bashrc

ENTRYPOINT ["/bin/bash", "-i"]

EXPOSE 8000
