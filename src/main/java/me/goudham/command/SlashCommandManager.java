package me.goudham.command;

import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import me.goudham.bot.command.ISlashCommand;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;

@Singleton
@Introspected
public class SlashCommandManager implements CommandManager {
    private final Map<String, ISlashCommand> commandMap = new HashMap<>();
    private final CommandLoader commandLoader;

    @Inject
    public SlashCommandManager(CommandLoader commandLoader) {
        this.commandLoader = commandLoader;
    }

    @Override
    public void registerSlashCommands(Guild guild) {
        CommandListUpdateAction commands = guild.updateCommands();
        List<CommandData> commandDataList = commandLoader.loadIntoMapAndReturnCommands(commandMap);
        commands.addCommands(commandDataList).queue();
    }

    @Override
    public void handleSlashCommandEvent(SlashCommandEvent slashCommandEvent) {
        String name = slashCommandEvent.getName();
        ISlashCommand slashCommand = commandMap.get(name);
        slashCommand.handle(slashCommandEvent);
    }
}
