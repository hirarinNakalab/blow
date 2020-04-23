import os

if __name__ == '__main__':
    dirs = "dat fig original" \
           " res res/blow res/blow/audio submit".split()

    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)