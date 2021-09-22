package me.goudham.bot.command.info;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.service.EmbedService;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.InteractionHook;

@SlashCommand(name = "ping", description = "Display the latency of the bot", isVisible = true)
public class Ping {
    private final EmbedService embedService;

    @Inject
    public Ping(EmbedService embedService) {
        this.embedService = embedService;
    }

    @Executable
    public void handle(SlashCommandEvent event) {
        event.deferReply(false).queue();
        InteractionHook hook = event.getHook();
        JDA jda = event.getJDA();

        jda.getRestPing().queue(ping -> hook.sendMessageEmbeds(embedService.getBaseEmbed().setDescription("**Rest ping: " + ping + "ms**\n**WS ping: " + jda.getGatewayPing() + "ms**").build()).queue());
    }
}