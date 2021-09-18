package me.goudham.bot;

import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandManager;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;

@Singleton
public class Enso implements Bot {
    private final JDA bot;
    private final Guild guild;
    private final CommandManager commandManager;

    @Inject
    public Enso(JDA bot, Guild guild, CommandManager commandManager) {
        this.bot = bot;
        this.guild = guild;
        this.commandManager = commandManager;
    }

    @Override
    public void startup() {
        commandManager.registerSlashCommands(guild);
    }
}
