package me.goudham.bot.command.misc;

import jakarta.inject.Inject;
import me.goudham.bot.command.ISlashCommand;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.service.EmbedGenerator;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.InteractionHook;

@SlashCommand(name = "ping", description = "Display the latency of the bot", isVisible = true)
public class Ping implements ISlashCommand {
    private final EmbedGenerator embedGenerator;

    @Inject
    public Ping(EmbedGenerator embedGenerator) {
        this.embedGenerator = embedGenerator;
    }

    @Override
    public void handle(SlashCommandEvent event) {
        event.deferReply(false).queue();
        InteractionHook hook = event.getHook();
        JDA jda = event.getJDA();

        jda.getRestPing().queue(ping -> hook.sendMessageEmbeds(embedGenerator.getBaseEmbed().setDescription("**Rest ping: " + ping + "ms**\n**WS ping: " + jda.getGatewayPing() + "ms**").build()).queue());
    }
}