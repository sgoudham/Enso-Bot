import asyncio
import random

from discord import Colour

import db
from db import connection

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


async def startup_cache_log():
    """Store the modlogs/prefixes in cache from the database on startup"""

    # Setup pool
    pool = await connection(db.loop)

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Grab the prefix of the server from the database
            select_query = """SELECT * FROM guilds"""

            # Execute the query
            await cur.execute(select_query)
            results = await cur.fetchall()

            # Store the guildID's, modlog channels and prefixes within cache
            for row in results:
                cache(guildid=row[0], channel=row[2], prefix=row[1])


# Method to store the guildID, channel
def cache(guildid, channel, prefix):
    """Storing GuildID, Modlogs Channel and Prefix in Cache"""
    enso_cache[guildid] = {"Modlogs": channel, "Prefix": prefix}


def get_cache(guildid):
    """Returning the cache"""
    return enso_cache[guildid]


def del_cache(guildid):
    """Deleting the entry of the guild within the cache"""
    del enso_cache[guildid]


# --------------------------------------------!End Cache Section!-------------------------------------------------------

# --------------------------------------------!ModLogs Section!---------------------------------------------------------

# Updating the modlog within the dict and database when the method is called
async def storage_modlog_for_guild(ctx, channelID, setup):
    enso_cache[str(ctx.guild.id)]["Modlogs"] = channelID

    # Setup pool
    pool = await connection(db.loop)

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Update the existing prefix within the database
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


# Method to store the cached modlog channels
def cache_modlogs(guildid, channel):
    enso_cache[guildid]["Modlogs"] = channel


# Deleting the key - value pair for guild/modlogs
def del_modlog_channel(guildid):
    if enso_cache[guildid]["Modlogs"] is not None:
        del enso_cache[guildid]["Modlogs"]
    else:
        pass


# Remove the value of modlog for the guild specified
def remove_modlog_channel(guildid):
    enso_cache[guildid]["Modlogs"] = None


# Get the modlog channel of the guild that the user is in
def get_modlog_for_guild(guildid):
    channel = enso_cache[guildid]["Modlogs"]
    return channel


# --------------------------------------------!End ModLogs Section!-----------------------------------------------------

# --------------------------------------------!Prefixes Section!--------------------------------------------------------

# Updating the prefix within the dict and database when the method is called
async def storage_prefix_for_guild(ctx, prefix):
    enso_cache[str(ctx.guild.id)]["Prefix"] = prefix

    # Setup pool
    pool = await connection(db.loop)

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


# Method to store the cached prefixes
def cache_prefix(guildid, prefix):
    enso_cache[guildid]["Prefix"] = prefix


# Deleting the key - value pair for guild
def del_cache_prefix(guildid):
    del enso_cache[guildid]["Prefix"]


# Get the prefix of the guild that the user is in
def get_prefix_for_guild(guildid):
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


# Returns a list of all the cogs
def extensions():
    ext = ['cogs.interactive', 'cogs.anime', 'cogs.relationship',
           'cogs.info', 'cogs.fun', 'cogs.enso',
           'cogs.guild', 'cogs.moderation']

    return ext


async def storeRoles(target, ctx, member):
    """Storing User Roles within Database"""
    role_ids = ", ".join([str(r.id) for r in target.roles])

    # Setup pool
    pool = await connection(db.loop)

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


async def clearRoles(ctx, member, pool):
    """Clear the roles when the user has been unmuted"""

    # Setup up pool connection and cursor
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Clear the existing roles of the user from the database
            update_query = """UPDATE members SET mutedroles = NULL WHERE guildID = (%s) AND discordID = (%s)"""
            update_vals = ctx.guild.id, member.id

            # Execute the query
            await cur.execute(update_query, update_vals)
            await conn.commit()
            print(cur.rowcount, f"Roles Cleared For User {member} in {ctx.guild.name}")


# Run the async function to store everything in cache
loop = asyncio.get_event_loop()
loop.run_until_complete(startup_cache_log())

# --------------------------------------------!End Cogs/Set Values Section!---------------------------------------------
