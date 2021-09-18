package me.goudham.command;

import io.micronaut.core.annotation.Introspected;
import io.micronaut.inject.BeanDefinition;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;

@Singleton
@Introspected
public class CommandManager {
    private final Map<String, BeanDefinition<?>> commandMap = new HashMap<>();
    private final CommandLoader commandLoader;

    @Inject
    public CommandManager(CommandLoader commandLoader) {
        this.commandLoader = commandLoader;
    }

    public void registerSlashCommands(Guild guild) {
        CommandListUpdateAction commands = guild.updateCommands();
        List<CommandData> commandDataList = commandLoader.loadIntoMapAndReturnCommands(commandMap);
        commands.addCommands(commandDataList).queue();
    }
}
