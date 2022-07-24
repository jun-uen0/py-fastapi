#!/bin/sh
set -e

# Ask the user to confirm running
read -p "Run FastAPI in local? (y/N):" yn
case "$yn" in [yY]*) ;; *) echo "exit" ; exit ;; esac

# Move to parent dir
cd $(dirname $0)
# Move to root dir
cd ../server

# Activate env_api/bin/
echo "env_api/bin/activate"
source env_api/bin/activate
echo "If you want to deactivate env_api/bin/"
echo "Just run command 'deactivate'"

# Run uvicorn
echo "uvicorn main:app --reload"
echo "uvicorn is running..."
uvicorn main:app --reload