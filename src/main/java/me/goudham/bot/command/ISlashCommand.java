package me.goudham.bot.command;

import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public interface ISlashCommand {
    void handle(SlashCommandEvent event);
}
