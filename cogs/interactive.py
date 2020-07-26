import datetime
import random
from contextlib import closing

from discord import Colour, Embed, Member
from discord.ext import commands
from discord.ext.commands import cooldown, command, BucketType, bot_has_permissions

import db
from settings import colour_list


# Gets the member and user avatar
def getMember(ctx):
    # Set member as the author
    member = ctx.message.author
    # Get the member avatar
    userAvatar = member.avatar_url

    return member, userAvatar


# Set up the Cog
class Interactive(commands.Cog):
    """Interactive Commands! (E.G Kiss/Hug/Cuddle)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @command(name="kiss", aliases=["Kiss"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def kiss(self, ctx, member: Member):
        """Kiss your Partner"""

        # Get the guild
        guild = ctx.author.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = ctx.author.id, guild.id,
            with closing(conn.cursor()) as cursor:

                # Execute the SQL Query
                cursor.execute(select_query, val)
                result = cursor.fetchone()
                married_user = result[1]

            # Error handling to make sure that the user can kiss themselves
            if member.id == ctx.author.id:
                kiss = False
                title = f":kissing_heart: :kissing_heart: | **{ctx.author.name}** kissed **themselves**"
            else:
                kiss = True
                title = f":kissing_heart: :kissing_heart: | **{ctx.author.name}** kissed **{member.display_name}**"

        try:
            # Make sure the user isn't trying to kiss someone else besides their partner
            if married_user is None and kiss:
                await ctx.send("Σ(‘◉⌓◉’) You need to be married in order to use this command! Baka!")
                return
            # Make sure that the married people can only kiss their partner
            elif not str(member.id) == married_user and kiss:
                await ctx.send("Σ(‘◉⌓◉’) You can only kiss your partner! Baka!")
                return
        except Exception as ex:
            print(ex)

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the kissing gifs
            with open('images/FunCommands/kissing.txt') as file:
                # Store content of the file in kissing_array
                kissing_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random kissing gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(kissing_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="cuddle", aliases=["Cuddle"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def cuddle(self, ctx, member: Member):
        """Cuddle your Partner"""

        # Get the guild
        guild = ctx.author.guild

        # Use database connection
        with db.connection() as conn:

            # Get the author's row from the Members Table
            select_query = """SELECT * FROM members WHERE discordID = (?) and guildID = (?)"""
            val = ctx.author.id, guild.id
            with closing(conn.cursor()) as cursor:

                # Execute the SQL Query
                cursor.execute(select_query, val)
                result = cursor.fetchone()
                married_user = result[1]

            # Error handling to make sure that the user can cuddle themselves
            if member.id == ctx.author.id:
                cuddle = False
                title = f":blush: :blush: | **{ctx.author.name}** cuddled **themselves**"
            else:
                cuddle = True
                title = f":blush: :blush: | **{ctx.author.name}** cuddled **{member.display_name}**"

        try:
            # Make sure the user isn't trying to cuddle someone else besides their partner
            if married_user is None and cuddle:
                await ctx.send("Σ(‘◉⌓◉’) You need to be married in order to use this command! Baka!")
                return
            # Make sure that the married people can only cuddle their partner
            elif not str(member.id) == married_user and cuddle:
                await ctx.send("Σ(‘◉⌓◉’) You can only cuddle your partner! Baka!")
                return
        except Exception as ex:
            print(ex)

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the cuddling gifs
            with open('images/FunCommands/cuddling.txt') as file:
                # Store content of the file in cuddling_array
                cuddling_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random cuddling gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(cuddling_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="kill", aliases=["Kill"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def kill(self, ctx, member: Member):
        """Kill a Member"""

        if member is ctx.author:
            title = f":scream: :scream: | **{ctx.author.name}** killed **themselves**"
        else:
            title = f":scream: :scream: | **{ctx.author.name}** killed **{member.display_name}**"

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the killing gifs
            with open('images/FunCommands/killing.txt') as file:
                # Store content of the file in killing_array
                killing_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random killing gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(killing_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="slap", aliases=["Slap"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def slap(self, ctx, member: Member):
        """Slap a Member"""

        if member is ctx.author:
            title = f":cold_sweat: :cold_sweat: | **{ctx.author.name}** slapped **themselves**"
        else:
            title = f":cold_sweat: :cold_sweat: | **{ctx.author.name}** slapped **{member.display_name}**"

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the cuddling gifs
            with open('images/FunCommands/slapping.txt') as file:
                # Store content of the file in cuddling_array
                slapping_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random slapping gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(slapping_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="pat", aliases=["Pat"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def pat(self, ctx, member: Member):
        """Pat a Member"""

        if member is ctx.author:
            title = f"👉 👈 | **{ctx.author.name}** patted **themselves**"
        else:
            title = f"👉 👈 | **{ctx.author.name}** patted **{member.display_name}**"

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the patting gifs
            with open('images/FunCommands/patting.txt') as file:
                # Store content of the file in patting_array
                patting_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random patting gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(patting_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="lemon", aliases=["Lemon"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def lemon(self, ctx, member: Member):
        """Give Lemon to Member"""

        if member is ctx.author:
            title = f":relaxed: :relaxed: | **{ctx.author.name}** gave a lemon to **themselves**"
        else:
            title = f":relaxed: :relaxed: | **{ctx.author.name}** gave a lemon to **{member.display_name}**"

        lemon_array = ["https://media.discordapp.net/attachments/669812887564320769/720093589056520202/lemon.gif",
                       "https://media.discordapp.net/attachments/669812887564320769/720093575492272208/lemon2.gif",
                       "https://media.discordapp.net/attachments/718484280925224981/719629805263257630/lemon.gif"]

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random lemon gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(lemon_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="choke", aliases=["Choke"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def choke(self, ctx, member: Member):
        """Choke a Member"""

        if member is ctx.author:
            title = f":confounded: :confounded: | **{ctx.author.name}** choked **themselves**"
        else:
            title = f":confounded: :confounded: | **{ctx.author.name}** choked **{member.display_name}**"

        # Surround with try/except to catch any exceptions that may occur
        try:
            # Open the file containing the choking gifs
            with open('images/FunCommands/choking.txt') as file:
                # Store content of the file in choking_array
                choking_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random choking gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(choking_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)

    @command(name="hug", aliases=["Hug"])
    @bot_has_permissions(embed_links=True)
    @cooldown(1, 1, BucketType.user)
    async def hug(self, ctx, member: Member):
        """Hug a Member"""

        if member is ctx.author:
            title = f":smiling_face_with_3_hearts: :smiling_face_with_3_hearts: | **{ctx.author.name}** hugged **themselves**"
        else:
            title = f":smiling_face_with_3_hearts: :smiling_face_with_3_hearts: | **{ctx.author.name}** hugged **{member.display_name}**"

        # Surround with try/except to catch any exceptions that may occur
        try:

            # Open the file containing the hug gifs
            with open('images/FunCommands/hugging.txt') as file:
                # Store content of the file in hugging_array
                hugging_array = file.readlines()

            # Get the member and the userAvatar
            member, userAvatar = getMember(ctx)

            # Set up the embed to display a random hugging gif
            embed = Embed(
                title=title,
                colour=Colour(int(random.choice(colour_list))),
                timestamp=datetime.datetime.utcnow())
            embed.set_image(url=random.choice(hugging_array))
            embed.set_footer(text=f"Requested by {member}", icon_url='{}'.format(userAvatar))

            # Send the embedded message to the user
            await ctx.send(embed=embed)

        except FileNotFoundError as e:
            print(e)


def setup(bot):
    bot.add_cog(Interactive(bot))
