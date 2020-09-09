def string_list(types, n, instance):
    """Return objects in nicely formatted strings"""

    if len(types) > n:
        # Retrieve the length of the remaining roles
        length = len(types) - n

        # Store the first nn roles in a string called "roles" (highest to lowest)
        role = f"{' **|** '.join(_type.mention for _type in list(reversed(types))[:n])} and **{length}** more"

    else:
        if instance == "Role":
            # Display all roles as it is lower than n provided
            role = f"{' **|** '.join(role.mention for role in list(reversed(types[1:])))}"
        else:
            # Display all roles as it is lower than n provided
            role = f"{' **|** '.join(role.mention for role in list(reversed(types)))}"

    return role
