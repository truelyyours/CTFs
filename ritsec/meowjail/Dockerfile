FROM python:3.13-slim

RUN apt-get update && apt-get install -y socat nasm binutils git && rm -rf /var/lib/apt/lists/*

RUN FLAG_DIR=$(head /dev/urandom | tr -dc a-f0-9 | head -c16) && \
    mkdir -p /$FLAG_DIR && \
    echo "/$FLAG_DIR/flag.txt" > /flag_location && \
    chmod 555 /$FLAG_DIR

COPY flag.txt /tmp/flag.txt
RUN FLAG_DIR=$(cat /flag_location | xargs dirname) && \
    mv /tmp/flag.txt "$FLAG_DIR/flag.txt" && \
    chmod 444 "$FLAG_DIR/flag.txt" && \
    rm -f /flag_location

RUN useradd -m ctf

USER ctf
WORKDIR /chall

COPY --chown=ctf:ctf horror.patch .
RUN git clone https://github.com/redgoldlace/python-horror \
    && cd python-horror \
    && git checkout a670e0a5b75574b5ddbb42bfc82fcbde763025e8 \
    && git apply ../horror.patch
    
COPY --chown=ctf:ctf meow.py .
RUN pip install ./python-horror
RUN echo "import horror.register" > "$(python -m site --user-site)/horror.pth"

EXPOSE 1337

CMD socat -v TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 meow.py"