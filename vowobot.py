import discord, io, datetime
import osu, database, person, gacha
from discord.ext import commands, tasks

#Add token here
token = "1"
bot = commands.Bot(command_prefix='<')
bot.remove_command('help')

#Add osu API key in config.txt
osu = osu.osuStats(open('config.txt', 'r').readline())
gacha = gacha.gachaStats(0, 0)
database = database.tracker()

@bot.event
async def on_ready():
    print('Ready.')
    database.readFile()
    
@bot.event
async def on_message(message):
    #When Josh talks
    if message.author.id == 378119119641378816:
        await message.channel.send('Shut the fuck up.')

    await bot.process_commands(message)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()
    
@tasks.loop(seconds=1)
async def checkBirthday():
    birthdays = [['Oli', (7, 9), '602920463349448711'], ['Khai-Yiu', (24, 10), '193695647239503872'], ['Han', (9, 11), '693345437087825953'],
                 ['Yu', (31, 12), '186780504060723200'], ['Rafid', (1, 1), '704201715607404604'], ['Thong', (27, 2), '223761488756604928'],
                 ['Josh', (10, 5), '378119119641378816'], ['Ibrahim', (22, 5), '319314559162908676']]
    channel = bot.get_channel(751540495582494833)
    timeObj = datetime.datetime.now()
    month, day, hour, min, sec = timeObj.month, timeObj.day, timeObj.hour, timeObj.minute, timeObj.second

    for person in birthdays:
        user = '<@' + person[2] + '>'
        if month == person[1][1] and day == person[1][0] and hour == 0 and min == 0 and sec == 0:
            await channel.send(':partying_face: ' + user + ' :birthday:')
            embed = discord.Embed(title='Happy Birthday, ' + person[0] + '!')
            embed.set_image(url='https://cdn.discordapp.com/attachments/395539967402704897/774948424604713020/pika2.gif')
            await channel.send(embed=embed)

@checkBirthday.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
    
@bot.command(pass_context=True, name='help')
async def help(ctx):
    await ctx.send(':hammer: Commands:\n' + \
                   '```osu!:\n' + \
                   'top, score, recent```\n' + \
                   '```Genshin Impact:\n' + \
                   'pull```')

@bot.command(pass_context=True, name='top')
async def top(ctx, user):
    #best score info
    data = osu.getUserBest(user, '0')
    
    if len(data) != 0:
        mapUrl = 'https://old.ppy.sh/b/' + data['beatmap_id'] + '?m=0'
        #user info for profile pic
        userdata = osu.getUser(user, '0')
        #map info for image
        mapdata = osu.getBeatmaps(mapUrl, str(osu.getMods(data['enabled_mods'])[1]))
        mapUrl = 'https://old.ppy.sh/b/' + data['beatmap_id'] + '?m=0'
        embed = discord.Embed(title='#1 for ' + user,
                              description='**' + mapdata['title'] + ' [' + mapdata['version'] + '] +' + osu.getMods(data['enabled_mods'])[0] + ' (' + str(round(float(mapdata['difficultyrating']), 2)) + ' :star:)**',
                              colour = discord.Colour.blue())
        
        embed.set_footer(text=mapUrl)
        embed.add_field(name='Rank:', value = data['rank'], inline=True)
        embed.add_field(name='Combo:', value = data['maxcombo'] + 'x/' + mapdata['max_combo'] + 'x', inline=True)
        embed.add_field(name='激/喝/50/Misses:', value = data['count300'] + '/' + data['count100'] + '/' + data['count50'] + '/' + data['countmiss'], inline=True)
        embed.add_field(name='Accuracy:', value = str(osu.calcAccuracy(int(data['count300']), int(data['count100']), int(data['count50']), int(data['countmiss']))) + '%', inline=True)
        embed.add_field(name='PP:', value = data['pp'], inline=True)
        embed.add_field(name='Date set:', value = osu.reformatDate(data['date']), inline=True)
        embed.set_thumbnail(url='http://s.ppy.sh/a/' + userdata['user_id'])
        embed.set_image(url='https://assets.ppy.sh/beatmaps/' + mapdata['beatmapset_id'] + '/covers/cover.jpg')
        
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=user + ' is a non-existing user.',
                              colour = discord.Colour.blue())
        await ctx.send(embed=embed)
        
@bot.command(pass_context=True, name='score')
async def score(ctx, user, mapUrl):
    #score info
    data = osu.getScores(mapUrl, user, '0')
    
    if len(data) != 0:
        #user info for profile pic
        userdata = osu.getUser(user, '0')
        #map info
        mapdata = osu.getBeatmaps(mapUrl, str(osu.getMods(data['enabled_mods'])[1]))
        embed = discord.Embed(title=user,
                              description='**' + mapdata['title'] + ' [' + mapdata['version'] + '] +' + osu.getMods(data['enabled_mods'])[0] + ' (' + str(round(float(mapdata['difficultyrating']), 2)) + ' :star:)**',
                              colour = discord.Colour.green())
        
        embed.set_footer(text=mapUrl)
        embed.add_field(name='Score:', value = data['score'], inline=True)
        embed.add_field(name='Combo:', value = data['maxcombo'] + 'x/' + mapdata['max_combo'] + 'x', inline=True)
        embed.add_field(name='激/喝/50/Misses:', value = data['count300'] + '/' + data['count100'] + '/' + data['count50'] + '/' + data['countmiss'], inline=True)
        embed.add_field(name='Rank:', value = data['rank'], inline=True)
        embed.add_field(name='Accuracy:', value = str(osu.calcAccuracy(int(data['count300']), int(data['count100']), int(data['count50']), int(data['countmiss']))) + '%', inline=True)
        embed.add_field(name='PP:', value = data['pp'], inline=True)
        embed.set_thumbnail(url='http://s.ppy.sh/a/' + userdata['user_id'])
        embed.set_image(url='https://assets.ppy.sh/beatmaps/' + mapdata['beatmapset_id'] + '/covers/cover.jpg')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=user + ' does not have a score on this map.',
                              colour = discord.Colour.green())
        await ctx.send(embed=embed)
        
@bot.command(pass_context=True, name='recent')
async def recent(ctx, user):
    data = osu.getUserRecent(user, '0')
    
    if len(data) != 0:
        mapUrl = 'https://old.ppy.sh/b/' + data['beatmap_id'] + '?m=0'
        userdata = osu.getUser(user, '0')
        mapdata = osu.getBeatmaps(mapUrl, str(osu.getMods(data['enabled_mods'])[1]))
        embed = discord.Embed(title='Most recent play for ' + user,
                              description = '**' + mapdata['title'] + ' [' + mapdata['version'] + '] +' + osu.getMods(data['enabled_mods'])[0] + ' (' + str(round(float(mapdata['difficultyrating']), 2)) + ' :star:)**',
                              colour = discord.Colour.red())
        
        embed.set_footer(text=mapUrl)
        embed.add_field(name='Rank: ', value = data['rank'], inline=True)
        embed.add_field(name='Combo:', value = data['maxcombo'] + 'x/' + mapdata['max_combo'] + 'x', inline=True)
        embed.add_field(name='激/喝/50/Misses:', value = data['count300'] + '/' + data['count100'] + '/' + data['count50'] + '/' + data['countmiss'], inline=True)
        embed.add_field(name='Accuracy:', value = str(osu.calcAccuracy(int(data['count300']), int(data['count100']), int(data['count50']), int(data['countmiss']))) + '%', inline=True)
        embed.add_field(name='Time set:', value = osu.diffTime(data['date']), inline=True)
        embed.set_thumbnail(url='http://s.ppy.sh/a/' + userdata['user_id'])
        embed.set_image(url='https://assets.ppy.sh/beatmaps/' + mapdata['beatmapset_id'] + '/covers/cover.jpg')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=user + ' has not played recently.',
                              colour = discord.Colour.red())
        await ctx.send(embed=embed)
        
@bot.command(pass_context=True, name='pull')
async def pull(ctx):
    person = database.getPerson(ctx.message.author.id)
    
    if (person is not None):
        gacha.setPity(person.purplePity, person.yellowPity)
        gachaImg = gacha.multiPull()
        byteArray = io.BytesIO()
        gachaImg.save(byteArray, format='PNG')
        byteArray.seek(0)
        await ctx.send(file=discord.File(byteArray, 'gachaImg.png'))
    
        person.updatePity(gacha.purplePity, gacha.yellowPity)
        database.updateDatabase(person)
        database.writeFile()

checkBirthday.start()  
bot.run(token)