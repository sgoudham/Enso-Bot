package me.goudham.command;

import io.micronaut.core.annotation.Introspected;
import io.micronaut.inject.ExecutableMethod;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;
import net.dv8tion.jda.internal.utils.tuple.Pair;

@Singleton
@Introspected
public class SlashCommandManager implements CommandManager {
    private final Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap = new HashMap<>();
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
        String commandPath = slashCommandEvent.getCommandPath();

        Pair<Object, ExecutableMethod<Object, Object>> slashCommandPair = commandMap.get(commandPath);
        Object bean = slashCommandPair.getLeft();
        ExecutableMethod<Object, Object> method = slashCommandPair.getRight();

        method.invoke(bean, slashCommandEvent);
    }
}
