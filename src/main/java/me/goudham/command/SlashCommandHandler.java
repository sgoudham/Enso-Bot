package me.goudham.command;

import io.micronaut.inject.ExecutableMethod;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.Map;
import me.goudham.domain.Pair;
import net.dv8tion.jda.api.events.Event;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

@Singleton
public class SlashCommandHandler implements CommandHandler {
    private final Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap;

    @Inject
    public SlashCommandHandler(Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap) {
        this.commandMap = commandMap;
    }

    @Override
    public void handle(Event event) {
        SlashCommandEvent slashCommandEvent = (SlashCommandEvent) event;
        String commandPath = slashCommandEvent.getCommandPath();

        Pair<Object, ExecutableMethod<Object, Object>> slashCommandPair = commandMap.get(commandPath);
        Object slashCommandBean = slashCommandPair.left();
        ExecutableMethod<Object, Object> slashCommandMethod = slashCommandPair.right();

        slashCommandMethod.invoke(slashCommandBean, slashCommandEvent);
    }
}
