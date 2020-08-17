# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

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
import random
import string
from typing import Optional

import discord
from discord import Embed, Colour
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, command, is_owner, bot_has_permissions, Cog

"""events = {
    "🎤": 722483603409469470,  # Karaoke Night
    "🎧": 696753950879383605,  # Enso Bros Podcast
    "🎥": 722482922518609990,  # Movie Night
    "🎮": 722493033882452078,  # Game Night
    "<:xoxo:743564377864536204>": 744356592186687521,
    ":GameNight:": 722493033882452078,
    ":EnsoBros:": 696753950879383605,
    ":MovieNight:": 722482922518609990,
    ":Karaoke:": 722483603409469470
}
"""


# Error handling function to make sure that the commands only work in "enso-chan-commands"
def error_function(self):
    """Make sure that commands only work in "enso-chan-commands" in the server"""

    return f"**Sorry! I only work in {self.bot.enso_ensochancommands_Mention}**"


def helpDm(self):
    """Returning message that Enso~Chan has dm'ed them"""

    return f"I've just pinged your dms UwU! <a:huh:676195228872474643> <a:huh:676195228872474643>" \
           f"\nPlease ping my owner {self.bot.hammy_role_ID} for any issues/questions you have!"


# Method to retrieve information about the user and the guild
def get_user_info(ctx):
    # Allowing the bot to dm the user
    author = ctx.author

    # Define guild icon, enso bot icon and enso bot name
    guild_icon = ctx.guild.icon_url
    enso_icon = ctx.bot.user.avatar_url
    enso_name = ctx.bot.user.display_name

    return author, guild_icon, enso_icon, enso_name


# Gets the member and user avatar
def getMember(ctx):
    # Set member as the author
    member = ctx.message.author
    # Get the member avatar
    userAvatar = member.avatar_url

    return member, userAvatar


# Function to display all the images requested of the people
def displayServerImage(array, ctx, name):
    # Get the member and the userAvatar
    member, userAvatar = getMember(ctx)

    # Set embed up for the person requested by the user
    embed = Embed(
        title=f"**Look At What A Cutie {name.capitalize()} is! <a:huh:676195228872474643> <a:huh:676195228872474643> **",
        colour=ctx.bot.rnd_colour,
        timestamp=datetime.datetime.utcnow())
    embed.set_image(url=random.choice(array))
    embed.set_footer(text=f"Requested by {member}", icon_url=userAvatar)

    return embed


def enso_people():
    """Return all the people in the txt files"""

    return ['hammy', 'hussein', 'inna', 'kate', 'calvin',
            'lukas', 'stitch', 'corona', 'ging', 'ash',
            'gria', 'lilu', 'ifrah', 'skye', 'chloe',
            'connor', 'taz', 'ryder', 'rin', 'izzy',
            'david', 'clarity', 'angel', "studentjon", "anton"]


class Enso(Cog):
    """Commands for Ensō server"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """Printing out that Cog is ready on startup"""
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    @bot_has_permissions(embed_links=True)
    async def enso(self, ctx, name: Optional[str] = None):
        """Shows Random Person from Ensō"""

        # Making sure this command only works in Enso
        if not ctx.guild.id == self.bot.enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # If the channel that the command has been sent is in the list of accepted channels
        if str(ctx.channel) in "enso-chan-commands":
            if name:
                # Get the lowercase
                lcase_name = name.lower()
                try:
                    # Retrieve image of the member specified
                    with open(f'images/ServerMembers/{lcase_name}.txt') as file:
                        images_array = file.readlines()

                    # Embed the image into a message and send it to the channel
                    embed = displayServerImage(images_array, ctx, lcase_name)
                    await ctx.send(embed=embed)

                except Exception as e:
                    print(e)

                    # Send the list of available members to the channel
                    nice = string.capwords(', '.join(map(str, enso_people())))
                    # Send error message saying that the person isn't recognised
                    await ctx.send(f"Sorry! That person doesn't exist! Try the names listed below!"
                                   f"\n{nice}")

            else:

                # Retrieve a random image of a member in the bot
                with open(f'images/ServerMembers/{random.choice(enso_people())}.txt') as file:
                    array = file.readlines()

                # Get the member and the userAvatar
                member, userAvatar = getMember(ctx)

                # Embed the image in a message and send it to the channel
                embed = Embed(
                    title=f"Oh Look! A Cute Person <a:huh:676195228872474643> <a:huh:676195228872474643> ",
                    colour=self.bot.random_colour(),
                    timestamp=datetime.datetime.utcnow())
                embed.set_image(url=random.choice(array))
                embed.set_footer(text=f"Requested by {member}", icon_url=userAvatar)

                await ctx.send(embed=embed)
        else:

            message = await ctx.send(error_function(self))

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

    @enso.command()
    async def list(self, ctx):
        """Shows the List of People in the Bot"""

        # Send the list of available members to the channel
        nice = string.capwords(', '.join(map(str, enso_people())))
        # Send error message saying that the person isn't recognised
        await ctx.send(f"Try the names listed below!"
                       f"\n{nice}")

    @command(name="rules")
    @cooldown(1, 5, BucketType.user)
    async def rules(self, ctx):
        """Ruleset for Ensō"""

        # Making sure this command only works in Enso
        if not ctx.guild.id == self.bot.enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # Define Izzy's roles ID
        izzyID = '<@397944038440828928>'

        # Get information about the user and the guild
        author, guild_icon, enso_icon, enso_name = get_user_info(ctx)

        # Set up embed to list all the rules within the server
        embed = Embed(title="(っ◔◡◔)っ Ensō Rules",
                      colour=self.bot.admin_colour,
                      description="ヽ(͡◕ ͜ʖ ͡◕)ﾉ Please respect the following rules that are going to be listed below ヽ(͡◕ ͜ʖ ͡◕)ﾉ",
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=guild_icon)
        embed.set_author(name=enso_name,
                         icon_url=enso_icon)

        fields = [
            (self.bot.blank_space,
             "**➳ Don't be overly toxic/purposely problematic** \n This one is pretty self explanatory, just treat others the way you want to be treated and you'll get along with everyone :)",
             False),
            (self.bot.blank_space,
             "**➳ Respect all admins and staff** \n They are enforcing these rules to help make and keep this server a fantastic place to hang out.",
             False),
            (self.bot.blank_space,
             "**➳ Keep content organized into their respective channels** \n For example. When connected to a voice channel, all messages relating to the discussion in voice-chat should be sent in #vc-chat",
             False),
            (self.bot.blank_space,
             "**➳ No advertising other servers** \nIt's disrespectful to do that and won't be tolerated in this server",
             False),
            (self.bot.blank_space,
             "**➳ No pornographic/adult/other NSFW material** \n This is a community server and not meant to share this kind of material. Try to stay around PG 13 as most of our users are between 13 - 16",
             False),
            (self.bot.blank_space,
             "**➳ Don't take insults too far** \n Poking fun at others is okay, just don't take it too far. Any disputes can be brought up to a staff member and they will handle it." +
             "\nIf you end up causing a problem or taking things into your in hands, you will be punished",
             False),
            (self.bot.blank_space,
             "**➳ Explicit Language** \n Swearing is perfectly fine as long as it's not in excess, with some exceptions of course." +
             "These exceptions being racial, sexual, and ethnic slurs",
             False),
            (self.bot.blank_space,
             "**➳ Discord ToS** \n As well as following the rules we have set forth, please make sure to follow [Discord's ToS](https://discordapp.com/terms)",
             False),
            (self.bot.blank_space,
             "```( ͡°ω ͡°) Disciplinary Actions ( ͡°ω ͡°)```", False),
            (self.bot.blank_space,
             "**➳ First Offense** \n Warning",
             True),
            (self.bot.blank_space,
             "**➳ Second Offense** \n1 hour mute",
             True),
            (self.bot.blank_space,
             "**➳ Third Offense** \n12 hour mute",
             True),
            (self.bot.blank_space,
             "**➳ Fourth Offense** \n24 hour mute",
             True),
            (self.bot.blank_space,
             "**➳Fifth Offense** \n Kicked from the server",
             True),
            (self.bot.blank_space,
             "**➳ Sixth Offense** \n Banned from the server",
             True),
            (self.bot.blank_space,
             "**➳ There are, of course, exceptions to these rules based on the severity of the offense Minor offenses will play out as described but major offenses will be dealt with at the discretion of the staff member involved.**",
             False),
            (self.bot.blank_space,
             f"**➳ Any disputes about a staff members choices or actions can be brought to myself, {ctx.message.author.mention} or my co-owner, {izzyID}**",
             False)]

        # Add fields to the embed
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        # Dm the user the embedded message
        await author.send(embed=embed)

        # Send the helpDm() message to the channel that the user is in
        message = await ctx.send(helpDm(self))

        # Let the user read the message for 10 seconds
        await asyncio.sleep(10)
        # Delete the message
        await message.delete()

    @command(name="roles")
    @cooldown(1, 5, BucketType.user)
    async def roles(self, ctx):
        """Leveled role/xp system for Ensō"""

        if not ctx.guild.id == self.bot.enso_guild_ID:
            await ctx.send("**Sorry! That command is only for a certain guild!**")
            return

        # Get the url of the leveled roles image
        roles_image = "https://media.discordapp.net/attachments/669812887564320769/717149671771996180/unknown.png"

        # Setting up embedded message about the leveled roles system within the server
        embed = Embed(title="```So you wanna know how the leveled roles system works huh?```",
                      colour=self.bot.admin_colour,
                      description="------------------------------------------------",
                      timestamp=datetime.datetime.utcnow())

        # Get information about the user and the guild
        author, guild_icon, enso_icon, enso_name = get_user_info(ctx)

        embed.set_image(url=roles_image)
        embed.set_thumbnail(url=guild_icon)
        embed.set_author(name=enso_name,
                         icon_url=enso_icon)

        embed.add_field(name="Cooldown", value="**•XP is gained every time you talk with a 2 minute cooldown.**",
                        inline=False),
        embed.add_field(name="Message Length",
                        value="**•XP is not determined by the size of the message. You will not get more XP just because "
                              "the message is bigger.**",
                        inline=False),
        embed.add_field(name="Roles",
                        value="**•As seen below, those are the colours and roles that will be achieved upon gaining that "
                              "amount of experience**",
                        inline=False)

        # Dm the user the embedded message
        await author.send(embed=embed)

        # Send the helpDm() message to the channel that the user is in
        message = await ctx.send(helpDm(self))

        # Let the user read the message for 10 seconds
        await asyncio.sleep(10)
        # Delete the message
        await message.delete()

    # Allowing people to get ping-able self roles
    @command(name="verification", hidden=True)
    @is_owner()
    async def verification(self, ctx):
        # Set up embed to let the user know that they have to react with ✅
        embed = Embed(title="**Verification**",
                      colour=self.bot.admin_colour,
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Remember to read the rules!",
            value="React with ✅ to gain access to the rest of the server!",
            inline=False)

        # Send embed to the channel it was called in and automatically add the reaction ✅
        # verif = await ctx.send(embed=embed)
        # await verif.add_reaction('✅')

        # Edit the Embed And Update it
        verif = await ctx.fetch_message(728424149692842115)
        await verif.edit(embed=embed)

    # Cog listener for enabling roles to be added to users when they react to the embedded message
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Get the guild
        guild = self.bot.get_guild(self.bot.enso_guild_ID)
        # Get the member
        member = guild.get_member(payload.user_id)
        # Getting the channel verification by setting it to #verification
        channel = guild.get_channel(self.bot.enso_verification_ID)

        # If the channel is #verification and If the member is not a user, do nothing
        if not payload.member.bot and payload.channel_id == channel.id:

            # Get the 'Lucid' role and then give it to the user
            lucid = discord.utils.get(guild.roles, name='Lucid')
            not_verified = discord.utils.get(guild.roles, name='Not Verified')

            # if the emoji that was reacted is the tick mark.
            if payload.emoji.name == "✅":
                await member.remove_roles(not_verified)
                await member.add_roles(lucid)

                # Set hamothyID equal to my id in discord
                hamothyID = '<@&715412394968350756>'

                # Set the channel id to "general"
                general = guild.get_channel(663651584399507481)

                # String for welcoming people in the #general channel
                general_welcome = f"Welcome to the server! {member.mention} I hope you enjoy your stay here <a:huh:676195228872474643> <a:huh:676195228872474643> " \
                                  f"\nPlease go into <#722347423913213992> to choose some ping-able roles for events! " \
                                  f"\nPlease ping {hamothyID} for any questions about the server and of course, the other staff members!"

                # Send welcome message to #general
                await general.send(general_welcome)

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:

            # Print out the emoji name
            print(payload.emoji.name)

            # Find a role corresponding to the Emoji name.
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been reacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Print to me that the role was found and display the id of the role
                print(role.name + " was found!")
                print(role.id)

                # Find the member who had reacted to the emoji
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                # Add the role to the member
                await member.add_roles(role)

                # Print to me that the role has been added
                print("done")

                """# Make sure the reaction event doesn't count other channels
                if payload.channel_id == 722347423913213992:
                    role = payload.member.guild.get_role(events.get(payload.emoji.name))
                    await payload.member.add_roles(role)
                    print(f"{payload.member.name} Was Given Role {role}")"""

    # Cog listener for enabling roles to be removed from users when they unreact to the embedded messaged
    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        # If the message id equals the self roles message
        if payload.message_id == 722514840559812649:

            # Print out the emoji name
            print(payload.emoji.name)

            # Get the server id
            guild_id = payload.guild_id

            # Find the guild Enso and find the role of the emoji that has been unreacted to
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            role = discord.utils.find(lambda r: r.name == payload.emoji.name, guild.roles)

            # if the role does exist
            if role is not None:
                # Find the member that has the role which the emoji is connected to
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

                # Remove the role from the member
                await member.remove_roles(role)

                """# Make sure the reaction event doesn't count other channels
                if payload.channel_id == 722347423913213992:
                    guild = self.bot.get_guild(payload.guild_id)
    
                    member = guild.get_member(payload.user_id)
                    role = guild.get_role(events.get(payload.emoji.name))
                    await member.remove_roles(role)
                    print(f"{member.name} Was Removed from Role {role}")"""

    # Allowing people to get ping-able self roles
    @command(name="rolemenu", hidden=True)
    @is_owner()
    async def role_menu(self, ctx):
        # Setting the channel to "
        channel = ctx.guild.get_channel(722347423913213992)

        # Set up embed to let people know what ping-able roles can be chosen
        embed = Embed(title="**Role Menu: Ping-Able Roles**",
                      colour=Colour.orange(),
                      timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.message.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="\u200b",
            value="React to give yourself roles to be pinged for these events!",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="🎥 : **Movie Nights**",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="🎤 : **Karaoke Nights**",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="🎧 : **Enso Bros Podcasts**",
            inline=False)
        embed.add_field(
            name="\u200b",
            value="🎮 : **Game Nights**",
            inline=False)

        # Edit the Embed And Update it
        message = await ctx.fetch_message(722514840559812649)
        await message.edit(embed=embed)

        # Send the embed to the channel "newpeople"
        # await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Enso(bot))
