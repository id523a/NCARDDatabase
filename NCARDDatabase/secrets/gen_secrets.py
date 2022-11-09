#!/usr/bin/env python3
import secrets
import os

def make_secret_file(path):
    if os.path.isfile(path):
        print(f"{path} already exists, skipping generation")
    else:
        with open(path, mode='w') as f:
            f.write(secrets.token_urlsafe(32))

make_secret_file("django_secret.txt")
make_secret_file("db_password.txt")
make_secret_file("admin_password.txt")
