
class HardWorker(object):
    u"Almost Sisyphus"
    def __init__(self, task):
        self.task = task

    def work_hard(self):
        for i in range(100):
            self.task()
