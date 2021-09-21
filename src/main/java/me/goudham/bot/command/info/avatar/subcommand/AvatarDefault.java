package me.goudham.bot.command.info.avatar.subcommand;

import jakarta.inject.Inject;
import me.goudham.bot.command.ISlashCommand;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SubCommand;
import me.goudham.service.EmbedGenerator;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.InteractionHook;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;

@SubCommand(
        commandParent = "avatar",
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
public class AvatarDefault implements ISlashCommand {
    private final EmbedGenerator embedGenerator;

    @Inject
    public AvatarDefault(EmbedGenerator embedGenerator) {
        this.embedGenerator = embedGenerator;
    }

    @Override
    public void handle(SlashCommandEvent event) {
        event.deferReply(false).queue();
        InteractionHook hook = event.getHook();

        OptionMapping optionalUser = event.getOption("member");
        User user = optionalUser == null ? event.getUser() : optionalUser.getAsUser();

        MessageEmbed avatarEmbed = embedGenerator.getBaseEmbed()
                .setAuthor(user.getName() + "'s Avatar")
                .setImage(user.getEffectiveAvatarUrl() + "?size=4096")
                .build();

        hook.sendMessageEmbeds(avatarEmbed).queue();
    }
}
