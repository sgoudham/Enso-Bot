package me.goudham.bot.command.info;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import java.awt.Color;
import java.util.EnumSet;
import java.util.List;
import java.util.StringJoiner;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.domain.Constants;
import me.goudham.service.EmbedService;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.utils.concurrent.Task;
import org.jetbrains.annotations.NotNull;

@SlashCommand(name = "info")
public class Info {
    private final EmbedService embedService;

    @Inject
    public Info(EmbedService embedService) {
        this.embedService = embedService;
    }

    @SuppressWarnings("ConstantConditions")
    @Executable
    @SubCommand(
            name = "user",
            description = "Retrieve your or another member's information",
            options = {
                    @Option(
                            optionType = OptionType.USER,
                            name = "member",
                            description = "A member within the server",
                            isRequired = false
                    )
            }
    )
    public void userCommand(@NotNull SlashCommandEvent slashCommandEvent) {
        OptionMapping optionalMember = slashCommandEvent.getOption("member");
        Member member = optionalMember == null ? slashCommandEvent.getMember() : optionalMember.getAsMember();

        MessageEmbed messageEmbed = embedService.getBaseEmbed()
                .setTitle(getMemberOnlineStatus(member) + " " + member.getUser().getAsTag() + " " + getMemberBadges(member))
                .setColor(getMemberColour(member))
                .setThumbnail(member.getUser().getEffectiveAvatarUrl() + "?size=4096")
                .addField("Registered", getRegisteredDate(member), false)
                .addField("Joined", getJoinedDate(member), false)
                .addField("Top Role", getTopRole(member), false)
                .addField("Roles (" + member.getRoles().size() + ")", getMemberRoles(member, 20), false)
                .setFooter("ID: " + member.getId())
                .build();

        slashCommandEvent.replyEmbeds(messageEmbed).queue();
    }

    @SuppressWarnings("ConstantConditions")
    @Executable
    @SubCommand(
            name = "role",
            description = "Retrieve your highest role or another role's information",
            options = {
                    @Option(
                            optionType = OptionType.ROLE,
                            name = "role",
                            description = "A role within the server",
                            isRequired = false
                    )
            }
    )
    public void roleCommand(@NotNull SlashCommandEvent slashCommandEvent) {
        OptionMapping optionalRole = slashCommandEvent.getOption("role");
        Guild guild = slashCommandEvent.getGuild();
        Role role;

        if (optionalRole == null) {
            Member member = slashCommandEvent.getMember();
            if (member == null) return;
            if (member.getRoles().isEmpty()) {
                slashCommandEvent.reply("No Role Given").queue();
                return;
            } else {
                role = member.getRoles().get(0);
            }
        } else {
            role = optionalRole.getAsRole();
        }

        Task<List<Member>> membersWithRoles = guild.findMembersWithRoles(role);
        String roleColour = role.getColor() == null ? "N/A" : getColorAsHex(role.getColor());

        String isMentionable = role.isMentionable() ? Constants.CHECK : Constants.CROSS;
        String isHoisted = role.isHoisted() ? Constants.CHECK : Constants.CROSS;
        String isManaged = role.isManaged() ? Constants.CHECK : Constants.CROSS;
        String miscString = "Mentionable: " + isMentionable
                + "\n" + "Hoisted: " + isHoisted
                + "\n" + "Managed: " + isManaged;

        EnumSet<Permission> permissions = role.getPermissions(slashCommandEvent.getGuildChannel());
        System.out.println(permissions);

        membersWithRoles.onSuccess(members -> {
            long humanCount = members.stream().filter(member -> !member.getUser().isBot()).count();
            long botCount = members.stream().filter(member -> member.getUser().isBot()).count();

            MessageEmbed messageEmbed = embedService.getBaseEmbed()
                    .setTitle(role.getName() + " Information")
                    .setDescription(role.getAsMention() + "\n" + "**Colour:** " + roleColour)
                    .setColor(role.getColor())
                    .setThumbnail(guild.getIconUrl() + "?size=4096")
                    .addField("Creation At", getCreationDate(role), false)
                    .addField("Members (" + members.size() + ")", "Humans: " + humanCount + "\nBots: " + botCount, true)
                    .addField("Misc", miscString, true)
                    .addField("List of Members (" + members.size() + ")", getListOfMembers(members, 20), false)
                    .setFooter("ID: " + role.getId())
                    .build();

            slashCommandEvent.replyEmbeds(messageEmbed).queue();
        });
    }

    private @NotNull String getColorAsHex (@NotNull Color color) {
        return "#" + Integer.toHexString(color.getRGB()).toUpperCase();
    }

    private Color getMemberColour(@NotNull Member member) {
        return member.getColor() == null ? Color.BLACK : member.getColor();
    }

    private @NotNull String getMemberBadges(@NotNull Member member) {
        User user = member.getUser();
        String memberBadges = "";

        if (user.isBot()) memberBadges += Constants.BADGE_BOT;
        if (member.getTimeBoosted() != null) memberBadges += Constants.BADGE_SERVER_BOOST;

        memberBadges += user.getFlags().toString()
                .substring(1, user.getFlags().toString().length() - 1)
                .replace(",", "")
                .replace("PARTNER", Constants.BADGE_PARTNER)
                .replace("HYPESQUAD_BRAVERY", Constants.BADGE_BRAVERY)
                .replace("HYPESQUAD_BRILLIANCE", Constants.BADGE_BRILLIANCE)
                .replace("HYPESQUAD_BALANCE", Constants.BADGE_BALANCE)
                .replace("VERIFIED_DEVELOPER", Constants.BADGE_EARLY_VERIFIED_BOT_DEVELOPER)
                .replace("EARLY_SUPPORTER", Constants.BADGE_EARLY_SUPPORTER)
                .replace("SYSTEM", Constants.BADGE_STAFF)
                .replace("BUG_HUNTER_LEVEL_1", Constants.BADGE_BUG_HUNTER)
                .replace("BUG_HUNTER_LEVEL_2", Constants.BADGE_BUG_HUNTER)
                .replace("VERIFIED_BOT", Constants.BADGE_VERIFIED_BOT);

        return memberBadges;
    }

    private @NotNull String getMemberOnlineStatus(@NotNull Member member) {
        return member.getOnlineStatus().toString()
                .replace("ONLINE", Constants.STATUS_ONLINE)
                .replace("IDLE", Constants.STATUS_IDLE)
                .replace("DO_NOT_DISTURB", Constants.STATUS_DND)
                .replace("OFFLINE", Constants.STATUS_OFFLINE)
                .replace("STREAMING", Constants.STATUS_STREAMING);
    }

    private @NotNull String getTopRole(@NotNull Member member) {
        List<Role> memberRoles = member.getRoles();
        if (memberRoles.isEmpty()) return "No Roles";

        return memberRoles.get(0).getAsMention();
    }

    private String getListOfMembers(@NotNull List<Member> members, int limit) {
        StringJoiner memberJoiner = new StringJoiner(" **|** ");
        if (members.isEmpty()) return "No Members In Role";

        members.stream()
                .limit(limit)
                .forEach(member -> memberJoiner.add(member.getAsMention()));

        if (members.size() > limit) {
            int leftOverMembers = members.size() - limit;
            memberJoiner.add(" and ** " + leftOverMembers + " ** more ");
        }

        return memberJoiner.toString();
    }

    private String getMemberRoles(@NotNull Member member, int limit) {
        StringJoiner memberRolesJoiner = new StringJoiner(" **|** ");
        List<Role> memberRoles = member.getRoles();
        if (memberRoles.isEmpty()) return "No Roles";

        memberRoles.stream()
                .limit(limit)
                .forEach(role -> memberRolesJoiner.add(role.getAsMention()));

        if (memberRoles.size() > limit) {
            int leftOverRoles = memberRoles.size() - limit;
            memberRolesJoiner.add(" and ** " + leftOverRoles + " ** more ");
        }

        return memberRolesJoiner.toString();
    }

    private @NotNull String getCreationDate(@NotNull Role role) {
        long timeCreated = role.getTimeCreated().toInstant().getEpochSecond();
        return "<t:" + timeCreated + ":F>";
    }

    private @NotNull String getRegisteredDate(@NotNull Member member) {
        long timeCreated = member.getTimeCreated().toInstant().getEpochSecond();
        return "<t:" + timeCreated + ":F>";
    }

    private @NotNull String getJoinedDate(@NotNull Member member) {
        long timeJoined = member.getTimeJoined().toInstant().getEpochSecond();
        return "<t:" + timeJoined + ":F>";
    }
}
