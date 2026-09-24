#!/usr/bin/env bash
# Explicitly read-only. No installs, account changes, service changes, or mounts.
set -u
show() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  result=$?
  printf '[exit=%s]\n' "$result"
}
show cat /etc/os-release
show uname -m
show uname -r
show id
show bash --version
show ps -p 1 -o comm=
show systemctl --version
show ip -brief address
show ip route
show ss -ltn
show lsblk -f
show findmnt /
show df -h .
show df -i .
for name in dnf rpm nmcli vim man less ssh java javac jar mvn curl tar; do
  show command -v "$name"
done
if command -v rpm >/dev/null 2>&1; then
  show rpm -q bash coreutils findutils grep util-linux systemd openssh-server
  show rpm -q vim-enhanced man-db java-21-openjdk-devel maven
fi
if command -v nmcli >/dev/null 2>&1; then
  show nmcli device status
  show nmcli connection show --active
fi
if command -v getenforce >/dev/null 2>&1; then show getenforce; fi
printf '\nRead-only environment inventory finished; this is not chapter execution evidence.\n'
