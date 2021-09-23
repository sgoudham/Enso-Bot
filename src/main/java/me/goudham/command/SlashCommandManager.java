package me.goudham.command;

import io.micronaut.context.annotation.Value;
import io.micronaut.core.annotation.Introspected;
import io.micronaut.inject.ExecutableMethod;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.List;
import java.util.Map;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;
import net.dv8tion.jda.internal.utils.tuple.Pair;

@Singleton
@Introspected
public class SlashCommandManager implements CommandManager {
    private final Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap;
    private final boolean registerCommandsGlobally;
    private final boolean registerCommandsForGuild;
    private final CommandLoader commandLoader;
    private final JDA jda;

    @Inject
    public SlashCommandManager(Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap,
                               @Value("${bot.config.registerCommandsGlobally}") boolean registerCommandsGlobally,
                               @Value("${bot.config.registerCommandsForGuild}") boolean registerCommandsForGuild,
                               CommandLoader commandLoader,
                               JDA jda) {
        this.commandMap = commandMap;
        this.registerCommandsGlobally = registerCommandsGlobally;
        this.registerCommandsForGuild = registerCommandsForGuild;
        this.commandLoader = commandLoader;
        this.jda = jda;
    }

    @Override
    public void populateCommandMap() {
        commandLoader.populateCommandMap();
    }

    @Override
    public void registerSlashCommands(Guild guild) {
        CommandListUpdateAction commands = null;
        if (registerCommandsGlobally) commands = jda.updateCommands();
        if (registerCommandsForGuild) commands = guild.updateCommands();

        if (commands != null) {
            List<CommandData> registeredSlashCommands = commandLoader.registerSlashCommands();
            commands.addCommands(registeredSlashCommands).queue();
        }
    }

    @Override
    public void handleSlashCommandEvent(SlashCommandEvent slashCommandEvent) {
        String commandPath = slashCommandEvent.getCommandPath();

        Pair<Object, ExecutableMethod<Object, Object>> slashCommandPair = commandMap.get(commandPath);
        Object slashCommandBean = slashCommandPair.getLeft();
        ExecutableMethod<Object, Object> slashCommandMethod = slashCommandPair.getRight();

        slashCommandMethod.invoke(slashCommandBean, slashCommandEvent);
    }
}
