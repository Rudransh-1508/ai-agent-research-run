#!/bin/bash
# Robust S2 fetch with retry/backoff. Usage: s2get.sh <url> <outfile>
url="$1"; out="$2"
for attempt in 1 2 3 4 5 6 7 8; do
  curl -s "$url" -o "$out.tmp"
  if grep -q '"Too Many Requests"' "$out.tmp" || grep -q '"message": "Too Many' "$out.tmp"; then
    wait_s=$((attempt * 20))
    echo "rate-limited, sleeping ${wait_s}s (attempt $attempt) for $out" >&2
    sleep $wait_s
    continue
  fi
  if [ -s "$out.tmp" ] && head -c 1 "$out.tmp" | grep -q '{'; then
    mv "$out.tmp" "$out"
    echo "OK $out" >&2
    return 0 2>/dev/null || exit 0
  fi
  sleep 5
done
mv "$out.tmp" "$out"
echo "FAIL $out: $(head -c 150 "$out")" >&2
exit 1
