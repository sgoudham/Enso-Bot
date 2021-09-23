package me.goudham.bot.command.info;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URL;
import javax.imageio.ImageIO;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.service.EmbedService;
import me.goudham.service.ImageService;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;

@SlashCommand(name = "avatar", description = "Display your avatar", isVisible = true)
public class Avatar {
    private final EmbedService embedService;
    private final ImageService imageService;

    @Inject
    public Avatar(EmbedService embedService, ImageService imageService) {
        this.embedService = embedService;
        this.imageService = imageService;
    }

    @Executable
    @SubCommand(
            name = "invert",
            description = "Display your or another member's avatar with a negative filter applied",
            options = {
                    @Option(
                            optionType = OptionType.USER,
                            name = "member",
                            description = "A member within the server",
                            isRequired = false
                    )
            }
    )
    public void invertCommand(SlashCommandEvent slashCommandEvent) throws IOException {
        OptionMapping optionalUser = slashCommandEvent.getOption("member");
        User user = optionalUser == null ? slashCommandEvent.getUser() : optionalUser.getAsUser();

        BufferedImage inputImage = ImageIO.read(new URL(user.getEffectiveAvatarUrl()));
        imageService.invertImage(inputImage);

        MessageEmbed avatarEmbed = embedService.getBaseEmbed()
                .setAuthor(user.getName() + "'s Avatar\nFilter Applied -> Negative")
                .setImage("attachment://invert.png")
                .build();

        byte[] imageByteArray = imageService.toByteArray(inputImage, "png");
        slashCommandEvent.replyEmbeds(avatarEmbed).addFile(imageByteArray, "invert.png").queue();
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
    public void grayscaleCommand(SlashCommandEvent slashCommandEvent) throws IOException {
        OptionMapping optionalUser = slashCommandEvent.getOption("member");
        User user = optionalUser == null ? slashCommandEvent.getUser() : optionalUser.getAsUser();

        BufferedImage inputImage = ImageIO.read(new URL(user.getEffectiveAvatarUrl()));
        BufferedImage grayscaleImage = imageService.toGrayscaleImage(inputImage);

        MessageEmbed avatarEmbed = embedService.getBaseEmbed()
                .setAuthor(user.getName() + "'s Avatar\nFilter Applied -> Grayscale")
                .setImage("attachment://grayscale.png")
                .build();

        byte[] imageByteArray = imageService.toByteArray(grayscaleImage, "png");
        slashCommandEvent.replyEmbeds(avatarEmbed).addFile(imageByteArray, "grayscale.png").queue();
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
        OptionMapping optionalUser = slashCommandEvent.getOption("member");
        User user = optionalUser == null ? slashCommandEvent.getUser() : optionalUser.getAsUser();

        MessageEmbed avatarEmbed = embedService.getBaseEmbed()
                .setAuthor(user.getName() + "'s Avatar")
                .setImage(user.getEffectiveAvatarUrl() + "?size=4096")
                .build();

        slashCommandEvent.replyEmbeds(avatarEmbed).queue();
    }
}
