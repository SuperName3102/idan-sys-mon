from rich.table import Table
from rich.console import Console
from rich.columns import Columns

console = Console()

class Display:
    def __init__(self, live):
        self.live = live
    
    def display_cpu(self, cpu_usage):
        table = Table(title="CPU Usage")
        table.add_column("Core")
        table.add_column("Usage")
        for i, core in enumerate(cpu_usage.cpus):
            table.add_row(str(i + 1), f"{core}%")
        table.add_row("Total", f"{cpu_usage.total}%")
        return table
    
    def display_memory(self, memory_usage):
        table = Table(title="Memory Usage")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_row("Used", f"{format_bytes(memory_usage.used)}")
        table.add_row("Total", f"{format_bytes(memory_usage.total)}")
        table.add_row("Percent", f"{memory_usage.percent}%")
        return table
    
    def display_disk(self, disk_usage):
        table = Table(title="Disk Usage")
        table.add_column("Partition")
        table.add_column("Usage")
        for partition in disk_usage:
            table.add_row(partition.name, f"{partition.percent}%")
        return table
    
    def update(self, metrics):
        cpu_table = self.display_cpu(metrics["cpu"])
        memory_table = self.display_memory(metrics["memory"])
        disk_table = self.display_disk(metrics["disk"])
        
        combined_tables = Columns([cpu_table, disk_table, memory_table])
        self.live.update(combined_tables)


def format_bytes(bytes):
    exts = ["B", "KB", "MB", "GB", "TB"]
    counter = 0
    while bytes >= 1024 and counter <= 4:
        bytes /= 1024
        counter += 1
    return f"{round(bytes, 2)}{exts[counter]}"