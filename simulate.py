#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import profile
import sys

from gittip.testing.client import TestClient


def main(path, run_through_profiler):
    client = TestClient()
    if run_through_profiler:
        profiler = profile.Profile()
        profiler.runcall(client.get, path)
        profiler.print_stats(sort=2)
    else:
        print(client.get(path).body)


if __name__ == '__main__':

    if '-x' in sys.argv:
        run_through_profiler = False
        sys.argv.remove('-x')
    else:
        run_through_profiler = True

    if len(sys.argv) > 1:
        path = sys.argv[2]
    else:
        path = '/'

    main(path, run_through_profiler)
