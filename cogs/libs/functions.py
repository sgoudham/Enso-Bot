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

# Using frozenset
# Permissions to filter through
perms = frozenset(
    {
        "create instant invite",
        "add reactions",
        "view audit log",
        "priority speaker",
        "stream",
        "read messages",
        "send messages",
        "send tts messages",
        "embed links",
        "attach links",
        "read message history",
        "external emojis",
        "view guild insights",
        "connect",
        "speak",
        "use voice activation",
        "change nickname"
    }
)

# List of regions mapped to emojis
region = {
    "eu-central": ":flag_eu: Central Europe",
    "europe": ":flag_eu: Central Europe",
    "singapore": ":flag_sg: Singapore",
    "india": ":flag_in: India",
    "japan": ":flag_jp: Japan",
    "us-central": ":flag_us: U.S. Central",
    "sydney": ":flag_au: Sydney",
    "us-east": ":flag_us: U.S. East",
    "us-south": ":flag_us: U.S. South",
    "us-west": ":flag_us: U.S. West",
    "eu-west": ":flag_eu: Western Europe",
    "vip-us-east": ":flag_us: VIP U.S. East",
    "london": ":flag_gb: London",
    "amsterdam": ":flag_nl: Amsterdam",
    "hongkong": ":flag_hk: Hong Kong",
    "russia": ":flag_ru: Russia",
    "southafrica": ":flag_za:  South Africa",
    "brazil": ":flag_br: Brazil"
}

# List of content filters and their descriptions
filters = {
    "disabled": "<:xMark:746834944629932032>",
    "no_role": "<:greenTick:746834932936212570> For Members Without Roles",
    "all_members": "<:greenTick:746834932936212570> For All Members"
}

# List of default notifications settings for guild
notifs = {
    "all_messages": "<:greenTick:746834932936212570> For All Messages",
    "only_mentions": "<:greenTick:746834932936212570> For All Mentions"
}


def detect_perms(message, fset):
    """Filter out permissions that are not important"""

    # Split the message individual permissions
    message = message.split(",")

    # Filter the permission out if it's in the frozenset
    filtered = filter(lambda perm: perm not in fset, message)
    return ", ".join(filtered)


def string_list(types, n, instance):
    """Return objects in nicely formatted strings"""

    if len(types) > n:
        # Retrieve the length of the remaining roles
        length = len(types) - n

        if instance == "Emoji":
            # Store the first 20 emojis in a string
            string = f"{' '.join(map(str, (types[:n])))} and **{length}** more..."
        else:
            # Store the first n roles/members in a string called "roles" (highest to lowest)
            string = f"{' **|** '.join(_type.mention for _type in list(reversed(types))[:n])} and **{length}** more"

    else:
        if instance == "Role":
            # Display all roles as it is lower than n provided
            string = f"{' **|** '.join(role.mention for role in list(reversed(types[1:])))}"
        elif instance == "Emoji":
            # Display all the emojis in the server as it is less than 20
            string = " ".join(map(str, types))
        else:
            # Display all members as it is lower than n provided
            string = f"{' **|** '.join(role.mention for role in list(reversed(types)))}"

    return string


def get_region(disc_region):
    """Return Nicer Looking Region String"""

    for key in region:
        if key == disc_region:
            return region[key]


def get_content_filter(content_filter):
    """Return nicer looking content filter string"""

    for key in filters:
        if key == content_filter:
            return filters[key]


def get_notifs(notif):
    """Return nicer looking notification string"""

    for key in notifs:
        if key == notif:
            return notifs[key]
