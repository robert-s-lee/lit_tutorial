import lightning as L
# basic hello World
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def run(self,*args, **kwargs):
        print("Hello world from infinite event loop")
if __name__ == "__main__":
    app = L.LightningApp(Flow())
