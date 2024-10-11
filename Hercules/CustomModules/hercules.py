import os
import shutil
import subprocess
import sys
import tempfile
from functools import lru_cache


class Hercules:
    def __init__ (self, program_logger):
        self._program_logger = program_logger
        self._lua = self._getLuaInterpreter()
        if self._lua is None:
            self._program_logger.error("Could not find LUA 5.4")
            self._program_logger.info("Shutting down due to missing LUA 5.4")
            sys.exit(1)
        self._obfuscator_folder, self.obfuscator_file = self._detectObfuscator()
        if self._obfuscator_folder is None:
            self._program_logger.error("Could not find Obfuscator")
            self._program_logger.info("Shutting down due to missing Obfuscator")
            sys.exit(1)
        self.methods = [
            {'key': 'control_flow', 'name': 'Control Flow', 'bitkey': 0},
            {'key': 'variable_renaming', 'name': 'Variable Renaming', 'bitkey': 1},
            {'key': 'garbage_code', 'name': 'Garbage Code', 'bitkey': 2},
            {'key': 'opaque_predicates', 'name': 'Opaque Predicates', 'bitkey': 3},
            {'key': 'bytecode_encoding', 'name': 'Bytecode Encoding', 'bitkey': 4},
        ]


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

    def obfuscate(self, file_path: str, bitkey: int):
        old_wd = os.getcwd()
        os.chdir(self._obfuscator_folder)
        enabled_features = self._get_active_keys(bitkey)

        flags = " ".join([f"--{feature}" for feature in enabled_features])
        self._program_logger.info(f"Obfuscating file: {file_path} with flags: {flags}")
        
        try:
            result = subprocess.run([self._lua, "hercules.lua", file_path, "--overwrite"],
                                    check=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            
        except subprocess.CalledProcessError as e:
            self._program_logger.error(f"Error occurred: {e.output.decode()}\nFile: {file_path}")
            return
        finally:
            os.chdir(old_wd)
        if result.returncode != 0:
            return False
        else:
            return True

    @lru_cache(maxsize=None)
    def find_method(self, method_name):
        for method in self.methods:
            if method['name'] == method_name:
                return method
        return None

    @lru_cache(maxsize=None)
    def _get_active_keys(self, bitkey):
        max_bitkey = (1 << len(self.methods)) - 1
        if bitkey < 0 or bitkey > max_bitkey:
            raise ValueError(f"Invalid bitkey: {bitkey}. It must be between 0 and {max_bitkey}.")

        active_keys = []
        for method in self.methods:
            if bitkey & (1 << method['bitkey']):
                active_keys.append(method['key'])
        return active_keys

    def _getLuaInterpreter(self) -> str:
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
                    else:
                        return "lua"
            else:
                return "lua5.4"
        else:
            return "lua54"

    def _detectObfuscator(self):
        folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Obfuscator', 'src')).replace('\\', '/')
        file = os.path.join(folder, 'hercules.lua').replace('\\', '/')
        if os.path.exists(os.path.join(folder, 'hercules.lua')):
            return folder, file
        return None


            



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

    
    
    obfuscator.obfuscate("C:/Users/wissm/OneDrive/Dokumente/Visual Studio Repos/DiscordBots-Hercules/Hercules/Hercules-Bot/Buffer/970119359840284743_url.lua", 31)
        