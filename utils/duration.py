from datetime import datetime


class Timer:
    def __init__(self):
        self.start_time = datetime.now()

    def start(self):
        self.start_time = datetime.now()

    def stop(self):
        return (datetime.now() - self.start_time).total_seconds()