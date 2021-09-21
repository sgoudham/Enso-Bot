package me.goudham.bot.command.info.avatar;

import me.goudham.command.annotation.SlashCommand;

@SlashCommand(
        name = "avatar",
        description = "Display your avatar",
        isVisible = true,
        subCommands = { "default", "greyscale" }
)
public class Avatar {
}
