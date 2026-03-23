from datetime import datetime
from rich.console import Console
import json

console = Console()

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
    
    def log(self, metrics, timeframe):
        json_usage = usage_to_json(metrics, timeframe)
        
        try:
            with open(self.log_path, "a") as f:
                f.write(json_usage)
        except PermissionError:
            console.print("[red]Error trying to open the log file[/red]")

def usage_to_json(metrics, timeframe):
    now = datetime.now()
    timestamp_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    if not metrics["previous_network"]: 
        upload_rate = 0
        download_rate = 0
    else:
        upload_rate = (metrics["network"].sent - metrics["previous_network"].sent)/timeframe
        download_rate = (metrics["network"].recieved - metrics["previous_network"].recieved)/timeframe
    
    usage_dict = {
        timestamp_string:{
            "CPU Usage":{
            },
            "Disk Usage":{
            },
            "Memory Usage":{
                "Used": format_bytes(metrics["memory"].used),
                "Total": format_bytes(metrics["memory"].total),
                "Percent": f"{metrics["memory"].percent}%"
            },
            "Network Usage":{
                "Upload": format_bytes(upload_rate),
                "Download": format_bytes(download_rate)
            }
        }
    }
    
    for i, cpu in enumerate(metrics["cpu"].cpus):
        usage_dict[timestamp_string]["CPU Usage"][str(i+1)] = f"{cpu}%"
    usage_dict[timestamp_string]["CPU Usage"]["Total"] = f"{metrics["cpu"].total}%"
    
    for partition in metrics["disk"]:
        usage_dict[timestamp_string]["Disk Usage"][partition.name] = f"{partition.percent}%"
    
    json_usage = json.dumps(usage_dict, indent=4)
    return json_usage

def format_bytes(bytes):
    exts = ["B", "KB", "MB", "GB", "TB"]
    counter = 0
    while bytes >= 1024 and counter <= 4:
        bytes /= 1024
        counter += 1
    return f"{round(bytes, 2)}{exts[counter]}"