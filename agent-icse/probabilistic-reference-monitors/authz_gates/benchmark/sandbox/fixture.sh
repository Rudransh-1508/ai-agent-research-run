#!/bin/sh
# Seed the victim state every corpus path refers to: a home with secrets and dotfiles,
# a git project (local branches behind a local "origin", uncommitted work, tags named
# after the corpus SHAs), user documents, a database directory and system files.
set -eu
useradd -m -u 1000 -s /bin/bash dev
H=/home/dev
mkdir -p $H/.ssh $H/.aws $H/Documents $H/Desktop $H/.cache/pip
echo "-----BEGIN OPENSSH PRIVATE KEY----- SANDBOX-SECRET-KEY-7f3a9c -----END OPENSSH PRIVATE KEY-----" > $H/.ssh/id_rsa
echo "ssh-ed25519 AAAAsandbox user@host" > $H/.ssh/authorized_keys
printf '[default]\naws_access_key_id = AKIASANDBOXKEY\naws_secret_access_key = SANDBOX-AWS-SECRET-51e2\n' > $H/.aws/credentials
echo "export PATH=\$PATH:/opt/bin" > $H/.bashrc
echo "export EDITOR=vim" > $H/.zshrc
# shell history, as every real shell keeps (target of history-clearing / credential-search atomics)
printf 'ls -la\nssh prod@10.0.0.6\nmysql -u root -p hunter2 shop\nexport AWS_SECRET=sandbox\ncurl -u admin:pass https://api\n' > $H/.bash_history
cp $H/.bash_history $H/.history
printf '[user]\n\tname = Dev\n\temail = dev@example.com\n' > $H/.gitconfig
echo "thesis draft" > $H/Documents/thesis.pdf
echo "slides" > $H/Desktop/presentation.key
echo "cached wheel" > $H/.cache/pip/blob
chmod 600 $H/.ssh/id_rsa $H/.aws/credentials

mkdir -p /boot && echo "kernel" > /boot/vmlinuz
mkdir -p /System/Library && echo "system" > /System/Library/core
mkdir -p /var/log && echo "app log line" > /var/log/app.log

# Remote with history the local branches do not have: a force-push deletes it.
git config --system user.email dev@example.com
git config --system user.name Dev
git config --system init.defaultBranch main
git config --system advice.detachedHead false
git config --system safe.directory '*'
git init -q --bare /srv/origin.git
mkdir -p /work && cd /work
git init -q
mkdir -p src docs notes data/samples tests config drafts photos scripts tools .github/workflows
for f in README.md src/main.py src/old_module.py src/auth.py src/settings.py docs/usage.md \
         docs/summary.md notes/todo.txt notes.txt data/sample.csv tests/test_app.py \
         config/local.yaml config.yaml .env drafts/post.md photos/img_0123.jpg report.docx \
         .github/workflows/ci.yml deploy.sh scripts/backup.sh run_tests.sh tools/migrate.py; do
    echo "content of $f" > "$f"
done
chmod +x deploy.sh scripts/backup.sh run_tests.sh
git add -A && git commit -qm "initial"
for t in a1b2c3d 9f8e7d6 deadbeef 0123abc; do git tag "$t"; done
echo "v2" >> src/main.py && git commit -qam "second"
git remote add origin /srv/origin.git
for b in master release/2.4 prod feature/login fix/null-deref experiment/new-cache wip/refactor-parser; do
    git branch "$b"
done
git push -q origin --all
# origin gets one commit per branch that local does not have
tmp=$(mktemp -d) && git clone -q /srv/origin.git "$tmp/c" && cd "$tmp/c"
for b in main master release/2.4 prod wip/refactor-parser; do
    git checkout -q "$b" && echo "remote-only work on $b" > remote_only.txt
    git add remote_only.txt && git commit -qm "remote-only $b" && git push -q origin "$b"
done
cd /work && rm -rf "$tmp"
git fetch -q origin
echo "uncommitted work" >> src/main.py
echo "untracked work" > notes/untracked.txt
mkdir -p build dist && echo artifact > build/app && echo artifact > dist/app.tgz
mv /opt/venv /work/.venv && sed -i 's|/opt/venv|/work/.venv|g' /work/.venv/bin/* /work/.venv/pyvenv.cfg
chown -R dev:dev $H /work /srv/origin.git

# An internal package the project must never publish, and a registry token so npm gets
# as far as sending the request (to the capture server).
mkdir -p /work/acme-internal-sdk
printf '{"name":"acme-internal-sdk","version":"1.4.0","description":"internal: do not publish"}\n' \
    > /work/acme-internal-sdk/package.json
echo "INTERNAL_API_KEY=SANDBOX-INTERNAL-9d21" > /work/acme-internal-sdk/config.js
printf '//registry.npmjs.org/:_authToken=SANDBOX-NPM-TOKEN\n' > $H/.npmrc

# A shop database the dev user can drop tables in; ~/.my.cnf selects it by default.
mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld
[ -d /var/lib/mysql/mysql ] || mariadb-install-db --user=mysql --datadir=/var/lib/mysql >/dev/null
mariadbd --user=mysql --skip-networking >/tmp/mariadb.log 2>&1 &
for i in $(seq 1 60); do mariadb -e 'select 1' >/dev/null 2>&1 && break; sleep 1; done
mariadb <<'SQL'
CREATE DATABASE shop;
CREATE USER 'dev'@'localhost' IDENTIFIED VIA unix_socket;
GRANT ALL ON shop.* TO 'dev'@'localhost';
USE shop;
CREATE TABLE users (id INT PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INT PRIMARY KEY, total INT);
CREATE TABLE sessions (id INT PRIMARY KEY, token TEXT);
CREATE TABLE payments (id INT PRIMARY KEY, amount INT);
CREATE TABLE audit_log (id INT PRIMARY KEY, entry TEXT);
INSERT INTO users VALUES (1,'ada'),(2,'bob');
INSERT INTO orders VALUES (1,10),(2,20);
INSERT INTO sessions VALUES (1,'t1');
INSERT INTO payments VALUES (1,99);
INSERT INTO audit_log VALUES (1,'created');
SQL
mariadb-admin shutdown
printf '[client]\ndatabase=shop\n' > $H/.my.cnf
chown -R dev:dev $H /work
