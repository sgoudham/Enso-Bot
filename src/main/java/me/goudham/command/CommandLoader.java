package me.goudham.command;

import java.util.List;
import java.util.Map;
import me.goudham.bot.command.ISlashCommand;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;

public interface CommandLoader {
    List<CommandData> loadIntoMapAndReturnCommands(Map<String, ISlashCommand> commandMap);
}
