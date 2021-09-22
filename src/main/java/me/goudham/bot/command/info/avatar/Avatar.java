package me.goudham.bot.command.info.avatar;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.service.EmbedService;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.InteractionHook;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;

@SlashCommand(name = "avatar", description = "Display your avatar", isVisible = true, subCommandGroups = { "cool" })
public class Avatar {
    private final EmbedService embedService;

    @Inject
    public Avatar(EmbedService embedService) {
        this.embedService = embedService;
    }

    @Executable
    @SubCommand(
            name = "grayscale",
            description = "Display your or another member's avatar with a grayscale filter applied",
            options = {
                    @Option(
                            optionType = OptionType.USER,
                            name = "member",
                            description = "A member within the server",
                            isRequired = false
                    )
            }
    )
    public void grayscaleCommand(SlashCommandEvent slashCommandEvent) {

    }

    @Executable
    @SubCommand(
            name = "default",
            description = "Display your or another member's avatar",
            options = {
                    @Option(
                            optionType = OptionType.USER,
                            name = "member",
                            description = "A member within the server",
                            isRequired = false
                    )
            }
    )
    public void defaultCommand(SlashCommandEvent slashCommandEvent) {
        slashCommandEvent.deferReply(false).queue();
        InteractionHook hook = slashCommandEvent.getHook();

        OptionMapping optionalUser = slashCommandEvent.getOption("member");
        User user = optionalUser == null ? slashCommandEvent.getUser() : optionalUser.getAsUser();

        MessageEmbed avatarEmbed = embedService.getBaseEmbed()
                .setAuthor(user.getName() + "'s Avatar")
                .setImage(user.getEffectiveAvatarUrl() + "?size=4096")
                .build();

        hook.sendMessageEmbeds(avatarEmbed).queue();
    }
}
