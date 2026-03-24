from collector import Collector
from display import Display
from logger import Logger

import time, sys, os
from rich.live import Live
from rich.console import Console

cmds = {
    "--interval": 2,
    "--log": "c:\\users\\idanh\\downloads\\idan-sys-mon\\log.txt",
    "--cpu-warn": 90,
    "--mem-warn": 90,
    "--disk-warn": 95,
    "--net-warn": 1000000
}

console = Console()

def main():
    running = True
    log = False
    try:
        with Live(refresh_per_second=1) as live:
            usage_collector = Collector(cmds["--interval"]) # Usage collector
            display_adapter = Display(live, cmds["--cpu-warn"], cmds["--mem-warn"], cmds["--disk-warn"], cmds["--net-warn"]) # Display adapter
            
            console.print(f"""[blue]Starting monitor with the following settings:
Interval: {cmds['--interval']}, Log Path: {cmds['--log']}, 
CPU Warning: {cmds['--cpu-warn']}, Memory Warning: {cmds['--mem-warn']}, 
Disk Warning: {cmds['--disk-warn']}, Network Warning: {cmds['--net-warn']}
[/blue]""")
            
            if cmds["--log"] is None: pass
            elif os.path.exists("\\".join(cmds["--log"].split("\\")[:-1])):
                log = True
                logger = Logger(cmds["--log"])
            else: console.print("[red]Log file path invalid, logger disabled[/red]\n")
            
            previous_network = None
            start = time.time()
            end = time.time()
            while running:
                metrics = usage_collector.collect_metrics()
                end = time.time()
                metrics["previous_network"] = previous_network
                timeframe = end-start
                start = time.time()
                display_adapter.update(metrics, timeframe)
                
                if log: logger.log(metrics, timeframe)
                
                previous_network = metrics["network"]
                #time.sleep(interval) no need for that since were waiting the interval when colecting cpu data
                
    except KeyboardInterrupt:
        console.print("\n[purple]Ctrl+C pressed. Saving logs and exiting...[/purple]")
        sys.exit(0)
    except Exception:
        console.print("[red]General error, exiting program...[/red]\n")
        sys.exit(0)
    
def load_args():
    global cmds
    for arg, value in zip(sys.argv[1::2], sys.argv[2::2]):
        try:
            if arg in cmds.keys(): 
                if arg == "--log": cmds[arg] = value
                else: cmds[arg] = int(value)
        except:
            console.print(f"[red]Invalid argument {arg}, running with default value[/red]\n")
        
if __name__ == "__main__":
    load_args()
    main()