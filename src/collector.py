"""System metrics collector module.

Provides classes for gathering real-time system metrics including CPU, memory,
disk, and network usage using psutil.
"""
import psutil

class Collector:
    """Collects system usage metrics at specified intervals.
    
    Attributes:
        interval (float): Time interval in seconds for CPU sampling.
    """
    def __init__(self, interval):
        """Initialize the Collector with a sampling interval.
        
        Args:
            interval (float): Interval in seconds for CPU usage sampling.
        """
        self.interval = interval

    def get_cpu_usage(self):
        """Retrieve current CPU usage per core and total.
        
        Returns:
            CPU: CPU usage object with per-core and average usage.
        """
        try:
            cpu_usage = CPU(psutil.cpu_percent(interval=self.interval, percpu=True))
            return cpu_usage
        except Exception:
            return CPU([-1])
    
    def get_memory_usage(self):
        """Retrieve current memory usage statistics.
        
        Returns:
            Memory: Memory usage object with total, used, and percentage.
        """
        try:
            memory_info = psutil.virtual_memory()
            memory_usage = Memory(memory_info.total, memory_info.used, memory_info.percent)
            return memory_usage
        except Exception:
            return Memory(-1, -1, -1)
            
    def get_disk_usage(self):
        """Retrieve disk usage for all partitions.
        
        Returns:
            list: List of DiskPartition objects for each drive partition.
        """
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
        """Retrieve total network bytes sent and received.
        
        Returns:
            Network: Network usage object with sent and received byte counts.
        """
        try:
            net = psutil.net_io_counters()
            network_usage = Network(net.bytes_sent, net.bytes_recv)
            return network_usage
        except Exception:
            return Network(-1, -1)
    
    def collect_metrics(self):
        """Collect all system metrics at once.
        
        Returns:
            dict: Dictionary containing CPU, memory, disk, and network metrics.
        """
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
    """Represents disk partition usage information.
    
    Attributes:
        name (str): Partition device name.
        total (int): Total capacity in bytes.
        used (int): Used space in bytes.
        percent (float): Usage percentage.
    """
    def __init__(self, name, total, used, percent):
        """Initialize DiskPartition with usage data.
        
        Args:
            name (str): Partition device name.
            total (int): Total capacity in bytes.
            used (int): Used space in bytes.
            percent (float): Usage percentage.
        """
        self.name = name
        self.total = total
        self.used = used
        self.percent = percent

class Memory():
    """Represents memory usage information.
    
    Attributes:
        total (int): Total memory in bytes.
        used (int): Used memory in bytes.
        percent (float): Usage percentage.
    """
    def __init__(self, total, used, percent):
        """Initialize Memory with usage data.
        
        Args:
            total (int): Total memory in bytes.
            used (int): Used memory in bytes.
            percent (float): Usage percentage.
        """
        self.total = total
        self.used = used
        self.percent = percent

class CPU():
    """Represents CPU usage information.
    
    Attributes:
        cpus (list): Per-core CPU usage percentages.
        total (float): Average CPU usage across all cores.
    """
    def __init__(self, cpus):
        """Initialize CPU with per-core usage data.
        
        Args:
            cpus (list): List of per-core CPU usage percentages.
        """
        self.cpus = cpus
        self.total = round(sum(cpus)/len(cpus), 1)

class Network():
    """Represents network usage information.
    
    Attributes:
        sent (int): Total bytes sent.
        recieved (int): Total bytes received.
    """
    def __init__(self, sent, recieved):
        """Initialize Network with traffic data.
        
        Args:
            sent (int): Total bytes sent.
            recieved (int): Total bytes received.
        """
        self.sent = sent
        self.recieved = recieved