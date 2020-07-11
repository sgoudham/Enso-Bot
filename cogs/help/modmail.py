import asyncio
import random

import mariadb
from discord import DMChannel, Embed
from discord.ext import commands

import db
from settings import blank_space, enso_embedmod_colours, time, enso_guild_ID, enso_modmail_ID, hammyMention, \
    ensoMention, hammyID


# Method to send the prompt/embed to start sending modmail to the user
def startModMail(author):
    # Set up embed to let the user how to start sending modmail
    startModMailEmbed = Embed(title="**Welcome to Modmail!**",
                              colour=enso_embedmod_colours,
                              timestamp=time)

    startModMailEmbed.set_thumbnail(url=author.avatar_url)
    startModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [
        (blank_space, "**React to this message if you want to send a message to the Staff Team!**", False),
        (blank_space, "**Use :white_check_mark: for** `Yes`", True),
        (blank_space, "**Use :x: for** `No`", True),
        (blank_space, blank_space, True),
        (blank_space,
         "We encourage all suggestions/thoughts and opinions on the server! As long as it is **valid** criticism. "
         "Purely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        startModMailEmbed.add_field(name=name, value=value, inline=inline)

    return startModMailEmbed


# Method to ask the user if they want to be anonymous or not
def AnonOrNot(author):
    # Set up embed to let the user how to start sending modmail
    AnonModMailEmbed = Embed(title="**Want to send it Anonymously?**",
                             colour=enso_embedmod_colours,
                             timestamp=time)

    AnonModMailEmbed.set_thumbnail(url=author.avatar_url)
    AnonModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [(blank_space, "**We understand that for some things, you may want to remain Anonymous."
                            "\nFeel free to use the reactions below to choose!**", False),
              (blank_space, "**Use :white_check_mark: for** `Yes`", True),
              (blank_space, "**Use :x: for** `No`", True),
              (blank_space, blank_space, True),
              (blank_space,
               "This will make sure that Staff do not know who is sending the mail."
               "\nAgain, purely negative feedback will not be considered.", True)]

    for name, value, inline in fields:
        AnonModMailEmbed.add_field(name=name, value=value, inline=inline)

    return AnonModMailEmbed


# Method to send an embed to to let the user know to type into chat
def SendInstructions(author):
    # Set up embed to let the user know that they have aborted the modmail
    SendModMailEmbed = Embed(title="**Please enter a message for it to be sent to the staff!**",
                             colour=enso_embedmod_colours,
                             timestamp=time)

    SendModMailEmbed.set_thumbnail(url=author.avatar_url)
    SendModMailEmbed.set_footer(text=f"Sent by {author}")

    fields = [("**Make sure that the message is above 50 characters!**",
               "**Include as much detail as possible :P**",
               False)]

    for name, value, inline in fields:
        SendModMailEmbed.add_field(name=name, value=value, inline=inline)

    return SendModMailEmbed


# Method to let the user know that the message must be above 50 characters
def ErrorHandling(author):
    # Set up embed to let the user know that the message must be above 50 characters
    ErrorHandlingEmbed = Embed(title="**Uh Oh! Please make sure the message is above 50 characters!**",
                               colour=enso_embedmod_colours,
                               timestamp=time)

    ErrorHandlingEmbed.set_thumbnail(url=author.avatar_url)
    ErrorHandlingEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Please enter in a message which is above 50 characters!",
               "**This helps us reduce spam and allows you to include more detail in your mail!**",
               False)]

    for name, value, inline in fields:
        ErrorHandlingEmbed.add_field(name=name, value=value, inline=inline)

    return ErrorHandlingEmbed


# Method to send an embed into chat to let the user know that their mail has been sent successfully
def MessageSentConfirmation(author):
    # Set up embed to let the user know that they have sent the mail
    ConfirmationEmbed = Embed(title="**Message relayed to Staff!!**",
                              colour=enso_embedmod_colours,
                              timestamp=time)

    ConfirmationEmbed.set_thumbnail(url=author.avatar_url)
    ConfirmationEmbed.set_footer(text=f"Sent by {author}")

    fields = [("Thank you for your input! The staff team appreciate it very much!",
               f"\n As mentioned previously, please don't be hesistant to DM {hammyMention} for anything! :P",
               False)]

    for name, value, inline in fields:
        ConfirmationEmbed.add_field(name=name, value=value, inline=inline)

    return ConfirmationEmbed


# Method to actually allow the message to be sent to #mod-mail
def SendMsgToModMail(self, msg, author):
    if self.anon:

        avatars = ["https://cdn.discordapp.com/embed/avatars/0.png",
                   "https://cdn.discordapp.com/embed/avatars/1.png",
                   "https://cdn.discordapp.com/embed/avatars/2.png",
                   "https://cdn.discordapp.com/embed/avatars/3.png",
                   "https://cdn.discordapp.com/embed/avatars/4.png"]

        embed = Embed(title="Modmail",
                      colour=enso_embedmod_colours,
                      timestamp=time)

        embed.set_thumbnail(url=random.choice(avatars))
        embed.set_footer(text=f"Sent By Anon Member")

        fields = [("Member", "Anon Member", False),
                  ("Message", msg.content, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed

    else:
        embed = Embed(title="Modmail",
                      colour=enso_embedmod_colours,
                      timestamp=time)

        embed.set_thumbnail(url=author.avatar_url)
        embed.set_footer(text=f"Sent By {author}")

        fields = [("Member", author, False),
                  ("Message", msg.content, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed


# Method to allow modmail to be logged into the database
def logModMail(ctx, anon, msg):
    # With the database connection
    with db.connection() as conn:
        # Make sure that mariaDB errors are handled properly
        try:
            if anon:
                Anon = "True"
            else:
                Anon = "False"

            msg_name = ctx.message.author.name
            msg_discrim = ctx.message.author.discriminator
            time = ctx.message.created_at

            # Get:
            msg_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Time of the Message
            msg_author = f"{msg_name}#{msg_discrim}"  # DiscordID
            msg_content = msg.content  # Content of the message

            # Store the variables
            val = Anon, msg_time, msg_author, msg_content

            # Define the Insert Into Statement inserting into the database
            insert_query = """INSERT INTO modmail (Anon, messageTime, discordID, messageContent) VALUES (?, ?, ?, ?)"""
            cursor = conn.cursor()
            # Execute the SQL Query
            cursor.execute(insert_query, val)
            conn.commit()
            print(cursor.rowcount, "Record inserted successfully into Modmail")

        except mariadb.Error as ex:
            print("Parameterized Query Failed: {}".format(ex))


# Method to send an embed to let the user know that they have aborted the modmail process
def Abort(author):
    # Set up embed to let the user know that they have aborted the modmail
    AbortEmbed = Embed(title="**Aborting ModMail!**",
                       colour=enso_embedmod_colours,
                       timestamp=time)

    AbortEmbed.set_thumbnail(url=author.avatar_url)
    AbortEmbed.set_footer(text=f"Sent by {author}")

    fields = [
        ("**If you change your mind, you can do `~mm` or `~modmail` at anytime!**",
         f"If you want to speak to me personally, you can DM {hammyMention} anytime!", False)]

    for name, value, inline in fields:
        AbortEmbed.add_field(name=name, value=value, inline=inline)

    return AbortEmbed


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
        channel = self.bot.get_channel(enso_modmail_ID)
        # Get the guild Enso
        guild = self.bot.get_guild(enso_guild_ID)
        # Get Hamothy
        member = guild.get_member(hammyID)

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
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=emoji_check)
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

                        # Surround with try/except to catch any exceptions that may occur
                        try:

                            # Wait for the user to add a reaction
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=emoji_check)
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

                                # Making sure that the message is below 50 characters and the message was sent in the channel
                                while len(msg.content) < 50 and isinstance(msg.channel, DMChannel):
                                    await ctx.send(embed=ErrorHandling(member))

                                    # Wait for the message from the author
                                    msg = await self.bot.wait_for('message', check=check, timeout=300)

                                # Delete the previous embed
                                await instructions.delete()
                                # Send the message to the modmail channel
                                await channel.send(embed=SendMsgToModMail(self, msg, ctx.author.id))

                                # Make sure the user knows that their message has been sent
                                await ctx.send(embed=MessageSentConfirmation(member))

                                # Log the message within the database
                                logModMail(ctx, self.anon, msg)

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

                                # Making sure that the message is below 50 characters and the message was sent in the channel
                                while len(msg.content) < 50 and isinstance(msg.channel, DMChannel):
                                    await ctx.send(embed=ErrorHandling(member))

                                    # Wait for the message from the author again
                                    msg = await self.bot.wait_for('message', check=check, timeout=300)

                                # Delete the previous embed
                                await instructions.delete()
                                # Send the message to the modmail channel
                                await channel.send(embed=SendMsgToModMail(self, msg, ctx.author.id))

                                # Make sure the user knows that their message has been sent
                                await ctx.send(embed=MessageSentConfirmation(member))

                                # Log the message within the database
                                logModMail(ctx, self.anon, msg)

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
            message = await ctx.send(
                f"{ctx.author.mention} **ModMail can only be sent through DM's!** "
                f"\nSuggestions and Opinions on the server are always appreciated!\n"
                f"Make sure you DM {ensoMention} and then use `~modmail` or `~mm`")

            # Let the User read the message for 10 seconds
            await asyncio.sleep(10.0)
            # Delete the message
            await message.delete()


def setup(bot):
    bot.add_cog(Modmail(bot))
