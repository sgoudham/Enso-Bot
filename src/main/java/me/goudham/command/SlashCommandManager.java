package me.goudham.command;

import io.micronaut.context.annotation.Value;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.List;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;

@Singleton
public class SlashCommandManager implements CommandManager {
    private final boolean registerCommandsGlobally;
    private final boolean registerCommandsForGuild;
    private final CommandLoader commandLoader;
    private final JDA jda;

    @Inject
    public SlashCommandManager(@Value("${bot.config.registerCommandsGlobally}") boolean registerCommandsGlobally,
                               @Value("${bot.config.registerCommandsForGuild}") boolean registerCommandsForGuild,
                               CommandLoader commandLoader,
                               JDA jda) {
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
}
