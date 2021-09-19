package me.goudham.bot;

import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import me.goudham.command.CommandManager;
import me.goudham.listener.SlashCommandListener;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;

@Singleton
public class EnsoBot implements Bot {
    private final JDA jda;
    private final Guild guild;
    private final CommandManager commandManager;

    @Inject
    public EnsoBot(JDA jda, Guild guild, CommandManager commandManager) {
        this.jda = jda;
        this.guild = guild;
        this.commandManager = commandManager;
    }

    @Override
    public void startup() throws InterruptedException {
        jda.awaitReady();
        addEventListeners();
        commandManager.registerSlashCommands(guild);
    }

    private void addEventListeners() {
        jda.addEventListener(new SlashCommandListener(commandManager));
    }
}
