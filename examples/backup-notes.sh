#!/usr/bin/env bash
set -u
umask 077
root="$HOME/linux-lab"
source_dir="$root/notes"
backup_root="$root/backups"
if [ ! -d "$source_dir" ]; then
  printf 'Missing directory: %s\n' "$source_dir" >&2
  exit 1
fi
if ! mkdir -p -- "$backup_root"; then
  exit 1
fi
run_dir=$(mktemp -d "$backup_root/run.XXXXXXXX") || exit 1
archive="$run_dir/notes.tar.gz"
if ! tar -czf "$archive" -C "$source_dir" .; then
  printf 'Archive failed; inspect %s\n' "$run_dir" >&2
  exit 1
fi
if ! (
  cd "$run_dir" || exit 1
  sha256sum notes.tar.gz > notes.tar.gz.sha256 &&
    sha256sum -c notes.tar.gz.sha256
); then
  printf 'Checksum failed: %s\n' "$run_dir" >&2
  exit 1
fi
printf 'Backup ready: %s\n' "$run_dir"
