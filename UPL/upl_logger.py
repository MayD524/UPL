
import os

class logger:
    def __init__(self, log_file=None):
        self.log_file = log_file

    
    def toLog(self, logData):
        if self.log_file != None:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r") as reader:
                    data = reader.readlines()
                with open(self.log_file, "a+") as writer:
                    data.append(logData)
                    writer.writelines(data)
                
                return True

        return False

    def log(self, types, log):
        print(f"[{types}] - {log}")