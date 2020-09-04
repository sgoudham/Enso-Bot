# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Hamothy

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import asyncio
import datetime
import io
import random

import discord
from discord import Embed, File


class Modmail:
    """Methods for sending modmail!"""

    def __init__(self, bot):
        self.bot = bot
        self.anon = None
        self.avatars = ["https://cdn.discordapp.com/embed/avatars/0.png",
                        "https://cdn.discordapp.com/embed/avatars/1.png",
                        "https://cdn.discordapp.com/embed/avatars/2.png",
                        "https://cdn.discordapp.com/embed/avatars/3.png",
                        "https://cdn.discordapp.com/embed/avatars/4.png"]

    def anon_or_not(self, author):
        """Method to ask the user if they want to be anonymous or not"""

        # Set up embed to let the user how to start sending modmail
        AnonModMailEmbed = Embed(title="**Want to send it Anonymously?**",
                                 colour=self.bot.admin_colour,
                                 timestamp=datetime.datetime.utcnow())

        AnonModMailEmbed.set_thumbnail(url=author.avatar_url)
        AnonModMailEmbed.set_footer(text=f"Sent by {author}")

        fields = [(self.bot.blank_space, "**We understand that for some things,"
                                         "you may want to remain Anonymous."
                                         "\nUse the reactions below to choose!**", False),
                  (self.bot.blank_space, "**Use :white_check_mark: for** `Yes`", True),
                  (self.bot.blank_space, "**Use :x: for** `No`", True),
                  (self.bot.blank_space, self.bot.blank_space, True),
                  (self.bot.blank_space,
                   "The Staff will not know who is sending this"
                   "\nPurely negative feedback will not be considered.", True)]

        for name, value, inline in fields:
            AnonModMailEmbed.add_field(name=name, value=value, inline=inline)

        return AnonModMailEmbed

    def send_instructions(self, author):
        """Method to send an embed to to let the user know to type into chat"""

        SendModMailEmbed = Embed(title="**Please enter a message for it to be sent to the staff!**",
                                 colour=self.bot.admin_colour,
                                 timestamp=datetime.datetime.utcnow())

        SendModMailEmbed.set_thumbnail(url=author.avatar_url)
        SendModMailEmbed.set_footer(text=f"Sent by {author}")

        fields = [("**Make sure that the message is above **50** and below **1024** characters!**",
                   "**Include as much detail as possible :P**",
                   False)]

        for name, value, inline in fields:
            SendModMailEmbed.add_field(name=name, value=value, inline=inline)

        return SendModMailEmbed

    def error_handling(self, author):
        """Method to let the user know that the message must be above 50 characters"""

        ErrorHandlingEmbed = Embed(
            title="Uh Oh! Please make sure the message is above **50** and below **1024** characters!",
            colour=self.bot.admin_colour,
            timestamp=datetime.datetime.utcnow())

        ErrorHandlingEmbed.set_thumbnail(url=author.avatar_url)
        ErrorHandlingEmbed.set_footer(text=f"Sent by {author}")

        fields = [("Please enter in a message which is above **50** and below **1024** characters!",
                   "**This helps us reduce spam and allows you to include more detail in your mail!**",
                   False)]

        for name, value, inline in fields:
            ErrorHandlingEmbed.add_field(name=name, value=value, inline=inline)

        return ErrorHandlingEmbed

    def message_sent_confirmation(self, author):
        """Method to send an embed into chat to let the user know that their mail has been sent successfully"""

        ConfirmationEmbed = Embed(title="**Message relayed to Staff!!**",
                                  colour=self.bot.admin_colour,
                                  timestamp=datetime.datetime.utcnow())

        ConfirmationEmbed.set_thumbnail(url=author.avatar_url)
        ConfirmationEmbed.set_footer(text=f"Sent by {author}")

        fields = [("Thank you for your input! The staff team appreciate it very much!",
                   f"\n As mentioned previously, please don't be hesitant to DM the Staff for anything! :P",
                   False)]

        for name, value, inline in fields:
            ConfirmationEmbed.add_field(name=name, value=value, inline=inline)

        return ConfirmationEmbed

    def send_modmail(self, msg, author):
        """Method to actually allow the message to be sent to modmail logging channel"""

        embed = Embed(title="Modmail",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())

        if self.anon:

            embed.set_thumbnail(url=random.choice(self.avatars))
            embed.set_footer(text=f"Sent By Anon Member")

            fields = [("Member", "Anon Member", False),
                      ("Message", msg.content, False)]
        else:

            embed.set_thumbnail(url=author.avatar_url)
            embed.set_footer(text=f"Sent By {author}")

            fields = [("Member", author, False),
                      ("Message", msg.content, False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        return embed

    async def wait_for_msg(self, check, user_channel):
        """
        Method to check if the user actually types in a message
        If not, delete the channel
        """

        try:
            # Wait for the message from the author
            mod_message = await self.bot.wait_for('message', check=check, timeout=300.0)

        # Delete channel if user does not send a message within 5 minutes
        except asyncio.TimeoutError:
            await user_channel.delete()
            return None
        else:
            return mod_message

    async def modmail(self, payload):
        """Listen for reactions for modmail channel/starboard"""

        # Don't count reactions that are made by the bot
        # Don't count other reactions other than ✅ and ❌
        if payload.member.bot or str(payload.emoji) not in ['✅', '❌']:
            return

        # Get the modmail information from cache
        modmail = self.bot.get_modmail(payload.guild_id)
        if modmail:
            channel_id = modmail["modmail_channel_id"]
            message_id = modmail["message_id"]
            modmail_channel_id = modmail["modmail_logging_channel_id"]
        else:
            return

        # Bunch of checks to make sure it has the right guild, channel, message and reaction
        if payload.channel_id == channel_id and payload.message_id == message_id and payload.emoji.name == "✅":

            # Get the guild
            guild = self.bot.get_guild(payload.guild_id)
            # Get the member
            member = guild.get_member(payload.user_id)
            # Get the setup modmail channel
            channel = guild.get_channel(payload.channel_id)
            # Get the modmail logging channel
            modmail_channel = guild.get_channel(modmail_channel_id)

            # Fetch the message and remove the reaction
            reaction = await channel.fetch_message(message_id)
            await reaction.remove_reaction('✅', member)

            # Setting up the channel permissions for the new channel that will be created
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, embed_links=True,
                                                      add_reactions=True, manage_messages=True),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Saving this for later within when discord.py 1.4 comes out
            # user_channel = await guild.create_category_channel("Member", overwrites=overwrites, position=7)

            # Create the text channel
            user_channel = await guild.create_text_channel("Member", overwrites=overwrites,
                                                           position=0)

            # Mention the user to make sure that they get pinged
            mention = await user_channel.send(member.mention)
            await mention.delete()

            try:

                # Send the embed if they want to remain anonymous or not
                Anon_or_Not = await user_channel.send(embed=self.anon_or_not(member))
                # Add reactions to the message
                await Anon_or_Not.add_reaction('✅')
                await Anon_or_Not.add_reaction('❌')

                # Checking if the user reacted with ✅ with response to sending staff a message
                def emoji_check(reaction, user):
                    return user == member and str(reaction.emoji) in ['✅', '❌']

                try:
                    # Wait for the user to add a reaction
                    reaction, user = await self.bot.wait_for('reaction_add', check=emoji_check, timeout=60.0)

                # Delete channel if user does not react within 60 seconds
                except asyncio.TimeoutError as ex:
                    print(ex)
                    await user_channel.delete()
                else:

                    # Making sure that the reply is from the author
                    def check(m):
                        return m.author == payload.member and user_channel.id == instructions.channel.id

                    # Checking if user wants to be Anonymous or not
                    if str(reaction.emoji) == "✅":
                        self.anon = True

                    if str(reaction.emoji) == "❌":
                        self.anon = False

                    # Delete the old embed
                    await Anon_or_Not.delete()

                    # Tell the user to type their mail into the chat
                    instructions = await user_channel.send(embed=self.send_instructions(member))

                    # Wait for the message from the author
                    msg = await self.wait_for_msg(check, user_channel)
                    if not msg: return

                    # Making sure that the message is below 50 characters and the message was sent in the channel
                    while len(msg.content) <= 50 and msg.channel == user_channel:
                        await user_channel.send(embed=self.error_handling(member))

                        # Wait for the message from the author
                        msg = await self.wait_for_msg(check, user_channel)
                        if not msg: return

                    # As long as the message is above 50 characters and in the correct channel
                    if len(msg.content) > 50 and msg.channel == user_channel:
                        # Delete the previous embed
                        await instructions.delete()

                        # Store all text in the channel in a bytesio object
                        text = ""
                        async for message in user_channel.history(limit=300):
                            text += "".join(f"{message.created_at} : {message.content}\n")
                        text_bytes = str.encode(text)

                        file = io.BytesIO(text_bytes)
                        file_name = "Anon.txt" if self.anon else f"{member.name}.txt"

                        # Send the message to the modmail channel
                        await modmail_channel.send(embed=self.send_modmail(msg, member),
                                                   file=File(file, file_name))

                        # Make sure the user knows that their message has been sent
                        await user_channel.send(embed=self.message_sent_confirmation(member))

                        # Let the user read the message for 5 seconds
                        await asyncio.sleep(5)

                        # Delete the channel and then stop the function
                        await user_channel.delete()

                    # If the user types anywhere else, delete the channel
                    else:
                        await user_channel.delete()

            except Exception as ex:
                print(ex)

                # Send out an error message if the user waited too long
                await user_channel.send(
                    "Sorry! Something seems to have gone wrong and the modmail will be aborting."
                    "\nRemember to make sure it's under **1024** characters!!")

                await asyncio.sleep(5)
                await user_channel.delete()
