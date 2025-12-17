import logging
from os.path import exists
from pprint import pformat

import xarray as xr
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich import print

LOGGER = logging.getLogger("syize")


class NCView:
    def __init__(self, data_path: str):
        if not exists(data_path):
            LOGGER.error(f"File not exists: {data_path}")
            exit(1)
            
        try:
            self.dataset = xr.open_dataset(data_path, decode_timedelta=False)
            
        except ValueError:
            LOGGER.error(f"Failed to read data: {data_path}.")
            LOGGER.error("Check if it is a NetCDF data.")
            exit(1)
            
        self.completer = WordCompleter(["help", "quit", "attrs", "coords", "data", "vars"], ignore_case=True)
        self.session = PromptSession(message=">>> ", completer=self.completer)
            
    def _help(self):
        print("[red]You are in the interactive mode of syize.NCView.")
        print("")
        print("[red]Available command:")
        print("[cyan]NCView command:")
        print("\t[green]help | h        [blue]print this message.")
        print("\t[green]quit | q        [blue]exit.")
        print("[cyan]Command to print data:")
        print("\t[green]attrs           [blue]print attributes of the dataset.")
        print("\t[green]coords          [blue]print coordinates of the dataset.")
        print("\t[green]data            [blue]print the whole dataset.")
        print("\t[green]field           [blue]print the field.")
        print("\t[green]field.data      [blue]print data of the field.")
        print("\t[green]field.attr      [blue]print attributes of the field.")
        print("\t[green]vars            [blue]print variables list.")
        print("")
        print("[red]You can type `help` or `h` to see this message again.")
        
    def exec_command(self, field: str):
        field_list = field.split(".")
        
        if len(field_list) < 2:
            
            if field_list[0] == "data":
                print(self.dataset)
                
            elif field_list[0] == "attrs":
                print(pformat(self.dataset.attrs))
                
            elif field_list[0] == "vars":
                print(self.dataset.data_vars)
                
            elif field_list[0] == "coords":
                print(self.dataset.coords)
                
            else:
                print(self.dataset[field])
                
        else:
            if field_list[-1] == "data":
                print(self.dataset[field_list[0]].to_numpy())
                
            elif field_list[-1] == "attr":
                print(pformat(self.dataset[field_list[0]].attrs))
                
            else:
                print(f"[red]Unknow attributes: {field_list[-1]}")
        
            
    def interact(self):
        exit_flag = False
        self._help()
        
        while not exit_flag:
            
            field = self.session.prompt()
            field = str(field).strip()
            
            if field in ["help", "h"]:
                self._help()
                
            elif field in ["quit", "q"]:
                exit_flag = True
                
            elif field == "":
                pass
                
            else:
                try:
                    self.exec_command(field)
                    
                except (ValueError, KeyError):
                    print(f"[red]Field name error: {field}")
        
        exit(0)
        
        
__all__ = ["NCView"]
