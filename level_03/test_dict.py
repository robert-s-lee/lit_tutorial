from lightning_app import LightningFlow, LightningWork
from lightning_app.structures import Dict
class CounterWork(LightningWork):
    def __init__(self):
        super().__init__()
        self.counter = 0
    def run(self):
        self.counter += 1

class RootFlow(LightningFlow):
    def __init__(self):
        super().__init__()
        self.dict = Dict(**{"work_0": CounterWork(), "work_1": CounterWork()})
    def run(self):
        for work_name, work in self.dict.items():
            work.run()

flow = RootFlow()
flow.run()
assert flow.dict["work_0"].counter == 1
