# centralised running script

from common.code.rr_utils import timestamp as T

import models

def run():
    print(f'Starting {T()}')

    print('Building db')

    print(f'Stopping {T()}')


if __name__ == '__main__':
    run()