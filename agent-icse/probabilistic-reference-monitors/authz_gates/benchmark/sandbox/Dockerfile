# Disposable victim environment for checking what each corpus command actually does.
# Built once (with network); every probe then runs in a fresh container with no network:
# outbound HTTP(S) to the call's own hosts reaches only the in-container capture server.
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        git python3 python3-pip python3-venv rsync curl wget ca-certificates openssl sudo findutils \
        procps e2fsprogs util-linux mariadb-server mariadb-client nodejs npm \
    && rm -rf /var/lib/apt/lists/*
# Standard developer tools an attack command may call (BLIND_PROTOCOL.md amendment 1): without
# them a command fails for want of the tool, which says nothing about the attack.
RUN apt-get update && apt-get install -y --no-install-recommends \
        zip unzip cron at binutils gcc libc6-dev ed openssh-client \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --break-system-packages requests setuptools certifi urllib3 wheel
# The project's own virtualenv, first on PATH, as in a typical dev checkout.
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install -q requests setuptools certifi urllib3 wheel
# Sandbox-only CA, trusted system-wide, so the capture server can answer HTTPS for any host.
RUN mkdir -p /opt/sandbox/ca && cd /opt/sandbox/ca \
    && openssl req -x509 -newkey rsa:2048 -nodes -days 3650 -subj "/CN=PRM sandbox CA" \
         -keyout ca.key -out ca.pem 2>/dev/null \
    && cp ca.pem /usr/local/share/ca-certificates/prm-sandbox.crt && update-ca-certificates >/dev/null
ENV NODE_EXTRA_CA_CERTS=/opt/sandbox/ca/ca.pem
COPY fixture.sh probe.py capture.py /opt/sandbox/
RUN sh /opt/sandbox/fixture.sh
WORKDIR /work
