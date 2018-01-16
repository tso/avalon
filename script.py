import os
import sys

from django.utils.crypto import get_random_string


def main():
    args = sys.argv[1:]
    if not args:
        return

    if args.pop() == 'generate_secret_key':
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(100, chars)
        with open(os.path.join('avalon', 'settings', 'secret_key.py'), 'w+') as secret_file:
            secret_file.write(f'SECRET_KEY = \'{secret_key}\'\n')


if __name__ == '__main__':
    main()
