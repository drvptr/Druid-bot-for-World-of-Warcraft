local frame = CreateFrame("Frame", "CoordsColorBar", UIParent)
frame:SetSize(90, 30) 
frame:SetPoint("TOPLEFT", UIParent, "TOPLEFT", 0, 0)

local textureX = frame:CreateTexture()
local textureY = frame:CreateTexture()
local textureZ = frame:CreateTexture()

textureX:SetSize(30, 30)
textureY:SetSize(30, 30)
textureZ:SetSize(30, 30)

textureX:SetPoint("TOPLEFT", frame, "TOPLEFT", 0, 0)
textureY:SetPoint("TOPLEFT", frame, "TOPLEFT", 30, 0)
textureZ:SetPoint("TOPLEFT", frame, "TOPLEFT", 60, 0)

local function encodeFloatToRGB(value)
	local intVal = math.floor(value * 1000)  
	local r = math.floor(intVal / 65536) % 256 / 255
	local g = math.floor(intVal / 256) % 256 / 255
	local b = (intVal % 256) / 255
	return r, g, b
end

frame:SetScript("OnUpdate", function()
	local x, y, z = UnitPosition("player")
	if x and y and z then
		local r1, g1, b1 = encodeFloatToRGB(x)
		local r2, g2, b2 = encodeFloatToRGB(y)
		local r3, g3, b3 = encodeFloatToRGB(z)
		textureX:SetColorTexture(r1, g1, b1, 0.99) -- 99% alpha channel for improve refresh
		textureY:SetColorTexture(r2, g2, b2, 0.99)
		textureZ:SetColorTexture(r3, g3, b3, 0.99)
		textureX:SetColorTexture(r1, g1, b1, 1)
		textureY:SetColorTexture(r2, g2, b2, 1)
		textureZ:SetColorTexture(r3, g3, b3, 1)
		-- print(string.format("X: %.3f, Y: %.3f, Z: %.3f", x, y, z))
	else
		-- print("ERROR: UnitPosition return nil!")
	end
end)
