import sys

from . import init
from . import gtg


if __name__ == '__main__':
    init.main()

    try:
        gtg.main()
    except KeyboardInterrupt:
        sys.exit(1)
