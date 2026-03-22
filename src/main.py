from collector import Collector
from display import Display
from logger import Logger

import time, sys, os
from rich.live import Live
from rich.console import Console

interval = 2

cmds = {
    "--interval": 2,
    "--log": "c:\\users\\idanh\\downloads\\idan-sys-mo",
    "--cpu-warn": None,
    "--mem-warn": None
}

console = Console()

def main():
    running = True
    log = False
    try:
        with Live(refresh_per_second=1) as live:
            usage_collector = Collector() # Usage collector
            display_adapter = Display(live) # Display adapter
            
            if cmds["--log"] is None: pass
            elif os.path.exists(cmds["--log"]):
                log = True
                logger = Logger(cmds["--log"])
            else: console.print("[red]Log file path invalid, logger disabled[/red]")
            
            while running:
                metrics = usage_collector.collect_metrics()
                
                display_adapter.update(metrics)
                
                if log: logger.log(metrics)
                time.sleep(interval)
                
    except KeyboardInterrupt:
        console.print("\nCtrl+C pressed. Saving logs and exiting.")
        sys.exit(0)

def load_args():
    global cmds
    for arg, value in zip(sys.argv[1::2], sys.argv[2::2]):
        if arg in cmds.keys(): cmds[arg] = value

if __name__ == "__main__":
    load_args()
    main()