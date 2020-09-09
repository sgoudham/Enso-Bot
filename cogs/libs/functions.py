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
