import time
import sys

class Timer:
    timeSum = 0
    numberOfCycles = 0
    def __init__(self):
        pass

    def start(self):
        self.startTime = time.perf_counter()

    def stop(self):
        self.endTime = time.perf_counter()
        Timer.timeSum += (self.endTime - self.startTime)
        Timer.numberOfCycles += 1
        self.averageTime = round(Timer.timeSum / Timer.numberOfCycles, 8)

    def __str__(self):
        return str(self.averageTime)


