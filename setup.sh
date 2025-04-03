#!/usr/bin/env bash

set -e
trap 'echo "Error on line $LINENO: $BASH_COMMAND"' ERR

echo "Starting Flask Backend..."
exec bash /TranslationApp/server/run.sh
