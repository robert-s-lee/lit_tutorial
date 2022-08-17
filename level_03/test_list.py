from lightning_app import LightningFlow, LightningWork
from lightning_app.structures import List
class CounterWork(LightningWork):
    def __init__(self):
        super().__init__()
        self.counter = 0
    def run(self):
        self.counter += 1

class RootFlow(LightningFlow):
    def __init__(self):
        super().__init__()
        self.list = List(*[CounterWork(), CounterWork()])
    def run(self):
        for work in self.list:
            work.run()

flow = RootFlow()
flow.run()
assert flow.list[0].counter == 1
