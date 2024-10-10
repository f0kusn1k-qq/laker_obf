import os
import shutil
import subprocess
import sys
import tempfile


class Hercules:
    def __init__ (self, program_logger):
        self._program_logger = program_logger
        self._lua = self._detectLUA()
        if self._lua is None:
            self._program_logger.error("Could not find LUA 5.4")
            self._program_logger.info("Shutting down due to missing LUA 5.4")
            sys.exit(1)
        self._obfuscator_folder = self._detectObfuscator()
        if self._obfuscator_folder is None:
            self._program_logger.error("Could not find Obfuscator")
            self._program_logger.info("Shutting down due to missing Obfuscator")
            sys.exit(1)
        self.methods = {'Control Flow': 0,
                        'Variable Renaming': 1,
                        'Garbage Code': 2,
                        'Opaque Predicates': 3,
                        'Bytecode Encoding': 4,
                        }


    def _detectLUA(self):
        LUA = shutil.which('lua54')
        if LUA is None:
            LUA = shutil.which('lua5.4')
            if LUA is None:
                LUA = shutil.which('lua')
                if LUA is None:
                    return None
                else:
                    result = subprocess.run([LUA, '-v'], capture_output=True, text=True)
                    if not '5.4' in result.stdout:
                        return None
        return LUA


    def _detectObfuscator(self):
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Obfuscator', 'src'))
        if os.path.exists(os.path.join(folder, 'hercules.lua')):
            return folder
        return None


    def isValidLUASyntax(self, lua_code: str) -> bool:
        with tempfile.NamedTemporaryFile(suffix=".lua", delete=False) as temp_file:
            temp_file.write(lua_code.encode('utf-8'))
            temp_file_path = temp_file.name

        try:
            result = subprocess.run(['luacheck', temp_file_path], capture_output=True, text=True)
            if result.returncode in [0,1]:
                return True
            else:
                return False
        finally:
            os.remove(temp_file_path)
            




if __name__ == '__main__':
    obfuscator = Hercules(None)


    lua_test = r'''-- Function to calculate Fibonacci numbers
function fibonacci(n)
    local fib = {0, 1} -- Initialize the first two Fibonacci numbers
    for i = 3, n do
        fib[i] = fib[i - 1] + fib[i - 2] -- Calculate the next Fibonacci number
    end
    return fib
end
-- Number of Fibonacci numbers to generate
local num = 10
local fib_sequence = fibonacci(num)
-- Print the Fibonacci sequence
for i = 1, ndo
    print(fib_sequence[i])
end'''

    

    print(obfuscator.isValidLUASyntax(lua_test))