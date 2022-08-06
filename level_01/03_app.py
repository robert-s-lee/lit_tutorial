import lightning as L
from lightning_app.frontend import StreamlitFrontend
import streamlit as st
# lets create UI
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
class Work(L.LightningWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def run(self,*args, **kwargs):
        print(f"Hello world from work {args[0]}")
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work()
        self.ui = UI()
    def run(self):
        self.work.run(self.ui.msg)
if __name__ == "__main__":
    app = L.LightningApp(Flow())
