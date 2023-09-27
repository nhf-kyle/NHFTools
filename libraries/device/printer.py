#Version 23.01 [UNSTABLE, IN DEVELOPMENT] Library to print labels via Zebra Printer

import os
import sys
import time
import subprocess
import win32print

class ZebraPrinter:
    #Initialize connection to printer
    def __init__(self):
        operating_system = ''
        if sys.platform.lower().startwith('win'):
            import win32print
            operating_system = 'Windows'
        else:
            import subprocess
            operating_system = 'Linux'
        self.queue = 'ZDesigner GK420d'

    #Print label
    def print_label(self, label):
        label = str(label).encode()
        if self.operating_system == 'Windows':
            printer = win32print.OpenPrinter(self.queue)
            try:
                job = win32print.StartDocPrinter(printer, 1, ('Label',None,'RAW'))
                try:
                    win32print.StartPagePrinter(printer)
                    win32print.WritePrinter(printer, label)
                    win32print.EndPagePrinter(printer)
                finally:
                     win32print.EndDocPrinter(printer)
            finally:
                 win32print.ClosePrinter(printer)
        else:
            printer = subprocess.Popen(['lpr','-P{}'.format(self.queue),'-oraw'], stdin=subprocess.PIPE)
            printer.communicate(label)
            printer.stdin.close()