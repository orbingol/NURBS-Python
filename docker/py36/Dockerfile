# geomdl Dockerfile for Python v3.6
FROM python:3.6-slim

USER root

RUN apt-get update -q -y \
    && apt-get install -q -y gcc git \
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

RUN pip install --user --no-cache-dir -r requirements.txt \
    && pip install --user --no-cache-dir tornado

RUN python setup.py bdist_wheel --use-cython \
    && pip install --user dist/* \
    && python setup.py clean --all

WORKDIR /home/nurbs/app

RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir .

WORKDIR /home/nurbs/shapes

RUN pip install --user --no-cache-dir -r requirements.txt

RUN pip install --user --no-cache-dir .

WORKDIR /home/nurbs

RUN python -c "import geomdl; import geomdl.core; import geomdl.cli; import geomdl.shapes"

COPY --chown=nurbs:nurbs matplotlibrc .config/matplotlib/matplotlibrc
COPY --chown=nurbs:nurbs README.md .

RUN echo "cat README.md" >> .bashrc

ENTRYPOINT ["/bin/bash", "-i"]

EXPOSE 8000
