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
    def run(self,*args, **kwargs):
        print(f"Hello world from work {args[0]}")
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work(parallel=True, cache_calls=False)
        self.work_calls_len = None
        # if this variable is in REDIS, the there is delay
        self.work_status_stage = WorkStageStatus.NOT_STARTED
        self.counter = 1
    def run(self):

        # there is lag in work.status.stage getting back to flow
        # set the work.status.stage in flow
        if (self.work_status_stage == WorkStageStatus.NOT_STARTED) or (self.work_status_stage == WorkStageStatus.SUCCEEDED):   
          self.work_status_stage = "X"  
          #print("flow",self.work_status_stage,"work",self.work.status.stage )
          self.work.run(self.counter)
          # x = work_calls_len(self.work)
          print("exec len",self.counter )
          self.counter += 1  
        # then wait for work.status.stage to change
        else:
          if (self.work.status.stage != self.work_status_stage):
            self.work_status_stage = self.work.status.stage
    
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