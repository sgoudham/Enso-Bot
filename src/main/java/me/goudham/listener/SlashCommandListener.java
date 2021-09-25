package me.goudham.listener;

import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandHandler;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.jetbrains.annotations.NotNull;

@Singleton
public class SlashCommandListener extends ListenerAdapter {
    private final CommandHandler commandHandler;

    @Inject
    public SlashCommandListener(CommandHandler commandHandler) {
        this.commandHandler = commandHandler;
    }

    @Override
    public void onSlashCommand(@NotNull SlashCommandEvent event) {
        if (event.getGuild() == null) return;
        commandHandler.handle(event);
    }
}
