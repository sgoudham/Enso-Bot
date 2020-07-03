import asyncio
import datetime
import random

from discord import DMChannel, Colour, Embed
from discord.ext import commands


# Method to send the prompt/embed to start sending modmail to the user
def startModMail(author):
    # Set up embed to let the user how to start sending modmail
    startModMailEmbed = Embed(title="**Welcome to Modmail!**",
                              colour=Colour(0xFF69B4),
                              timestamp=datetime.datetime.utcnow())

    startModMailEmbed.set_thumbnail(url=author.avatar_url)
    startModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("\u200b", "**React to this message if you want to send a message to the Staff Team!**", False),
              ("\u200b", "**Use :white_check_mark: for** `Yes`", True),
              ("\u200b", "**Use :x: for** `No`", True),
              ("\u200b", "\u200b", True),
              ("\u200b",
               "We encourage all suggestions/thoughts and opinions on the server! As long as it is **valid** criticism. "
               "Purely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        startModMailEmbed.add_field(name=name, value=value, inline=inline)

    return startModMailEmbed


# Method to ask the user if they want to be anonymous or not
def AnonOrNot(author):
    # Set up embed to let the user how to start sending modmail
    AnonModMailEmbed = Embed(title="**Want to send it Anonymously?**",
                             colour=Colour(0xFF69B4),
                             timestamp=datetime.datetime.utcnow())

    AnonModMailEmbed.set_thumbnail(url=author.avatar_url)
    AnonModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("\u200b", "**React to this message if you want to send a message to the Staff Team!**", False),
              ("\u200b", "**Use :white_check_mark: for** `Yes`", True),
              ("\u200b", "**Use :x: for** `No`", True),
              ("\u200b", "\u200b", True),
              ("\u200b",
               "This will make sure that Staff do not know who is sending the mail."
               "\nAgain, purely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        AnonModMailEmbed.add_field(name=name, value=value, inline=inline)

    return AnonModMailEmbed


# Method to send an embed to let the user know that they have aborted the modmail process
def Abort(author):
    # Get my user ID
    hammyID = '<@154840866496839680>'

    # Set up embed to let the user know that they have aborted the modmail
    AbortEmbed = Embed(title="**Aborting ModMail!**",
                       colour=Colour(0xFF69B4),
                       timestamp=datetime.datetime.utcnow())

    AbortEmbed.set_thumbnail(url=author.avatar_url)
    AbortEmbed.set_footer(text=f"Sent by {author}")

    fields = [("\u200b", "**If you change your mind, you can do `~mm` or `~modmail` at anytime!**", False),
              ("\u200b", f"If you want to speak to me personally, you can DM {hammyID} anytime!", True)]

    for name, value, inline in fields:
        AbortEmbed.add_field(name=name, value=value, inline=inline)

    return AbortEmbed


# Method to send an embed to to let the user know to type into chat
def SendInstructions(author):
    # Set up embed to let the user know that they have aborted the modmail
    SendModMailEmbed = Embed(title="**Please enter a message for it to be sent to the staff!**",
                             colour=Colour(0xFF69B4),
                             timestamp=datetime.datetime.utcnow())

    SendModMailEmbed.set_thumbnail(url=author.avatar_url)
    SendModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("\u200b", "**Make sure that the message is above 50 characters! Include as much detail as possible :P**",
               False)]

    for name, value, inline in fields:
        SendModMailEmbed.add_field(name=name, value=value, inline=inline)

    return SendModMailEmbed


# Method to actually allow the message to be sent to #mod-mail
def SendMsgToModMail(self, msg, author):
    if self.anon:

        avatars = ["https://cdn.discordapp.com/embed/avatars/0.png",
                   "https://cdn.discordapp.com/embed/avatars/1.png",
                   "https://cdn.discordapp.com/embed/avatars/2.png",
                   "https://cdn.discordapp.com/embed/avatars/3.png",
                   "https://cdn.discordapp.com/embed/avatars/4.png"]

        embed = Embed(title="Modmail",
                      colour=Colour(0xFF69B4),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=random.choice(avatars))
        embed.set_footer(text=f"Requested by Anon Member")

        fields = [("Member", "Anon Member", False),
                  ("Message", msg.content, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed

    else:
        embed = Embed(title="Modmail",
                      colour=Colour(0xFF69B4),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"Requested by {author}")

        fields = [("Member", author, False),
                  ("Message", msg.content, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed


# Set up the Cog
class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction = None
        self.anon = None

    # Allows for the modmail system
    @commands.command(name="modmail", aliases=["mm"])
    async def mod_mail(self, ctx):
        self.anon = None
        # Get the mod-mail channel
        channel = self.bot.get_channel(728083016290926623)
        # Get the guild Enso
        guild = self.bot.get_guild(663651584399507476)
        # Get the member
        member = guild.get_member(ctx.author.id)

        # Making sure the user is in a DM channel with the bot
        if isinstance(ctx.message.channel, DMChannel):

            # Asking if the user wants to send staff mail
            modmail = await ctx.send(embed=startModMail(member))
            # Add reactions to the message
            await modmail.add_reaction('✅')
            await modmail.add_reaction('❌')

            # Surround with try/except to catch any exceptions that may occur
            try:
                # Checking if the user reacted with ✅ with response to sending staff a message
                def emoji_check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

                # Surround with try/except to catch any exceptions that may occur
                try:
                    # Wait for the user to add a reaction
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=emoji_check)
                except Exception as ex:
                    print(ex)
                    return
                else:
                    if str(reaction.emoji) == "✅":

                        # Delete the old embed
                        await modmail.delete()

                        # Ask the user if they want the mail to be anonymized
                        anonornot = await ctx.send(embed=AnonOrNot(member))
                        # Add reactions to the message
                        await anonornot.add_reaction('✅')
                        await anonornot.add_reaction('❌')

                        # Checking if the user reacted with ✅ with response to sending staff a message
                        def anon_check(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

                        # Surround with try/except to catch any exceptions that may occur
                        try:
                            # Wait for the user to add a reaction
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=anon_check)
                        except Exception as ex:
                            print(ex)
                            return
                        else:
                            if str(reaction.emoji) == "✅":
                                self.anon = True

                                # Delete the old embed
                                await anonornot.delete()

                                # Tell the user to type their mail into the chat
                                instructions = await ctx.send(embed=SendInstructions(member))

                                # Making sure that the reply is from the author
                                def check(m):
                                    return m.author == ctx.author

                                # Wait for the message from the author
                                msg = await self.bot.wait_for('message', check=check, timeout=300)

                                while len(msg.content) < 50:
                                    await ctx.send("**Make sure your mail is above 50 characters!!**"
                                                   "\n**This helps us reduce spam and allows you to include more detail in your mail**")

                                    # Wait for the message from the author
                                    msg = await self.bot.wait_for('message', check=check, timeout=300)

                                await channel.send(embed=SendMsgToModMail(self, msg, member))
                                await ctx.send("**Message relayed to Staff!"
                                               "\nThank you for your input!**")
                                await instructions.delete()

                            if str(reaction.emoji) == "❌":
                                self.anon = False

                                # Delete the old embed
                                await anonornot.delete()

                                # Tell the user to type their mail into the chat
                                instructions = await ctx.send(embed=SendInstructions(member))

                                # Making sure that the reply is from the author
                                def check(m):
                                    return m.author == ctx.author

                                # Wait for the message from the author
                                msg = await self.bot.wait_for('message', check=check, timeout=300)

                                while len(msg.content) < 50:
                                    await ctx.send("**Make sure your mail is above 50 characters!!**"
                                                   "\n**This helps us reduce spam and allows you to include more detail in your mail**")

                                    # Wait for the message from the author
                                    msg = await self.bot.wait_for('message', check=check, timeout=300)

                                await channel.send(embed=SendMsgToModMail(self, msg, member))
                                await ctx.send("**Message relayed to Staff!"
                                               "\nThank you for your input!**")
                                await instructions.delete()

                    if self.anon is None:
                        if str(reaction.emoji) == "❌":
                            # Delete the old embed
                            await modmail.delete()

                            # Send the Abort embed to the user
                            await ctx.send(embed=Abort(member))
                            return

            except Exception as ex:
                print(ex)

                # Send out an error message if the user waited too long
                await ctx.send("ModMail Timed Out! Do `~mm` or `~modmail` if you want to use the ModMail system!")

        else:
            ensoID = '<@716701699145728094>'

            message = await ctx.send(
                f"{ctx.author.mention} **ModMail can only be sent through DM's!** "
                f"\nSuggestions and Opinions on the server are always appreciated!\n"
                f"Make sure you DM {ensoID} and then use `~modmail` or `~mm`")

            # Let the User read the message for 10 seconds
            await asyncio.sleep(10.0)
            # Delete the message
            await message.delete()


def setup(bot):
    bot.add_cog(Modmail(bot))
