import psutil

class Collector:
    def __init__(self, interval):
        self.interval = interval

    def get_cpu_usage(self):
        try:
            cpu_usage = CPU(psutil.cpu_percent(interval=self.interval, percpu=True))
            return cpu_usage
        except Exception:
            return CPU([-1])
    
    def get_memory_usage(self):
        try:
            memory_info = psutil.virtual_memory()
            memory_usage = Memory(memory_info.total, memory_info.used, memory_info.percent)
            return memory_usage
        except Exception:
            return Memory(-1, -1, -1)
            
    def get_disk_usage(self):
        try:
            partitions = [part.device for part in psutil.disk_partitions()]
            disk_usage = []
            for partition in partitions:
                disk_info = psutil.disk_usage(partition)
                partition_usage = DiskPartition(partition, disk_info.total, disk_info.used, disk_info.percent)
                disk_usage.append(partition_usage)
            return disk_usage
        except Exception:
            return [DiskPartition("-1", -1, -1, -1)]
    
    def get_network_usage(self):
        try:
            net = psutil.net_io_counters()
            network_usage = Network(net.bytes_sent, net.bytes_recv)
            return network_usage
        except Exception:
            return Network(-1, -1)
    
    def collect_metrics(self):
        cpu_usage = self.get_cpu_usage()
        memory_usage = self.get_memory_usage()
        disk_usage = self.get_disk_usage()
        network_usage = self.get_network_usage()
        
        return {
            "cpu": cpu_usage,
            "memory": memory_usage,
            "disk": disk_usage,
            "network": network_usage
        }
    

class DiskPartition():
    def __init__(self, name, total, used, percent):
        self.name = name
        self.total = total
        self.used = used
        self.percent = percent

class Memory():
    def __init__(self, total, used, percent):
        self.total = total
        self.used = used
        self.percent = percent

class CPU():
    def __init__(self, cpus):
        self.cpus = cpus
        self.total = round(sum(cpus)/len(cpus), 1)

class Network():
    def __init__(self, sent, recieved):
        self.sent = sent
        self.recieved = recieved