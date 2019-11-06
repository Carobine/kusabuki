import discord
from discord.ext import commands
from lxml import html, etree
import re
import requests
import fileinput

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def link(ctx, query):
    await ctx.send(link_helper(query))

@bot.command()
async def embedtest(ctx):
    embed = discord.Embed(
        title = 'Title'
    )
    await ctx.send(embed=embed)


# Teleram history scraper
files = ['telegram_history/messages.html','telegram_history/messages2.html','telegram_history/messages3.html', 'telegram_history/messages4.html']

title_ids = []
gdrive_links = []

for messages_part in files:
    part = open(messages_part, encoding='utf8').read()
    title_ids.extend(re.findall('(?<=\[)0100\w{12}(?=\])', part))
    gdrive_links.extend(re.findall('(?<=<a href=")https://drive.google.com/a/\w.+export=download(?=">)', part))

print(len(title_ids), "titles found")
print(len(gdrive_links), "links loaded")
if (len(title_ids) == len(gdrive_links)):
    print("Link enumeration appears successful!")
else:
    print("ERROR: Titleid/link mismatch. You may receive the wrong link!")


# Switchbrew scraper
page = requests.get("https://switchbrew.org/wiki/Title_list/Games")
brewtree = html.fromstring(page.content)
brew_titleids_html = brewtree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr/td[1]')
brew_gamenames = brewtree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr/td[2]/text()') 
# Required because text() will not match empty table entries
brew_titleids = [element.text for element in brew_titleids_html]
print(len(brew_titleids), "Switchbrew titleids found")
print(len(brew_gamenames), "Switchbrew game titles found")
if (len(brew_gamenames) == len(brew_titleids)):
    print("Game lookup enumeration appears successful!")
else:
    print("ERROR: Lookup table mismatch. You may receive the wrong game info!")


def link_helper(query):
    try:
        link = gdrive_links[title_ids.index(query)]
    except ValueError:
        return "Sorry! Game not found."
    gamename = brew_gamenames[brew_titleids.index(query)]

    string = "**Found Game!**\n" + gamename + "\n" + link
    return string

bot.run('token')
