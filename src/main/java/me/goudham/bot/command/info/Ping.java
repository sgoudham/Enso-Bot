package me.goudham.bot.command.info;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.util.EmbedUtil;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;

@SlashCommand(name = "ping", description = "Display the latency of the bot")
public class Ping {
    private final EmbedUtil embedUtil;

    @Inject
    public Ping(EmbedUtil embedUtil) {
        this.embedUtil = embedUtil;
    }

    @Executable
    public void handle(SlashCommandEvent slashCommandEvent) {
        JDA jda = slashCommandEvent.getJDA();
        jda.getRestPing().queue(ping -> {
            MessageEmbed messageEmbed = embedUtil.getBaseEmbed()
                    .setDescription("**Rest ping: " + ping + "ms**\n**WS ping: " + jda.getGatewayPing() + "ms**")
                    .build();
            slashCommandEvent.replyEmbeds(messageEmbed).queue();
        });
    }
}