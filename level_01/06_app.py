import lightning as L
from lightning_app.frontend import StreamlitFrontend
from lit_bashwork import LitBashWork
import streamlit as st
# use UI to drive work
def ui_main(state):
  msg = st.text_input("msg")
  submit = st.button("submit")
  if submit:
    state.msg = msg
    state.process_run = True
class UI(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = None
        self.process_run = False
    def configure_layout(self):
      return(StreamlitFrontend(render_fn=ui_main))
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = LitBashWork(cloud_compute=L.CloudCompute("cpu-small"))
        self.ui = UI()
    def run(self):
        if self.ui.process_run:
          self.work.run(f"python hello.py {self.ui.msg}")
          self.ui.process_run = False
if __name__ == "__main__":
    app = L.LightningApp(Flow())
