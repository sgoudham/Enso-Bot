package me.goudham.listener;

import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandManager;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.jetbrains.annotations.NotNull;

@Singleton
public class SlashCommandListener extends ListenerAdapter {
    private final CommandManager commandManager;

    @Inject
    public SlashCommandListener(CommandManager commandManager) {
        this.commandManager = commandManager;
    }

    @Override
    public void onSlashCommand(@NotNull SlashCommandEvent event) {
        if (event.getGuild() == null) return;
        commandManager.handleSlashCommandEvent(event);
    }
}
