-- modules/watermark.lua
local Watermark = {}

function Watermark.process(code)
    return "--[Obfuscated by Hercules v1.5 -> discord.gg/Hx6RuYs8Ku | by using the Hercules bot -> https://top.gg/bot/1293608330123804682]\n" .. code
end

return Watermark
