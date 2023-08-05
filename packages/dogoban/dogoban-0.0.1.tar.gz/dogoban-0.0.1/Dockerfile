FROM barnabyshearer/dockerfromscratch:10.1-python AS latest
COPY dogoban /usr/lib/python3.8/site-packages/dogoban
USER nobody
COPY *.txt /levels/
ENTRYPOINT ["python3", "-m", "dogoban"]
CMD ["/levels/level001.txt"]
