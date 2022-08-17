import lightning as L
from lightning_app.utilities.enum import WorkStageStatus
import time
import os
class Work(L.LightningWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seq = None
    def run(self, seq:int, *args, **kwargs):
        # print(f"Hello world from work {seq}")
        self.seq = seq
        time.sleep(int(os.getenv("WORK_DURATION", 0)))
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work(parallel=True, cache_calls=False)
        self.counter = 1
        self.seq = None
        self.starttime = None
    def run(self):

        if (self.work.status.stage == WorkStageStatus.NOT_STARTED) or (self.work.status.stage == WorkStageStatus.SUCCEEDED and self.work.seq == self.seq):   
          now = int(time.time() * 1000)
          if not(self.starttime is None):
            print(self.counter, "last run took (ms):", (now - self.starttime))
          self.work.run(self.counter)
          self.seq = self.counter
          self.starttime = now
          self.counter += 1  
    
if __name__ == "__main__":
    app = L.LightningApp(Flow())

