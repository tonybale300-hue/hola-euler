#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
  printf 'Usage: %s EXPECTED_VERSION\n' "$0" >&2
  exit 2
fi
expected="Hola Euler $1"
for attempt in {1..10}; do
  if body=$(curl -fsS --noproxy '*' \
      --connect-timeout 1 --max-time 2 \
      --write-out '\n%{http_code}' \
      http://127.0.0.1:8080/); then
    if [ "$body" = "$expected"$'\n\n200' ]; then
      printf 'Ready: %s\n' "$1"
      exit 0
    fi
  fi
  if [ "$attempt" -lt 10 ]; then sleep 1; fi
done
printf 'Not ready or wrong version: %s\n' "$1" >&2
exit 1
