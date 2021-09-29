package me.goudham.bot.command.info;

import io.micronaut.context.annotation.Executable;
import jakarta.inject.Inject;
import java.util.EnumSet;
import java.util.List;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.domain.Constants;
import me.goudham.service.EmbedService;
import me.goudham.service.InfoUtil;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.Permission;
import net.dv8tion.jda.api.Region;
import net.dv8tion.jda.api.entities.ChannelType;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.GuildChannel;
import net.dv8tion.jda.api.entities.Member;
import net.dv8tion.jda.api.entities.MessageEmbed;
import net.dv8tion.jda.api.entities.Role;
import net.dv8tion.jda.api.entities.TextChannel;
import net.dv8tion.jda.api.entities.VoiceChannel;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.utils.cache.MemberCacheView;
import net.dv8tion.jda.api.utils.concurrent.Task;
import org.jetbrains.annotations.NotNull;

@SlashCommand(name = "info")
public class Info {
    private final EmbedService embedService;
    private final InfoUtil infoUtil;

    @Inject
    public Info(EmbedService embedService, InfoUtil infoUtil) {
        this.embedService = embedService;
        this.infoUtil = infoUtil;
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
                .setTitle(infoUtil.getMemberOnlineStatus(member) + " " + member.getUser().getAsTag() + " " + infoUtil.getMemberBadges(member))
                .setColor(infoUtil.getMemberColour(member))
                .setThumbnail(member.getUser().getEffectiveAvatarUrl() + "?size=4096")
                .addField("Registered", infoUtil.getCreationDate(member), false)
                .addField("Joined", infoUtil.getJoinedDate(member), false)
                .addField("Top Role", infoUtil.getTopRole(member), false)
                .addField("Roles (" + member.getRoles().size() + ")", infoUtil.getMemberRoles(member, 20), false)
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
        String roleColour = role.getColor() == null ? "N/A" : infoUtil.getColorAsHex(role.getColor());

        String isMentionable = role.isMentionable() ? Constants.CHECK : Constants.CROSS;
        String isHoisted = role.isHoisted() ? Constants.CHECK : Constants.CROSS;
        String isManaged = role.isManaged() ? Constants.CHECK : Constants.CROSS;
        String miscString = """
                Mentionable: $isMentionable
                Hoisted: $isHoisted
                Managed: $isManaged
                """
                .replace("$isMentionable", isMentionable)
                .replace("$isHoisted", isHoisted)
                .replace("$isManaged", isManaged);

        EnumSet<Permission> permissions = role.getPermissions(slashCommandEvent.getGuildChannel());
        System.out.println(permissions);

        membersWithRoles.onSuccess(members -> {
            long humanCount = members.stream().filter(member -> !member.getUser().isBot()).count();
            long botCount = members.stream().filter(member -> member.getUser().isBot()).count();

            MessageEmbed messageEmbed = embedService.getBaseEmbed()
                    .setTitle("@" + role.getName() + " Information")
                    .setDescription(role.getAsMention() + "\n" + "**Colour:** " + roleColour)
                    .setColor(role.getColor())
                    .setThumbnail(guild.getIconUrl() + "?size=4096")
                    .addField("Creation At", infoUtil.getCreationDate(role), false)
                    .addField("Members (" + members.size() + ")", "Humans: " + humanCount + "\nBots: " + botCount, true)
                    .addField("Misc", miscString, true)
                    .addField("List of Members (" + members.size() + ")", infoUtil.getListOfMembers(members, 20), false)
                    .setFooter("ID: " + role.getId())
                    .build();

            slashCommandEvent.replyEmbeds(messageEmbed).queue();
        });
    }

    @SuppressWarnings("ConstantConditions")
    @Executable
    @SubCommand(
            name = "channel",
            description = "Retrieve the current channel or another channel's information",
            options = {
                    @Option(
                            optionType = OptionType.CHANNEL,
                            name = "channel",
                            description = "A channel within the server",
                            isRequired = false
                    )
            }
    )
    public void channelCommand(@NotNull SlashCommandEvent slashCommandEvent) {
        OptionMapping optionalChannel = slashCommandEvent.getOption("channel");
        JDA jda = slashCommandEvent.getJDA();
        MessageEmbed messageEmbed;

        if (optionalChannel == null) {
            ChannelType channelType = slashCommandEvent.getChannelType();
            if (channelType == ChannelType.TEXT) {
                messageEmbed = handleTextChannel(slashCommandEvent.getTextChannel());
            } else {
                slashCommandEvent.reply("Channel Type Not Supported").queue();
                return;
            }
        } else {
            ChannelType channelType = optionalChannel.getChannelType();
            GuildChannel guildChannel = optionalChannel.getAsGuildChannel();

            if (channelType == ChannelType.TEXT) {
                messageEmbed = handleTextChannel(jda.getTextChannelById(guildChannel.getId()));
            } else if (channelType == ChannelType.VOICE) {
                messageEmbed = handleVoiceChannel(jda.getVoiceChannelById(guildChannel.getId()));
            } else {
                slashCommandEvent.reply("Channel Type Not Supported").queue();
                return;
            }
        }

        slashCommandEvent.replyEmbeds(messageEmbed).queue();
    }

    @SuppressWarnings("ConstantConditions")
    @Executable
    @SubCommand(
            name = "server",
            description = "Retrieve information about the current server you are in"
    )
    public void serverCommand(SlashCommandEvent slashCommandEvent) {
        Guild guild = slashCommandEvent.getGuild();
        MemberCacheView memberCache = guild.getMemberCache();


        String owner = guild.getOwner() == null ? "Unknown Owner" : guild.getOwner().getAsMention();

        long onlineMemberCount = infoUtil.getMemberStatusCount(guild, OnlineStatus.ONLINE);
        long idleMemberCount = infoUtil.getMemberStatusCount(guild, OnlineStatus.IDLE);
        long dndMemberCount = infoUtil.getMemberStatusCount(guild, OnlineStatus.DO_NOT_DISTURB);
        long offlineMemberCount = infoUtil.getMemberStatusCount(guild, OnlineStatus.OFFLINE);
        String statuses = Constants.STATUS_ONLINE + onlineMemberCount
                + Constants.STATUS_IDLE + idleMemberCount
                + Constants.STATUS_DND + dndMemberCount
                + Constants.STATUS_OFFLINE + offlineMemberCount;

        String humanCount = String.valueOf(memberCache.stream().filter(member -> !member.getUser().isBot()).count());
        String botCount = String.valueOf(memberCache.stream().filter(member -> member.getUser().isBot()).count());
        String bannedUsersCount = String.valueOf(guild.retrieveBanList().complete().size());
        String membersString = """
                Humans: $humans
                Bots: $bots
                Banned: $banned
                """
                .replace("$humans", humanCount)
                .replace("$bots", botCount)
                .replace("$banned", bannedUsersCount);

        String textChannelCount = String.valueOf(infoUtil.getChannelCount(guild, ChannelType.TEXT));
        String voiceChannelCount = String.valueOf(infoUtil.getChannelCount(guild, ChannelType.VOICE));
        String categoryChannelCount = String.valueOf(infoUtil.getChannelCount(guild, ChannelType.CATEGORY));
        String channelsString = """
                Text: $text
                Voice: $voice
                Category: $category
                """
                .replace("$text", textChannelCount)
                .replace("$voice", voiceChannelCount)
                .replace("$category", categoryChannelCount);

        String boostingMembers = infoUtil.getListOfMembers(guild.getBoosters(), 10);
        String topRole = infoUtil.getTopRole(guild);
        String allRoles = infoUtil.getGuildRoles(guild, 20);
        String allEmotes = infoUtil.getGuildEmotes(guild, 20);

        String boostCount = String.valueOf(guild.getBoostCount());
        String boostTier = String.valueOf(guild.getBoostTier().getKey());
        String verificationLevel = String.valueOf(guild.getVerificationLevel().getKey());
        String miscString = """
                Boost Tier: $tier
                No. of Boosters: $count
                Verification Level: $verifLevel
                """
                .replace("$tier", boostTier)
                .replace("$count", boostCount)
                .replace("$verifLevel", verificationLevel);

        MessageEmbed messageEmbed = embedService.getBaseEmbed()
                .setTitle("Server Information")
                .setThumbnail(guild.getIconUrl())
                .addField("Owner", owner, false)
                .addField("Created", infoUtil.getCreationDate(guild), false)
                .addField("Statuses", statuses, false)
                .addField("Members (" + memberCache.size() + ")", membersString, true)
                .addField("Channels (" + guild.getChannels().size() + ")", channelsString, true)
                .addField("Misc", miscString, true)
                .addField("Boosting Members (" + boostCount + ")", boostingMembers, false)
                .addField("Top Role", topRole, false)
                .addField("Roles (" + guild.getRoleCache().size() + ")", allRoles, false)
                .addField("Emotes (" + guild.getEmoteCache().size() + ")", allEmotes, false)
                .setFooter("ID: " + guild.getId())
                .build();

        slashCommandEvent.replyEmbeds(messageEmbed).queue();
    }

    private @NotNull MessageEmbed handleVoiceChannel(@NotNull VoiceChannel voiceChannel) {
        String region;
        if (voiceChannel.getRegion() == Region.AUTOMATIC) {
            region = "\uD83C\uDFF3️\u200D\uD83C\uDF08 " + voiceChannel.getRegion().getName();
        } else {
            region = voiceChannel.getRegion().getEmoji() + " " + voiceChannel.getRegion().getName();
        }
        String userLimit = voiceChannel.getUserLimit() == 0 ? "No Limit" : String.valueOf(voiceChannel.getUserLimit());
        String bitrate = voiceChannel.getBitrate() + "bit/s";
        String isSynced = voiceChannel.isSynced() ? Constants.CHECK : Constants.CROSS;
        String category = voiceChannel.getParent() == null ? "No Category" : voiceChannel.getParent().getName();
        String position = "#" + voiceChannel.getPosition();
        String miscString = "Synced: " + isSynced;
        String description = """
                $channelMention
                **Category:** $category
                **Position:** $position
                **Bitrate:** $bitrate
                **User Limit:** $userLimit
                **Region:** $region
                """
                .replace("$channelMention", voiceChannel.getAsMention())
                .replace("$category", category)
                .replace("$position", position)
                .replace("$bitrate", bitrate)
                .replace("$userLimit", userLimit)
                .replace("$region", region);


        return embedService.getBaseEmbed()
                .setTitle("\uD83D\uDD08" + voiceChannel.getName() + " Information")
                .setDescription(description)
                .setThumbnail(voiceChannel.getGuild().getIconUrl())
                .addField("Creation At", infoUtil.getCreationDate(voiceChannel), false)
                .addField("Misc", miscString, false)
                .setFooter("ID: " + voiceChannel.getId())
                .build();
    }

    private @NotNull MessageEmbed handleTextChannel(@NotNull TextChannel textChannel) {
        String isNsfw = textChannel.isNSFW() ? Constants.CHECK : Constants.CROSS;
        String isNews = textChannel.isNews() ? Constants.CHECK : Constants.CROSS;
        String isSynced = textChannel.isSynced() ? Constants.CHECK : Constants.CROSS;
        String topic = textChannel.getTopic() == null ? "No Topic Set" : textChannel.getTopic();
        String category = textChannel.getParent() == null ? "No Category" : textChannel.getParent().getName();
        String position = "#" + textChannel.getPosition();
        String miscString = """
                Nsfw: $isNsfw
                News: $isNews
                Synced: $isSynced
                """
                .replace("$isNsfw", isNsfw)
                .replace("$isNews", isNews)
                .replace("$isSynced", isSynced);
        String description = """
                $channelMention
                **Category:** $category
                **Position:** $position
                **Topic:** $topic
                """
                .replace("$channelMention", textChannel.getAsMention())
                .replace("$category", category)
                .replace("$position", position)
                .replace("$topic", topic);

        return embedService.getBaseEmbed()
                .setTitle("#" + textChannel.getName() + " Information")
                .setDescription(description)
                .setThumbnail(textChannel.getGuild().getIconUrl())
                .addField("Creation At", infoUtil.getCreationDate(textChannel), false)
                .addField("Misc", miscString, false)
                .setFooter("ID: " + textChannel.getId())
                .build();
    }
}
