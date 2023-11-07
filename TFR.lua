T = {}
T.__index = T
function T.new()
	local self = setmetatable({}, T)
	self.str = 'T'
	self.bool = {"ozo", "ulu"}
	return self
end
function T:answer(expr)
	return self.bool[eval(expr) and 2 or 1]
end

F = {}
F.__index = F
function F.new()
	local self = setmetatable({}, F)
	self.str = 'F'
	self.bool = {"ozo", "ulu"}
	return self
end
function F:answer(expr)
	return self.bool[eval(expr) and 1 or 2]
end

R = {}
R.__index = R
function R.new()
	local self = setmetatable({}, R)
	self.str = 'R'
	self.bool = {"ozo", "ulu"}
	return self
end
function R:answer(expr)
	return self.bool[math.random(2)]
end

function shuffle(x)
	math.randomseed(os.time()*math.random())
	for i = #x, 2, -1 do
		local j = math.random(#x)
		x[i], x[j] = x[j], x[i]
		local j = math.random(i)
		x[i], x[j] = x[j], x[i]
	end
	return x
end

function isinstance(x, t)
	if x.str == nil then
		return nil
	elseif x.str == t then
		return true
	elseif type(t) == 'table' then
		for _, v in ipairs(t) do
			if x.str == v then return true end
		end
	else
		return false
	end
end

function eval(expr)
	if (type(expr) == "number") then
		return expr ~= 0
	elseif (type(expr) == "string") then
		return expr ~= ""
	elseif (type(expr) == "table") then
		return next(expr) ~= nil
	else
		return (expr and true or false)
	end
end

function gen_seat(ticket)
	seat = {}
	for i=1,ticket[1] do
		seat[#seat+1]=T.new()
	end
	for i=1,ticket[2] do
		seat[#seat+1]=F.new()
	end
	for i=1,ticket[3] do
		seat[#seat+1]=R.new()
	end
	shuffle(seat)
	return seat
end

function score(seat,role)
	if #seat ~= #role then
		print("The length of guesses does not match!")
		return nil
	end
	local pts = 0
	for i,v in ipairs(seat) do
		print(i, v.str)
		if role[i] == v.str then
			pts= pts + 1
		end
	end
	print(table.concat({"You've correctly guessed",pts,"/",#seat,"roles."}," "))
end

local function exec(code)
    local func, err = loadstring(code)
    if func then
        func()
    else
        print("Error executing code:", err)
    end
end
function hint()
print([[
=-=-=-=-=-=-=-=-= TFR in Lua =-=-=-=-=-=-=-=-=-=-=-=
The three god riddle game implemented in Lua 5.1
T will answer truth to your question.
F will answer falsehood to your question.
R will answer randomly.
the two words they will use are {"ozo", "ulu"}
=-=-=-=-=-=-=-=-=-= COMMANDS =-=-=-=-=-=-=-=-=-=-=-=
hint()        Print this help.
game()        Start a new game.
game({3,2,1}) Start a new game with {#T=3,#F=2,#R=1}.
quit()        Exit this program.]])
end
function game(ticket)
	if ticket and type(ticket)== 'table' and #ticket ==3 then
		seat = gen_seat(ticket)
	else
		seat = gen_seat({1,1,1})
	end
	for i=1,#seat do
		io.write("(",i,"/",#seat,") Which seat # do you want to ask[1-",#seat,"]?: \n>>>")
		n = io.read()
		io.write("(",i,"/",#seat,") What question do you want to ask?: \n>>>")
		q = io.read()
		s = table.concat({"print('The answer is:',seat[",n,"]:answer(",q,"))"})
		exec(s)
	end
	print("Please give the roles as a table, e.g. {'F','T','R'}:")
	io.write(">>> ")
	s = io.read()
	s = table.concat({"score(seat,",s,")"})
	exec(s)
end

-- Main Loop --
hint()
while true do
	io.write(_PROMPT or "> ")
	s = io.read()
	if #s==0 or s == "quit()" or s == "exit" then break end
	exec(s)
end
