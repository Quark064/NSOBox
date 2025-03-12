class ADBCommand:
    def __init__(self):
        self.commands = []
        self.useSU = False

    def AddCommand(self, command: str):
        self.commands.append(command)
        return self
    
    def UseSU(self):
        self.useSU = True
        return self
        
    def Build(self) -> str:
        command = " && ".join(self.commands)
        command = command.replace('"', '\\"').replace("'", "'\"'\"'")

        if self.useSU:
            return f"""adb shell "su -c '{command}'\""""

        return f'adb shell "{command}"'
