import discord
from discord.ext import commands, tasks
from discord.utils import get
from kahoot import client
import platform
import datetime
import asyncio
import random
import json
import aiohttp
import psutil
import os

botclient = commands.Bot(command_prefix = ['!', 'k!', 'K!'])


defaultColour = discord.Colour(0x2ed7de)
greenColour = discord.Colour(0x00f708)
orangeColour = discord.Colour(0xffa500)
redColour = discord.Colour(0xff1500)

allowed_channel_id = [765702373308891186, 765493609029566476]

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

botclient.remove_command('help')

###
@botclient.event
async def on_ready():
	status = f'!help | kahootbot.xyz'
	await botclient.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
	print(f"Bot logged in as '{botclient.user.name}' ({botclient.user.name}).\n")

# ###
# @botclient.command(pass_context=True)
# async def say(ctx, *, sentence):
# 	await ctx.send(sentence)

# ###
# @say.error
# async def say_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         embed = discord.Embed(title='Please specify the message for the bot to send. Eg: "!say Hello!"',colour = redColour)
#         await ctx.send(embed=embed)

###
@botclient.command(aliases=['Help'])
async def help(ctx):
	if ctx.channel.id in allowed_channel_id:
		embed = discord.Embed(colour = defaultColour, title = 'Help Menu')
		embed.add_field(name='`▬▬▬▬▬▬ !raid ▬▬▬▬▬▬`', value='Raid a Kahoot lobby! Options will be given once the command has been exectuted.', inline=False)
		embed.add_field(name='`▬▬▬▬▬▬ !info ▬▬▬▬▬▬`', value='Displays information about the bot.', inline=False)
		embed.add_field(name='`▬▬▬▬▬▬ !disclaimer ▬▬▬▬▬▬`', value='Displays necessary disclaimer.', inline=False)
		embed.set_footer(text=" \nNote: If a username has been kicked out of a game already, the bot cannot join another user with the same name. This is due to Kahoot's own limitations.")
		await ctx.send(embed=embed)

###
@botclient.command()
async def info(ctx):
	if ctx.channel.id in allowed_channel_id:
		await ctx.send(f'```I am in {len(botclient.guilds)} servers with {len(botclient.users)} members.\n\nI am running on discord.py version {discord.__version__} and python version {platform.python_version()}\n\nI am running on {platform.system()} {platform.release()}\n\n```')

###
@botclient.command()
async def disclaimer(ctx):
	if ctx.channel.id in allowed_channel_id:
		embed = discord.Embed(colour = defaultColour, title = 'Disclaimer')
		embed.add_field(name='Usage of this bot requires understanding of the following:', value='This bot is for educational and personal use. As we cannot control what the bot is used for, we take no responsibility for repercussions as a result of the use of the bot. Thank you for understanding.', inline=False)
		await ctx.send(embed=embed)


@botclient.command()
async def redeem(ctx):
	global codes
	global count
	def check(author):
		def inner_check(message):
			return message.author == author
		return inner_check
	if ctx.channel.id in allowed_channel_id:
		embed=discord.Embed(colour = defaultColour, title=f"Please enter your issued code:", description="If you don't have a code, this command won't apply to you.")
		await ctx.send(embed=embed)
		msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
		msgcontent = msg.content
		found = False
		file = open("codes.txt", "r")
		codes = file.readline()
		count = file.readline()
		codes = codes.replace("\n", "")
		codes = list(codes.split(" "))
		count = list(count.split(" "))
		await msg.delete()
		if msgcontent in codes:
			found = True

		if found == True:
			index = codes.index(msgcontent)
			codeCount=count[index]
			codeCount=int(codeCount)
			if codeCount > 1:
				codeCountNew=codeCount-1
				count[index]=codeCountNew
				codes = ' '.join(codes)
				count = ' '.join(str(e) for e in count)
				codes=(f"{codes}\n")
				file = open('codes.txt', 'w')
				file.truncate()
				file.close()
				file = open('codes.txt', 'w')
				file.write(codes)
				file.write(count)
				file.close
				embed = discord.Embed(title=f'Valid code entered', colour = greenColour)
				message = await ctx.send(embed=embed)
				member = msg.author
				ROLE = "Silver"
				role = get(member.guild.roles, name=ROLE)
				await member.add_roles(role)
				await asyncio.sleep(3)
				await message.delete()
				channel = botclient.get_channel(844109788723150859)
				embed=discord.Embed(colour = defaultColour, title=f"Successfuly redeemed a code:", description=f'User: <@{ctx.author.id}> Count: {codeCountNew}')
				embed.add_field(name='Mode:', value='redeem', inline=False)
				await channel.send('<@&844109788723150859>', embed=embed)
				
			else:
				codes.remove(msgcontent)
				count.pop(index)
				codes = ' '.join(codes)
				count = ' '.join(str(e) for e in count)
				codes=(f"{codes}\n")
				file = open('codes.txt', 'w')
				file.truncate()
				file.close()
				file = open('codes.txt', 'w')
				file.write(codes)
				file.write(count)
				file.close
				embed = discord.Embed(title=f'Valid code entered', colour = greenColour)
				message = await ctx.send(embed=embed)
				member = msg.author
				ROLE = "Redeemer"
				role = get(member.guild.roles, name=ROLE)
				await member.add_roles(role)
				await asyncio.sleep(3)
				await message.delete()
				channel = botclient.get_channel(844109788723150859)
				embed=discord.Embed(colour = defaultColour, title=f"Successfuly redeemed a code:", description=f'User: <@{ctx.author.id}> Count: {codeCount}')
				embed.add_field(name='Mode:', value='redeem', inline=False)
				await channel.send('<@&844109788723150859>', embed=embed)
				embed=discord.Embed(colour = defaultColour, title=f"Code has run out", description=f'Code: {msgcontent}')
				embed.add_field(name='Mode:', value='redeem', inline=False)
				await channel.send('<@&844109788723150859>', embed=embed)



		else:
			embed = discord.Embed(title=f'Not a valid code', colour = redColour)
			message = await ctx.send(embed=embed)
			await asyncio.sleep(3)
			await message.delete()
			channel = botclient.get_channel(844109788723150859)
			embed=discord.Embed(colour = defaultColour, title=f"Attempted, and failed, to redeem a code:", description=f'User: <@{ctx.author.id}>')
			embed.add_field(name='Mode:', value='redeem', inline=False)
			await channel.send('<@&844109788723150859>', embed=embed)
	
	else:
		raid.reset_cooldown(ctx)
		embed = discord.Embed(title=f'You can only use bot commands in #bot', colour = redColour)
		message = await ctx.send(embed=embed)
		await asyncio.sleep(10)
		await message.delete()


# @botclient.command(aliases=['Play'])
# async def play(ctx):

# 	def check(author):
# 		def inner_check(message):
# 			return message.author == author
# 		return inner_check

# 	embed=discord.Embed(colour = defaultColour, title=f"Please specify the code of the game you would like to play", description='This will timeout in 30 seconds...')
# 	await ctx.send(embed=embed)
# 	msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
# 	code = msg.content

# 	embed=discord.Embed(colour = defaultColour, title=f"What would you like your name to be?", description='This will timeout in 30 seconds...')
# 	await ctx.send(embed=embed)
# 	msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
# 	username = msg.content

# 	embed=discord.Embed(colour = defaultColour, title=f"You're in!", description='See your nickname on screen?')
# 	embed.add_field(name='Code:',value=code)
# 	embed.add_field(name='Nickname:',value=username)
# 	await ctx.send(embed=embed)

# 	bot = client()
# 	bot.join(code,username)
# 	def joinHandle():
# 		pass
	
# 	def question():
# 		question.answer(0)
	
# 	bot.on("joined",joinHandle)
# 	# client.on("Joined",()=>{console.log("Joined!")});
# 	bot.on("QuizStart",question())

###
@commands.cooldown(1, 120, commands.BucketType.user)
@botclient.command(aliases=['Raid', 'spam', 'Spam'])
async def raid(ctx, code=None):
	if ctx.channel.id in allowed_channel_id:

		role = discord.utils.get(ctx.guild.roles, name="Developers")
		if role in ctx.author.roles:
			raid.reset_cooldown(ctx)
		
		def check(author):
			def inner_check(message):
				return message.author == author
			return inner_check

		if code == None:
			embed=discord.Embed(colour = defaultColour, title=f"Please specify the code of the game you would like to raid", description='This will timeout in 30 seconds...')
			embed.add_field(name='\n__**Be Aware:**__', value='Spamming of the bot (excesive bypassing of the 100-250 bot limit) will trigger temporary blacklisting.', inline=True)
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
			code = msg.content

		embed=discord.Embed(colour = defaultColour, title=f"What mode would you like to use?", description='This will timeout in 30 seconds...')
		embed.add_field(name='`customname` or `c`', value='Join bots to a lobby with your own set name. (Kahoot automatically filters inappropriate names).', inline=True)
		embed.add_field(name='`randomname` or `r`', value='Join bots to a lobby with unique random names.', inline=True)
		embed.add_field(name='`sentence` or `s`', value='Have inputed sentence display as seperate bots.', inline=True)
		embed.add_field(name='`insult` or `i`', value='Have an insult directed at target of your choice.', inline=True)
		embed.add_field(name='`asciiface` or `a`', value='Join many bots to a room with random random ascii emojis.', inline=True)	
		await ctx.send(embed=embed)
		msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
		option = msg.content

		### Custom Usernames
		if option == 'customname' or option == 'Customname' or option == 'c' or option == 'C':
			embed=discord.Embed(colour = defaultColour, title=f"What would you like the bot's name to be?", description='This will timeout in 30 seconds...')
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
			username = msg.content

			role = discord.utils.get(ctx.guild.roles, name="Developer")
			if role in ctx.author.roles:
				raid.reset_cooldown(ctx)
			else:
				username=username[0:10]
			
			embed=discord.Embed(colour = defaultColour, title=f"How many bots would you like to join your room? 1 - 150 (or 1 - 600 with a higher rank)", description='This will timeout in 30 seconds and will default to 150 (or higher with a higher rank) if number entered is to high...')
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
			botnum = msg.content
			botnum = int(botnum)

			changed = False

			role = discord.utils.get(ctx.guild.roles, name="Bronze")
			if role in ctx.author.roles:
				if botnum > 250:
					botnum = 250
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Silver")
			if role in ctx.author.roles:
				if botnum > 350:
					botnum = 350
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Gold")
			if role in ctx.author.roles:
				if botnum > 450:
					botnum = 450
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Diamond")
			if role in ctx.author.roles:
				if botnum > 600:
					botnum = 600
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Redeemer")
			if role in ctx.author.roles:
				if botnum > 300:
					botnum = 300
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Developers")
			if role in ctx.author.roles:
				changed = True

			if not changed:
				if botnum > 150:
					botnum = 150
				
			estseconds = 0.17 * botnum

			embed=discord.Embed(colour = orangeColour, title=f"Starting {botnum} bots joining...", description=f'Estimated time: {estseconds} seconds')
			await ctx.send(embed=embed)

			i = 1
			while i <= botnum:
				name = f"{username} {i}"
				i += 1
				bot = client()
				bot.join(code,name)
				def joinHandle():
					pass
				bot.on("joined",joinHandle)
			print(f'[{time()}] Successfuly joined lobby ({code}) with {botnum} bots. User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')

			channel = botclient.get_channel(785465225142730773)
			embed=discord.Embed(colour = defaultColour, title=f"Successfuly joined lobby ({code}) with {botnum} bots.", description=f'User: <@{ctx.author.id}>')
			embed.add_field(name='Mode:', value='customname', inline=False)
			await channel.send('<@&785464020961460245>', embed=embed)

			embed=discord.Embed(colour = greenColour, title="Finished joining bots...")
			await ctx.send(embed=embed)

		### Radnomised Usernames
		if option == 'randomname' or option == 'Randomname' or option == 'R' or option == 'r':

			embed=discord.Embed(colour = defaultColour, title=f"How many bots would you like to join your room? 1 - 150 (or 1 - 600 with higher rank)", description='This will timeout in 30 seconds and will default to 150 (or higher with higher rank) if number entered is to high...')
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
			botnum = msg.content
			botnum = int(botnum)

			changed = False

			role = discord.utils.get(ctx.guild.roles, name="Bronze")
			if role in ctx.author.roles:
				if botnum > 250:
					botnum = 250
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Silver")
			if role in ctx.author.roles:
				if botnum > 350:
					botnum = 350
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Gold")
			if role in ctx.author.roles:
				if botnum > 450:
					botnum = 450
					changed = True
			role = discord.utils.get(ctx.guild.roles, name="Diamond")
			if role in ctx.author.roles:
				if botnum > 600:
					botnum = 600
					changed = True

			role = discord.utils.get(ctx.guild.roles, name="Developers")
			if role in ctx.author.roles:
				changed = True

			if not changed:
				if botnum > 150:
					botnum = 150

			estseconds = 0.17 * botnum

			embed=discord.Embed(colour = orangeColour, title=f"Starting {botnum} bots joining...", description=f'Estimated time: {estseconds} seconds')
			await ctx.send(embed=embed)

			i = 1

			async with aiohttp.ClientSession() as cs:
				async with cs.get(f'https://random-word-api.herokuapp.com/word?number={botnum}') as data:
					ranstri = (await data.json())
			for i in ranstri:
				bot = client()
				bot.join(code,i)
				def joinHandle():
					pass
				bot.on("joined",joinHandle)

			print(f'[{time()}] Successfuly joined lobby ({code}) with {botnum} bots. User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')

			channel = botclient.get_channel(785465225142730773)
			embed=discord.Embed(colour = defaultColour, title=f"Successfuly joined lobby ({code}) woth {botnum} bots.", description=f'User: <@{ctx.author.id}>')
			await channel.send('<@&785464020961460245>', embed=embed)
			embed.add_field(name='Mode:', value='randomname', inline=False)
			embed=discord.Embed(colour = greenColour, title="Finished joining bots...")
			await ctx.send(embed=embed)	

		### Custom Sentences
		if option == 'sentence' or option == 'Sentence' or option == 'S' or option == 's':
			embed=discord.Embed(colour = defaultColour, title=f"Please enter your sentence:", description='This will timeout in 60 seconds...')
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=60)
			my_string = msg.content
			role = discord.utils.get(ctx.guild.roles, name="Basic")
			if role in ctx.author.roles:
				raid.reset_cooldown(ctx)
			else:
				my_string=my_string[0:100]
				my_string=my_string.split()[0:30]
				my_string = ' '.join([str(elem) for elem in my_string]) 

			def Convert(string): 
				li = list(string.split(" ")) 
				return li 
			reversed_string = " ".join(my_string.split(" ")[::-1])
			converted = (Convert(reversed_string)) 

			embed=discord.Embed(colour = orangeColour, title="Started creating your sentence", description=f'Estimated time: 5 seconds')

			await ctx.send(embed=embed)
			repeat = []
			num=1
			botnum=0
			for i in converted:
				bot = client()
				if i in repeat:
					bot.join(code,f"{i} {num}")
					num=num+1
				else:
					bot.join(code,f"{i}")
					repeat.append(i)
				def joinHandle():
					pass
				bot.on("joined",joinHandle)
				await asyncio.sleep(0.5)
				botnum=botnum+1

			print(f'[{time()}] Successfuly joined lobby ({code}) with {botnum} bots. User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')
			channel = botclient.get_channel(785465225142730773)
			embed=discord.Embed(colour = defaultColour, title=f"Successfuly joined lobby ({code}) with {botnum} bots.", description=f'User: <@{ctx.author.id}>')
			embed.add_field(name='Mode:', value='sentence', inline=False)
			await channel.send('<@&785464020961460245>', embed=embed)

			embed=discord.Embed(colour = greenColour, title="Finished joining the room and created your sentence")
			await ctx.send(embed=embed)
			
		### Random Targeted Insults
		if option == 'insult' or option == 'Insult' or option == 'I' or option == 'i':

			embed=discord.Embed(colour = defaultColour, title=f"Please enter the name of your target:", description='This will timeout in 30 seconds...')
			await ctx.send(embed=embed)
			msg = await botclient.wait_for('message', check=check(ctx.author), timeout=30)
			target = msg.content

			insult1 = ['humour', 'of', 'sense', 'a', 'has', 'God', 'that', 'proof', 'is', target]
			insult2 = ['shاt', 'like', 'smells', target]
			insult3 = ['alone', 'be', 'always', 'will', target]
			insult4 = ['friends', 'no', 'has', target]
			insult5 = ['maths', 'core', 'studying', 'is', target]

			embed=discord.Embed(colour = orangeColour, title=f"Starting bots joining...")
			await ctx.send(embed=embed)
			
			insultran=(random.randint(1,5))
			if insultran == 1:
				final=insult1
			elif insultran == 2:
				final=insult2
			elif insultran == 3:
				final=insult3
			elif insultran == 4:
				final=insult4
			elif insultran == 5:
				final=insult5

			for i in final:
				bot = client()
				bot.join(code,f"{i}")
				def joinHandle():
					pass
				bot.on("joined",joinHandle)
				await asyncio.sleep(1)
			print(f'[{time()}] Successfuly joined lobby ({code}). User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')
			
			channel = botclient.get_channel(785465225142730773)
			embed=discord.Embed(colour = defaultColour, title=f"Successfuly joined lobby ({code}) with insult mode.", description=f'User: <@{ctx.author.id}>')
			embed.add_field(name='Mode:', value='insult', inline=False)
			await channel.send('<@&785464020961460245>', embed=embed)

			embed=discord.Embed(colour = greenColour, title="Finished joining the room and created insult")
			await ctx.send(embed=embed)
			
		### Randomised Ascii
		if option == 'asciiface' or option == 'Asciiface' or option == 'a' or option == 'A':
			ranstri = ['V●ᴥ●V', '◖⚆ᴥ⚆◗', '(✪㉨✪)', '(￣(ｴ)￣)', '(=^･ｪ･^=)', 'ʕ ꈍᴥꈍʔʕ·ᴥ·ʔ', '(・(ｪ)・）',
			'(＾∇＾)', '(☉｡☉)!', 'ლ(^o^ლ)', '(‘◉⌓◉’)', '(｡◕o◕｡)', 'ヽ((◎д◎))ゝ', '(ノ￣皿￣)ノ', 'ヘ(￣ω￣ヘ)', 
			'◝( •௰• )◜', '♪┌|∵|┘♪', '乁( •_• )ㄏ', '⌐■-■', '(ノಥ,_｣ಥ)ノ', '(┛ಸ_ಸ)┛彡┻━┻',
			'(ノ•̀ o •́ )ノ ~ ┻━┻', '┻━┻┻┻︵¯\(ツ)/¯︵┻┻', 'ゞ(─.─)', '(ノT＿T)ノ ＾┻━┻┻┻', '(๑´•.̫ • ๑)', '( ≧Д≦)',
			'(ノಠ益ಠ)ノ彡┻━┻┻┻', '¯\_(⊙_ʖ⊙)_/¯', '(๑¯◡¯๑)', '┌( ͝° ͜ʖ͡°)=ε/̵͇̿̿/’̿’̿ ̿']
			
			botnum = len(ranstri)
				
			estseconds = 0.36 * botnum

			embed=discord.Embed(colour = orangeColour, title=f"Starting bots joining...", description=f'Estimated time: {estseconds} seconds')
			await ctx.send(embed=embed)
			repeat = 0
			def joinHandle():
				pass
			rnum=[i for i in range(0, botnum)]
			while repeat < botnum:
				bot = client()
				number = random.choice(rnum)
				chosen = ranstri[number]
				bot.join(code,f"{chosen}")
				rnum.remove(number)
				bot.on("joined",joinHandle)
				repeat=repeat+1

			embed=discord.Embed(colour = greenColour, title="Finished joining bots...")
			await ctx.send(embed=embed)
			print(f'[{time()}] Successfuly joined lobby ({code}). User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})')

			channel = botclient.get_channel(785465225142730773)
			embed=discord.Embed(colour = defaultColour, title=f"Successfuly joined lobby ({code}).", description=f'User: <@{ctx.author.id}>')
			embed.add_field(name='Mode:', value='ascii', inline=False)
			await channel.send('<@&785464020961460245>', embed=embed)
	else:
		raid.reset_cooldown(ctx)
		embed = discord.Embed(title=f'You can only use bot commands in #bot', colour = redColour)
		message = await ctx.send(embed=embed)
		await asyncio.sleep(10)
		await message.delete()

@raid.error
async def raid_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f'You must wait another {round(error.retry_after)} seconds before you can use this command again.',colour = redColour)
        await ctx.send(embed=embed)

botclient.run('ODQzNzc1MDM3ODMwOTg3ODE2.YKIwvQ.brkpNuGqpN5iXvhcC1P6Sx9fJwQ')
