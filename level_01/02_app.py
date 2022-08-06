import lightning as L
# Allocate a default vm and run Work
class Work(L.LightningWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def run(self,*args, **kwargs):
        print("Hello world from work")
class Flow(L.LightningFlow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.work = Work()
    def run(self):
        self.work.run()
if __name__ == "__main__":
    app = L.LightningApp(Flow())
