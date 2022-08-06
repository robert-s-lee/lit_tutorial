import lightning as L
# Allocate a default vm and run Work
def work_calls_len(lwork:L.LightningWork):
  """get the number of call in state dict. state dict has current and past calls to work."""
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
        x = work_calls_len(self.work)
        if (x != self.work_calls_len):
          print(x)
          self.work_calls_len = x
        self.work.run(self.counter)
        self.counter += 1
if __name__ == "__main__":
    app = L.LightningApp(Flow())
