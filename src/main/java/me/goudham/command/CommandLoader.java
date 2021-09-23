package me.goudham.command;

import java.util.List;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;

public interface CommandLoader {
    void populateCommandMap();
    List<CommandData> registerSlashCommands();
}
