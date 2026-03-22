from datetime import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
    
    def log(self, metrics):
        timestamp = datetime.now()
        cpu_usage = metrics["cpu"]
        memory_usage = metrics["memory"]
        disk_usage = metrics["disk"]
        
        with open(self.log_path, "w+") as f:
            f.write(timestamp)
            f.write(cpu_usage)
            f.write(memory_usage)
            f.write(disk_usage)