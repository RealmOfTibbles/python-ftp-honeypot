FROM ubuntu:latest

RUN mkdir -p /opt/logs
RUN mkdir -p /opt/code

RUN apt-get update && apt-get install python3 -y

COPY ftp-honeypot.py /opt/code/ftp-honeypot.py
COPY server.conf /opt/code/server.conf
COPY users.conf /opt/code/users.conf


# dont use port 21 on root, dont be an idiot
# you can use iptables or ufw to redirct port 42069 to port 21 instead

# or use dockers networking tools to port forward
Expose 42069

ENTRYPOINT ["bash"]
CMD ["-c","python3 /opt/code/ftp-honeypot.py"]
