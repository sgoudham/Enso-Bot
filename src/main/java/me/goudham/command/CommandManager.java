package me.goudham.command;

import net.dv8tion.jda.api.entities.Guild;

public interface CommandManager {
    void populateCommandMap();
    void registerSlashCommands(Guild guild);
}
