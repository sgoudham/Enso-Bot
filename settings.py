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

import random

from discord import Colour, Embed

# Defining a list of colours
colors = {
    'DEFAULT': 0x000000,
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'GREY': 0x95A5A6,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_GREY': 0x979C9F,
    'DARKER_GREY': 0x7F8C8D,
    'LIGHT_GREY': 0xBCC0C0,
    'DARK_NAVY': 0x2C3E50,
    'BLURPLE': 0x7289DA,
    'GREYPLE': 0x99AAB5,
    'DARK_BUT_NOT_BLACK': 0x2C2F33,
    'NOT_QUITE_BLACK': 0x23272A,
    'CRIMSON': 0xDC143C,
    'HOT_PINK': 0xFF69B4,
    'DEEP_PINK': 0xFF69B4,
    'MAGENTA': 0xFF00FF,
    'VIOLET': 0xEE82EE,
    'TEAL': 0x008080,
    'MIDNIGHT_BLUE': 0x191970,
    'MISTY_ROSE': 0xFFE4E1,
    'SEA_GREEN': 0x2E8B57,
    'MEDIUM_VIOLET_RED': 0xC71585,
}

# Grabbing the list of colours
colour_list = [c for c in colors.values()]


def rndColour():
    """Generate a random hex colour"""

    return Colour(random.randint(0, 0xFFFFFF))


# --------------------------------------------!Cache Section!-----------------------------------------------------------

# Setup Dict To Store Values
enso_cache = {}


def cache(guildid, prefix, channel, rolespersist):
    """Storing GuildID, Modlogs Channel and Prefix in Cache"""

    enso_cache[guildid] = {"Modlogs": channel, "Prefix": prefix, "RolesPersist": rolespersist}


def get_cache(guildid):
    """Returning the cache"""

    return enso_cache[guildid]


def del_cache(guildid):
    """Deleting the entry of the guild within the cache"""

    del enso_cache[guildid]


# --------------------------------------------!End Cache Section!-------------------------------------------------------

# --------------------------------------------!RolePersist Section!-----------------------------------------------------


def get_roles_persist(guildid):
    """Returning rolespersist value of the guild"""

    return enso_cache[guildid]["RolesPersist"]


async def update_role_persist(guildid, value, pool):
    """Update the rolepersist value of the guild (Enabled or Disabled)"""

    enso_cache[guildid]["RolesPersist"] = value

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Update the existing prefix within the database
            update_query = """UPDATE guilds SET rolespersist = (%s) WHERE guildID = (%s)"""
            update_vals = value, guildid,

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()


# --------------------------------------------!End RolePersist Section!-------------------------------------------------

# --------------------------------------------!ModLogs Section!---------------------------------------------------------

async def storage_modlog_for_guild(pool, ctx, channelID, setup):
    """Updating the modlog within the dict and database"""

    enso_cache[str(ctx.guild.id)]["Modlogs"] = channelID

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Update the existing modlogs channel within the database
            update_query = """UPDATE guilds SET modlogs = (%s) WHERE guildID = (%s)"""
            update_vals = channelID, ctx.guild.id,

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()

    # Send custom confirmation messages to log based on the command update or setup
    if setup:
        print(cur.rowcount, f"Modlog channel for guild {ctx.guild.name} has been Setup")
    else:
        print(cur.rowcount, f"Modlog channel for guild {ctx.guild.name} has been Updated")

    if setup:
        # Send confirmation that modmail channel has been setup
        await ctx.send("Your **Modlogs Channel** is now successfully set up!" +
                       f"\nPlease refer to **{ctx.prefix}help** for any information")
    else:
        # Let the user know that the guild modlogs channel has been updated
        channel = ctx.guild.get_channel(channelID)
        await ctx.send(f"Modlog Channel for **{ctx.guild.name}** has been updated to {channel.mention}")


def cache_modlogs(guildid, channel):
    """Store the cached modlog channels"""

    enso_cache[guildid]["Modlogs"] = channel


def del_modlog_channel(guildid):
    """Deleting the key - value pair for guild/modlogs"""

    if enso_cache[guildid]["Modlogs"] is not None:
        del enso_cache[guildid]["Modlogs"]


def remove_modlog_channel(guildid):
    """Remove the value of modlog for the guild specified"""

    enso_cache[guildid]["Modlogs"] = None


def get_modlog_for_guild(guildid):
    """Get the modlog channel of the guild that the user is in"""

    channel = enso_cache[guildid]["Modlogs"]
    return channel


# --------------------------------------------!End ModLogs Section!-----------------------------------------------------

# --------------------------------------------!Prefixes Section!--------------------------------------------------------

async def storage_prefix_for_guild(pool, ctx, prefix):
    """Updating the prefix within the dict and database when the method is called"""

    enso_cache[str(ctx.guild.id)]["Prefix"] = prefix

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Update the existing prefix within the database
            update_query = """UPDATE guilds SET prefix = (%s) WHERE guildID = (%s)"""
            update_vals = prefix, ctx.guild.id,

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()
            print(cur.rowcount, f"Guild prefix has been updated for guild {ctx.guild.name}")

            # Let the user know that the guild prefix has been updated
            await ctx.send(f"**Guild prefix has been updated to `{prefix}`**")


def cache_prefix(guildid, prefix):
    """Storing prefixes for the guild"""

    enso_cache[guildid]["Prefix"] = prefix


def del_cache_prefix(guildid):
    """Deleting the key - value pair for guild"""

    del enso_cache[guildid]["Prefix"]


def get_prefix_for_guild(guildid):
    """Get the prefix of the guild that the user is in"""

    prefix = enso_cache[guildid]["Prefix"]
    if prefix is not None:
        return prefix
    return "~"


# --------------------------------------------!End Prefixes Section!----------------------------------------------------

# --------------------------------------------!Cogs/Set Values Section!-------------------------------------------------

# Define repeated variables
hammyMention = '<@154840866496839680>'
hammyID = 154840866496839680
ensoMention = '<@716701699145728094>'

blank_space = "\u200b"
enso_embedmod_colours = Colour(0x62167a)

enso_ensochancommands_Mention = "<#721449922838134876>"

enso_ensochancommands_ID = 721449922838134876
enso_verification_ID = 728034083678060594
enso_selfroles_ID = 722347423913213992
enso_guild_ID = 663651584399507476
enso_newpeople_ID = 669771571337887765
enso_modmail_ID = 728083016290926623
enso_feedback_ID = 739807803438268427


def extensions():
    """Returns a list of all the cogs"""

    ext = ['cogs.interactive', 'cogs.anime', 'cogs.relationship',
           'cogs.info', 'cogs.fun', 'cogs.enso',
           'cogs.guild', 'cogs.moderation', "cogs.help"]

    return ext


async def generate_embed(ctx, desc):
    """Generate Embed"""

    embed = Embed(description=desc,
                  colour=enso_embedmod_colours)

    await ctx.send(embed=embed)


async def storeRoles(pool, target, ctx, member):
    """Storing User Roles within Database"""

    role_ids = ", ".join([str(r.id) for r in target.roles])

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Store the existing roles of the user within the database
            update_query = """UPDATE members SET mutedroles = (%s) WHERE guildID = (%s) AND discordID = (%s)"""
            update_vals = role_ids, ctx.guild.id, member.id

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()
            print(cur.rowcount, f"Roles Added For User {member} in {ctx.guild.name}")


async def clearRoles(member, pool):
    """Clear the roles when the user has been unmuted"""

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Clear the existing roles of the user from the database
            update_query = """UPDATE members SET mutedroles = NULL WHERE guildID = (%s) AND discordID = (%s)"""
            update_vals = member.guild.id, member.id

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()
            print(cur.rowcount, f"Roles Cleared For User {member} in {member.guild.name}")

# --------------------------------------------!End Cogs/Set Values Section!---------------------------------------------
