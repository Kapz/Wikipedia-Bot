import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import wikipedia
from random import randint


bot = commands.Bot(command_prefix="/w ") #You can edit it to whatever you want
client = discord.Client()
bot.remove_command('help') #Removes help so we can add our own version of it



current_language = "en" #Default language



@bot.event
async def on_ready():
    print("Bot in server: {}".format("Succes"))
    print("Bot name: {}".format(bot.user.name))




@bot.command(pass_context=True)
async def search(ctx):

    #Load current lang for picture
    global current_language

    #Get user input
    msg = ctx.message.content.split(" ")
    request = msg[2:]
    request = " ".join(request)
    error = None


    try:

        wikicontent = wikipedia.search(request, results=20, suggestion=False) #Wikipedia search request
        print(wikicontent)
        print(" ".join(wikicontent))

        #If there are no results
        if not wikicontent:
            wikicontent ="Sorry, there are no search results for '{}'.".format(request)
            embed = discord.Embed(title="Wikipedia search results:", color=0xe74c3c, description=wikicontent)
            embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await bot.say(embed=embed)

        #If there are do:
        else:
            embed = discord.Embed(title="Wikipedia search results:", color=0, description="\n".join(wikicontent))
            embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await bot.say(embed=embed)


    #Handle random errors
    except Exception as error:
        error = str(error)
        await bot.say("Sorry, a random error occurred. Please try again.")
        print(error)





@bot.command(pass_context=True)
async def display(ctx):

    global current_lang

    msg = ctx.message.content.split(" ")
    request = msg[2:]
    request = " ".join(request)


    #Checks if the request is valid
    try:
        pagecontent = wikipedia.page(request)
        pagetext = wikipedia.summary(request, sentences=5)


        #Try to get random image from the article to display.
        #If there are no pictures, it wil set it to the default wkikipedia picture
        try:
            thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]

        except:
            thumbnail = "https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language)


        embed = discord.Embed(title=request, color=0, description=pagetext + "\n\n[Read further]({})".format(pagecontent.url))
        embed.set_thumbnail(url=thumbnail)
        await bot.say(embed=embed)


    except wikipedia.DisambiguationError:

        NotSpecificRequestErrorMessage = """Sorry, your search request wasn't specific enough. Please try '/w search (your request)'. This will display all wikipedia articles with your search request. You can than copy the correct result and put that in /a display."""
        embed = discord.Embed(title="Bad request: ", color=0xe74c3c, description=NotSpecificRequestErrorMessage)
        embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
        await bot.say(embed=embed)

    except wikipedia.PageError:

        NoResultErrorMessage = "Sorry, there are no Wikipedia articles with this title. Please try '/w search (your request)' to look up Wikipedia article name's"
        embed = discord.Embed(title="Not found: ", color=0xe74c3c, description=NoResultErrorMessage)
        embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
        await bot.say(embed=embed)

    except:
        RandomErrorMessage = "Sorry, a random error occured"
        embed = discord.Embed(title="Error", color=0xe74c3c, description=RandomErrorMessage)
        embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
        await bot.say(embed=embed)
        #await bot.say(error)




@bot.command(pass_context=True)
async def lang(ctx):

    global current_language

    msg = ctx.message.content.split(" ")
    command = msg[2]
    langcodes = wikipedia.languages().keys()


    #Check which command to run
    if command == "list" or command == "List":

        #List of most used languages on wikipedia
        languagelist = "English / English = en\nCebuano / Sinugboanong = ceb\nSwedish / Svenska = sv\nGerman / Deutsch = de\nFrench / Français = fr\nDutch / Nederlands = nl\nRussian / Русский = ru\nItalian / Italiano = it\nSpanish / Español = es\nWaray-Waray / Winaray = war\nPolish / Polski = pl\nVietnamese / Tiếng Việt = vi\n Japanese / 日本語 = ja\n"
        languagelistwiki = "https://meta.wikimedia.org/wiki/List_of_Wikipedias"

        embed = discord.Embed(title="Wikipedia language list:", color=0, description=languagelist + "\n\nAll supported languages can be found [here]({})".format(languagelistwiki))
        embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
        await bot.say(embed=embed)


    elif command == "set" or command == "Set":

        #Check if the given language(langcode) is valid
        if msg[3] in langcodes:
            current_language = msg[3]
            wikipedia.set_lang(msg[3])

        else:
            embed = discord.Embed(title="Languages not found:", color=0xe74c3c, description="Sorry, the language '{}' was not found. Please run '/w lang list' to see all language codes.".format(msg[3]))
            embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await bot.say(embed=embed)



@bot.command(pass_context=True)
async def random(ctx):

    global current_language

    #Makes sure you will get an article.
    try:
        random_article = wikipedia.random(pages=1)

    except DisambiguationError:

        try:
            random_article = wikipedia.random(pages=1)
        except DisambiguationError:

            try:
                random_article = wikipedia.random(pages=1)

            except DisambiguationError:
                random_article = wikipedia.random(pages=1)



    pagecontent = wikipedia.page(random_article)
    pagetext = wikipedia.summary(random_article, sentences=5)


    #Try to set an random image in the article as the thumbnail
    try:
        thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]

    except Exception as error:
        thumbnail = "https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language)
        print("Couldn't load {}".format(thumbnail))


    embed = discord.Embed(title=random_article, color=0, description=pagetext + "\n\n[Read further]({})".format(pagecontent.url))
    embed.set_thumbnail(url=thumbnail)
    await bot.say(embed=embed)




@bot.command(pass_context=True)
async def about(ctx):

    #Just an about page
    github = "https://github.com/Kapz/Wikipedia-Bot"
    about = "{} is a bot made by Qubit#4222 with [Discord.py](https://github.com/Rapptz/discord.py) and the [Wikipedia Api](https://wikipedia.readthedocs.io/en/latest/code.html). All articles fall under the [Creative Commons Attribution-ShareAlike License](https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License). Special thanks to Wikipedia for making this possible. Please consider [donating](https://wikimediafoundation.org/wiki/Ways_to_Give) to the Wikipedia Foundation to keep the biggest free Encyclopedia alive. You can contribute to the bot on [github]({})\nThanks.".format(bot.user.name, github)
    embed = discord.Embed(title="About:", color=0, description=about + "\n\n[Wikipedia Official Site](https://en.wikipedia.org/wiki/Main_Page)")
    #embed.set_footer(text="")
    embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
    await bot.say(embed=embed)



@bot.command(pass_context=True)
async def help(ctx):

    #Help menu

    msg = ctx.message.content.split(" ")

    try:
        helpselect = msg[2]

        if helpselect == "search":
            await bot.say("```/w search 'term' - searches wikipedia on given term```")

        elif helpselect == "display":
            await bot.say("```/w display 'term' - displays the article with the given term```")

        elif helpselect == "lang":
            try:
                langhelp = msg[3]

                if langhelp == "list":
                    await bot.say("```/w lang list - displays wikipedia language options list```")

                elif langhelp == "set":
                    await bot.say("```/w lang set 'language code' - set's the language to the given code.\nCode can be found at /w lang list```")

                else:
                    await bot.say("```Oops, this looks like invalid input to me.\nPlease see '/w help lang'```")

            except:
                await bot.say("```/w help lang list\n/w help set```")


        elif helpselect == "random":
            await bot.say("```/w random - displays a random article based on the current language set```")


        elif helpselect == "about":
            await bot.say("```/w about - display's additional information```")

        else:
            await bot.say("```Oops, looks like invalid input to me.\nPlease see '/w help'```")



    except:
        await bot.say("```/w help search\n/w help display\n/w help lang\n/w help random\n/w help about```")





#Checks if the filled-in token is correct
try:
    bot.run("") #Put your token here

except discord.errors.LoginFailure:
    print("Incorrect token")
