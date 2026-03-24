from rich.table import Table
from rich.console import Console
from rich.columns import Columns
from plyer import notification

console = Console()

class Display:
    def __init__(self, live, cpu_warn, mem_warn, disk_warn, net_warn):
        self.live = live
        self.cpu_warn = cpu_warn
        self.mem_warn = mem_warn
        self.disk_warn = disk_warn
        self.net_warn = net_warn
    
    def display_cpu(self, cpu_usage):
        table = Table(title="CPU Usage")
        table.add_column("Core")
        table.add_column("Usage")
        for i, core in enumerate(cpu_usage.cpus):
            table.add_row(str(i + 1), f"{core}%", style=get_warn_color(core, self.cpu_warn, f"CPU usage for core {i+1}"))
        
        table.add_row("Total", f"{cpu_usage.total}%", style=get_warn_color(core, self.cpu_warn, f"total CPU usage"))
        return table
    
    def display_memory(self, memory_usage):
        table = Table(title="Memory Usage")
        table.add_column("Metric")
        table.add_column("Value")
        
        color = get_warn_color(memory_usage.percent, self.mem_warn, "memory usage")
        table.add_row("Used", f"{format_bytes(memory_usage.used)}", style=color)
        table.add_row("Total", f"{format_bytes(memory_usage.total)}", style=color)
        table.add_row("Percent", f"{memory_usage.percent}%", style=color)
        return table
    
    def display_disk(self, disk_usage):
        table = Table(title="Disk Usage")
        table.add_column("Partition")
        table.add_column("Usage")
        for partition in disk_usage:
            table.add_row(partition.name, f"{partition.percent}%", style=get_warn_color(partition.percent, self.disk_warn, None))
        return table
    
    def display_network(self, network, previous_network, timeframe):
        table = Table(title="Network Usage")
        table.add_column("Metric")
        table.add_column("Value")

        if not previous_network: 
            upload_rate = 0
            download_rate = 0
        else:
            upload_rate = (network.sent - previous_network.sent)/timeframe
            download_rate = (network.recieved - previous_network.recieved)/timeframe
        
        table.add_row("Upload", f"{format_bytes(upload_rate)}/s", style=get_warn_color(upload_rate, self.net_warn, None))
        table.add_row("Download", f"{format_bytes(download_rate)}/s", style=get_warn_color(download_rate, self.net_warn, None))
        return table
    
    def update(self, metrics, timeframe):
        cpu_table = self.display_cpu(metrics["cpu"])
        memory_table = self.display_memory(metrics["memory"])
        disk_table = self.display_disk(metrics["disk"])
        network_table = self.display_network(metrics["network"], metrics["previous_network"], timeframe)
        
        combined_tables = Columns([cpu_table, disk_table, memory_table, network_table])
        self.live.update(combined_tables)


def format_bytes(bytes):
    exts = ["B", "KB", "MB", "GB", "TB"]
    counter = 0
    while bytes >= 1024 and counter <= 4:
        bytes /= 1024
        counter += 1
    return f"{round(bytes, 2)}{exts[counter]}"

def get_warn_color(parameter, limit, type):
    if parameter > limit:
        if type: send_notification(f"{type} passed the threshold", f"Got a warning for {type} being higher than {limit} ({parameter})")
        return "on red"
    if parameter > limit/2: return "on yellow"
    return "on green"

def send_notification(title, message, timeout=2):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Idan System Monitor",
            timeout=timeout,
        )
    except Exception:
        console.print("[red]Error sending desktop notification[/red]\n")