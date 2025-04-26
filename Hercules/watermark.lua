-- modules/watermark.lua
function Watermark.process(code)
    local watermark = [[
         __    ____                      __           __   __                 __      __      ____      _ __  
  ____  / /_  / __/_  ________________ _/ /____  ____/ /  / /_  __  __   ____/ /___  / /___  / __/___  (_) /__
 / __ \/ __ \/ /_/ / / / ___/ ___/ __ `/ __/ _ \/ __  /  / __ \/ / / /  / __  / __ \/ / __ \/ /_/ __ \/ / //_/
/ /_/ / /_/ / __/ /_/ (__  ) /__/ /_/ / /_/  __/ /_/ /  / /_/ / /_/ /  / /_/ / /_/ / / /_/ / __/ / / / / ,<   
\____/_.___/_/  \__,_/____/\___/\__,_/\__/\___/\__,_/  /_.___/\__, /   \__,_/\____/_/\____/_/ /_/ /_/_/_/|_|  
                                                             /____/      
                                        start from loader instad it may crash u xD
]]
    local result = ""
    for line in watermark:gmatch("[^\r\n]+") do
        result = result .. "--" .. line .. "\n"
    end
    return result .. code
end

return Watermark
