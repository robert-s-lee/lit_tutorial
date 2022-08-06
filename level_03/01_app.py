from re import S
import lightning as L
from lightning_app.frontend import StreamlitFrontend
from lit_bashwork import LitBashWork
from lit_bashwork.lit_work_utils import work_is_free, work_calls_len
import streamlit as st
from lightning_app.structures import Dict, List
from lightning_app.utilities.enum import (
    make_status,
    WorkFailureReasons,
    WorkStageStatus,
    WorkStatus,
    WorkStopReasons,
)
# utilities
def set_flow_stage_from_work(work, flow_stage) -> WorkStageStatus:
  if flow_stage != work.status.stage:
      print(f"work stage is {work.status.stage}")
      return(work.status.stage)
  else:
    return(flow_stage)
# use UI to drive work
def ui_bash(state):
  state.target_bash = st.text_input("bash")
  submit_bash = st.button("submit")
  if submit_bash:
    state.process_bash = True
def ui_args(state):
  state.target_args = st.text_input("args")
  submit_args = st.button("submit")
  if submit_args:
    state.process_args = True
def ui_main(state):
  page_names_to_func = {
    'Args': ui_args,
    'Bash': ui_bash,}
  page = st.sidebar.radio("Main Menu", options=page_names_to_func.keys())
  page_names_to_func[page](state)
class UI(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_args = None
        self.target_bash = None
        self.process_args = False
        self.process_bash = False
    def configure_layout(self):
      return(StreamlitFrontend(render_fn=ui_main))
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work_args = LitBashWork(parallel=False, cache_calls=False, cloud_compute=L.CloudCompute("cpu-small"))
        self.work_bash = LitBashWork(parallel=True, cache_calls=False, cloud_compute=L.CloudCompute("default"))
        self.work_args_stage = None
        self.work_bash_stage = None
        self.work_args_len = None
        self.work_bash_len = None        
        self.ui = UI()

    def run(self):
        self.work_args_stage = set_flow_stage_from_work(self.work_args, self.work_args_stage)
        self.work_bash_stage = set_flow_stage_from_work(self.work_bash, self.work_bash_stage)

        if self.ui.process_bash:
          if self.work_bash.parallel or self.work_bash.cache_calls == False: 
            self.ui.process_bash = False
          self.work_bash.run(self.ui.target_bash)
          self.ui.process_bash = False

        if self.ui.process_args:
          if self.work_args.parallel or self.work_args.cache_calls == False: 
            self.ui.process_args = False
          self.work_args.run(f"python hello.py {self.ui.target_args}")
          self.ui.process_args = False

if __name__ == "__main__":
    app = L.LightningApp(Flow())

"""
not_started
pending (waiting for vm right before running)
running (wen a new run is run)
succeeded (remain succeeded if same run is submitted)
running (wen a new run is run)
succeeded
"""