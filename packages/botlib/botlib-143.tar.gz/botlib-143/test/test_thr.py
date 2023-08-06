# This file is placed in the Public Domain.


import random
import unittest


from bot.obj import Object
from bot.tbl import Table
from bot.thr import launch
from bot.utl import getmain


events = []


k = getmain("k")


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["server=localhost", ""]
param.dne = ["test4", ""]
param.rm = ["reddit", ""]
param.dpl = ["reddit title,summary,link", ""]
param.log = ["test1", ""]
param.flt = ["0", ""]
param.fnd = [
    "cfg",
    "log",
    "rss",
    "log txt==test",
    "cfg server==localhost",
    "rss rss==reddit",
]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]


class Test_Threaded(unittest.TestCase):
    def test_thrs(self):
        thrs = []
        nr = k.cfg.index or 1
        for x in range(nr):
            thr = launch(exec, name="task%s" % x)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()


def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res


def exec():
    k = getmain("k")
    c = k.first()
    cmds = list(Table.modnames)
    random.shuffle(cmds)
    for cmd in cmds:
        for ex in getattr(param, cmd, [""]):
            e = c.event(cmd + " " + ex)
            k.dispatch(e)
            events.append(e)
