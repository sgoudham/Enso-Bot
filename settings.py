from discord import Colour

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

# Allowed channel for Enso~Chan commands
channels = ["enso-chan-commands", "picto-chat", 663651584399507481]

# Grabbing the list of colours
colour_list = [c for c in colors.values()]

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
           'cogs.modmail']

    return ext
