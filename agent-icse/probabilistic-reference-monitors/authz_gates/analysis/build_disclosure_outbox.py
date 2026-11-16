#!/usr/bin/env python3
"""Turn DISCLOSURE_DRAFTS.md into ready-to-send messages, one file per maintainer.

Writes to disclosure_outbox/ (gitignored: it holds maintainers' contact addresses). Each
file starts with To / Subject lines, then the body: a short introduction, that repo's
findings verbatim from the drafts, and the 14-day coordination window. Repos with no private
channel get a separate public issue text that asks for one and contains no details.

  python3 analysis/build_disclosure_outbox.py
Stdlib only.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "disclosure_outbox")

# repo -> (channel, address or None, draft heading prefix). Addresses are the ones the
# maintainers publish (SECURITY.md or public GitHub profile), looked up 2026-11-17.
TARGETS = {
    "eugeniughelbur/jev-engineering": ("email", "e.ghelbur@gmail.com", "## eugeniughelbur/jev-engineering"),
    "valentynkit/jev-belay": ("email", "valentynkit.work@pm.me", "## valentynkit/jev-belay"),
    "ismaelsoilet/jev-harness": ("email", "ismael.soilet@hotmail.com", "## ismaelsoilet/jev-harness"),
    "alelaguard/agentguards-plugins": ("email", "support@agentguards.co", "## alelaguard/agentguards-plugins"),
    "leepokai/jev-guard": ("ask-for-channel", None, "## leepokai/jev-guard"),
    "Dicklesworthstone/destructive_command_guard": ("ask-for-channel", None, "## Dicklesworthstone/destructive_command_guard"),
    "sdkks/example-claude-settings": ("ask-for-channel", None, "## sdkks/example-claude-settings"),
}

INTRO = ("Hi,\n\nI am researching authorization gates for AI coding agents (GitHub @Rudransh-1508). "
         "While measuring {repo} as a Claude Code hook, we found the issues below. Each was "
         "observed with our test harness; the commands are labelled by executing them in a "
         "disposable sandbox. I am reporting privately first.\n\n")
OUTRO = ("\n\nWe plan to describe these results in a research paper. We will not publish details "
         "for at least 14 days from this message, and are happy to coordinate on timing or "
         "credit. I can share the exact commands and the harness on request. Thank you for "
         "maintaining the project.\n\nRudransh\n")
ISSUE = ("Title: Request for a private channel to report a security issue\n\n"
         "Hi, I found a security-relevant issue in {repo} while researching authorization gates "
         "for AI coding agents, and would like to report it privately rather than in a public "
         "issue. Could you enable GitHub private vulnerability reporting for this repository "
         "(Settings > Code security > Private vulnerability reporting), or share an email "
         "address for security reports? Thank you.\n")


def sections(text):
    parts = re.split(r"(?m)^(?=## )", text)
    return {p.splitlines()[0]: p for p in parts if p.startswith("## ")}


def body_for(repo, heading, secs):
    sec = next(v for k, v in secs.items() if k.startswith(heading))
    findings = "\n".join(sec.splitlines()[1:]).strip()
    if repo == "valentynkit/jev-belay":  # the draft section is shared with limpet
        findings = re.sub(r"(?m)^- limpet:.*(\n  .*)*", "", findings).strip()
    return INTRO.format(repo=repo) + findings + OUTRO


def main():
    with open(os.path.join(ROOT, "DISCLOSURE_DRAFTS.md")) as f:
        secs = sections(f.read())
    os.makedirs(OUT, exist_ok=True)
    for repo, (channel, addr, heading) in TARGETS.items():
        name = repo.replace("/", "__")
        body = body_for(repo, heading, secs)
        if channel == "email":
            with open(os.path.join(OUT, f"{name}.email.txt"), "w") as f:
                f.write(f"To: {addr}\nSubject: Private security report: {repo}\n\n{body}")
        else:
            with open(os.path.join(OUT, f"{name}.1_public_issue.txt"), "w") as f:
                f.write(ISSUE.format(repo=repo))
            with open(os.path.join(OUT, f"{name}.2_private_report_after_reply.txt"), "w") as f:
                f.write(f"Send through the private channel the maintainer provides.\n"
                        f"Subject: Private security report: {repo}\n\n{body}")
        print(f"{repo}: {channel}")


if __name__ == "__main__":
    main()
