class Logs:
    def __init__(self, show_log=False):
        self.log = []
        self.show = show_log

    def append(self, log: str):
        self.log.append(log)
        if self.show:
            self.show_log()

    def show_log(self):
        if self.log:
            print('\n'.join(self.log))
            self.log.clear()
