#!/usr/bin/env bash
url='http://127.0.0.1:8080/health'
if ! body=$(curl -fsS --noproxy '*' \
    --connect-timeout 2 --max-time 5 \
    --write-out '\n%{http_code}' "$url"); then
  printf 'Request failed: %s\n' "$url" >&2
  exit 1
fi
if [ "$body" != $'ok\n\n200' ]; then
  printf 'Unexpected response: %s\n' "$body" >&2
  exit 1
fi
printf '%s\n' 'healthy'
