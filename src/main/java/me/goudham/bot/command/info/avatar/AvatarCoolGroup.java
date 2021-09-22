package me.goudham.bot.command.info.avatar;

import io.micronaut.context.annotation.Executable;
import me.goudham.command.annotation.SubCommand;
import me.goudham.command.annotation.SubCommandGroup;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

@SubCommandGroup(parent = "avatar", name = "cool", description = "Just really cool stuff ya know")
public class AvatarCoolGroup {

    @Executable
    @SubCommand(name = "one", description = "just a really cool method that is called one")
    public void oneCommand(SlashCommandEvent slashCommandEvent) {

    }

    @Executable
    @SubCommand(name = "two", description = "just a really cool method that is called two")
    public void twoCommand(SlashCommandEvent slashCommandEvent) {

    }
}
