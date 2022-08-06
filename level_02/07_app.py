import lightning as L
from lightning_app.utilities.enum import (
    make_status,
    WorkFailureReasons,
    WorkStageStatus,
    WorkStatus,
    WorkStopReasons,
)
import time
# Allocate a default vm and run Work
def work_calls_len(lwork:L.LightningWork):
  """get the number of unique calls. state dict has current and past calls to work.
  if all of the calls had same arg1, then this will be 1
  the dict can change while this is running, so this is not a reliable way
  """
  # reduce by 1 to remove latest_call_hash entry
  return(len(lwork.state["calls"]) - 1)

class Work(L.LightningWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seq = None
    def run(self, seq:int, *args, **kwargs):
        # print(f"Hello world from work {seq}")
        self.seq = seq
        time.sleep(5)
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work(parallel=True, cache_calls=False)
        self.work_calls_len = None
        # if this variable is in REDIS, the there is delay
        self.counter = 1
        self.seq = None
        self.starttime = None
    def run(self):

        # work.status.stage could be in SUCCEEDED even after the run has been invoked
        # wait for seq to be set from work before trusting the veracity 
        if (self.work.status.stage == WorkStageStatus.NOT_STARTED) or (self.work.status.stage == WorkStageStatus.SUCCEEDED and self.work.seq == self.seq):   
          now = int(time.time() * 1000)
          if not(self.starttime is None):
            print(self.counter, "last run took (ms):", (now - self.starttime))
          self.work.run(self.counter)
          # print("ran ",self.counter )
          self.seq = self.counter
          self.starttime = now
          self.counter += 1  
    
if __name__ == "__main__":
    app = L.LightningApp(Flow())

"""
class WorkStageStatus:
    NOT_STARTED = "not_started"
    STOPPED = "stopped"
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
"""