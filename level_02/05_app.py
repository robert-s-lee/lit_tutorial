import lightning as L
from lightning_app.utilities.enum import (
    make_status,
    WorkFailureReasons,
    WorkStageStatus,
    WorkStatus,
    WorkStopReasons,
)
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
    def run(self,*args, **kwargs):
        print(f"Hello world from work {args[0]}")
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work(parallel=True, cache_calls=False)
        self.work_calls_len = None
        self.counter = 1
    def run(self):
        if (self.work.status.stage == WorkStageStatus.NOT_STARTED) or (self.work.status.stage == WorkStageStatus.SUCCEEDED):   
          self.work.run(self.counter)
           # x = work_calls_len(self.work)
          print("exec len",self.counter )
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