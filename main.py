from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from re import findall

channel, src, budget, secs = 0, 0, 0, 0
headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
        }

def priceToInt(string):
    return int(findall(r'\d+', string)[0])

def scrap_VivaReal(link):
    apDict = {}
    global headers
    site = requests.get(link, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    apList = soup.find_all('div', class_="js-card-selector")

    for ap in apList:
        title = ap.find('span', class_="property-card__title js-cardLink js-card-title").get_text()
        adress = ap.find('span', class_="property-card__address").get_text()
        rent = ap.find('div', class_="property-card__price js-property-card-prices js-property-card__price-small").get_text()
        condo = 0 #ap.find('div', class_="property-card__price-details--condo").get_text()
        path = ap.find('a', class_="property-card__labels-container js-main-info js-listing-labels-link")['href']
        img = ap.find('img', class_="carousel__image js-carousel-image")["src"]

        apDict[apList.index(ap)] = [title, img, adress, rent, condo, "https://www.vivareal.com.br/"+path]
        
    return apDict

bot = commands.Bot("!")

@bot.event
async def on_ready():
    print("I'm Ready!")

@bot.command(name="start")
async def botConfig(ctx, path, price, time):
    global channel, src, budget, secs

    botSearch.start()
    await ctx.send(f"O bot estará pesquisando, a cada {time} horas, aluguéis de até R${price} no site {path}.")
    channel = ctx.channel
    src = path
    budget = price
    secs = time*3600

@bot.command(name="stop")
async def botStop(ctx):
    botSearch.stop()

    await ctx.send("O bot parou")

@tasks.loop(seconds=20)
async def botSearch():
    print("rodou")
    global channel, src, budget
    aps = scrap_VivaReal(src)
    for keys, values in aps.items():
        if priceToInt(values[3]) <= int(budget):
            await channel.send(f"{values[1]}\n{values[0]}\n{values[2]}\n{values[3]}\n{values[4]}\n{values[5]}")

bot.run("token")