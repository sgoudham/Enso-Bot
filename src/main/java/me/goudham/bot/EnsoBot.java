package me.goudham.bot;

import io.micronaut.context.annotation.Value;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandManager;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;

@Singleton
public class EnsoBot implements Bot {
    private final JDA jda;
    private final Guild guild;
    private final boolean registerCommands;
    private final CommandManager commandManager;

    @Inject
    public EnsoBot(JDA jda,
                   Guild guild,
                   @Value("${bot.config.registerCommands}") boolean registerCommands,
                   CommandManager commandManager) {
        this.jda = jda;
        this.guild = guild;
        this.registerCommands = registerCommands;
        this.commandManager = commandManager;
    }

    @Override
    public void startup() throws InterruptedException {
        jda.awaitReady();

        if (registerCommands) {
            commandManager.registerSlashCommands(guild);
        } else {
            commandManager.populateCommandMap();
        }
    }
}
