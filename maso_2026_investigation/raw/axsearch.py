import re, sys, html
data = open(sys.argv[1]).read()
# Each result: <li class="arxiv-result"> ... <p class="list-title is-inline-block"><a href="https://arxiv.org/abs/ID"> ... <p class="title is-5 mathjax">TITLE</p>
results = re.findall(r'<li class="arxiv-result">(.*?)</li>', data, re.S)
for r in results:
    m_id = re.search(r'arxiv.org/abs/([0-9]{4}\.[0-9]{4,5})', r)
    m_t = re.search(r'<p class="title is-5 mathjax">\s*(.*?)\s*</p>', r, re.S)
    m_d = re.search(r'<p class="is-size-7">\s*Submitted\s*(.*?)\s*;', r, re.S)
    if m_id and m_t:
        title = html.unescape(re.sub(r'\s+',' ', m_t.group(1))).strip()
        date = m_d.group(1).strip() if m_d else '?'
        print(f"{m_id.group(1)} | {date} | {title}")
