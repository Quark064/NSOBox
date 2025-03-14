from Strings import Utils
from subprocess import call

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
    
    def Run(self):
        call(self.Build(), shell=True)

class ADBUtil:
    def OverwriteFile(filePath: str, contents: str, useSU=False) -> None:
        CHUNK_SIZE = 4000

        encodedText = Utils.ToHexString(contents)
        parts = [encodedText[i:i + CHUNK_SIZE] for i in range(0, len(encodedText), CHUNK_SIZE)]
        parts[-1] = f"{parts[-1]}\\x0A"
        
        out = []
        first = True
        for part in parts:
            if first:
                out.append(f'printf "{part}" > "{filePath}"')
                first = False
            else:
                out.append(f'printf "{part}" >> "{filePath}"')
        
        for command in out:
            command = command.replace('"', '\\"').replace("'", "'\"'\"'")
            if useSU:
                call(f"""adb shell "su -c '{command}'\"""", shell=True)
            else:
                call(f'adb shell "{command}"', shell=True)