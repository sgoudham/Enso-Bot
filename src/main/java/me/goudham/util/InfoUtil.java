package me.goudham.util;

import java.awt.Color;
import java.util.List;
import net.dv8tion.jda.api.OnlineStatus;
import net.dv8tion.jda.api.entities.ChannelType;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Member;
import org.jetbrains.annotations.NotNull;

public interface InfoUtil {
    @NotNull String getColorAsHex(@NotNull Color color);
    Color getMemberColour(@NotNull Member member);
    @NotNull String getMemberBadges(@NotNull Member member);
    @NotNull String getMemberOnlineStatus(@NotNull Member member);
    @NotNull String getTopRole(@NotNull Object object);
    String getListOfMembers(@NotNull List<Member> members, int limit);
    String getGuildEmotes(@NotNull Guild guild, int limit);
    String getGuildRoles(@NotNull Guild guild, int limit);
    String getMemberRoles(@NotNull Member member, int limit);
    long getMemberStatusCount(@NotNull Guild guild, OnlineStatus onlineStatus);
    long getChannelCount(@NotNull Guild guild, ChannelType channelType);
    @NotNull String getJoinedDate(@NotNull Member member);
    @NotNull String getCreationDate(Object object);
}
