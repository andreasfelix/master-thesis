FROM continuumio/miniconda3
WORKDIR /thesis

# TODO: add rsvg-convert
RUN conda config --add channels conda-forge && \
    conda install -y make pandoc=2.9.1.1 pandoc-crossref=0.3.6.1.2 livereload

CMD livereload --host 0.0.0.0 -p 8080 _dist
