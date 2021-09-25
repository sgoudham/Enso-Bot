package me.goudham.bot;

import io.micronaut.context.annotation.Value;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandManager;
import net.dv8tion.jda.api.entities.Guild;

@Singleton
public class EnsoBot implements Bot {
    private final Guild guild;
    private final boolean registerCommands;
    private final CommandManager commandManager;

    @Inject
    public EnsoBot(Guild guild,
                   @Value("${bot.config.registerCommands}") boolean registerCommands,
                   CommandManager commandManager) {
        this.guild = guild;
        this.registerCommands = registerCommands;
        this.commandManager = commandManager;
    }

    @Override
    public void startup() {
        if (registerCommands) {
            commandManager.registerSlashCommands(guild);
        } else {
            commandManager.populateCommandMap();
        }
    }
}
