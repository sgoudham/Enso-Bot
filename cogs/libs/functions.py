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


def get_region(disc_region):
    """Return Nicer Looking Region String"""

    for key in region:
        if key == disc_region:
            return region[key]
