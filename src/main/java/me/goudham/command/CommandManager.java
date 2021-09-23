package me.goudham.command;

import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

public interface CommandManager {
    void populateCommandMap();
    void registerSlashCommands(Guild guild);
    void handleSlashCommandEvent(SlashCommandEvent slashCommandEvent);
}
