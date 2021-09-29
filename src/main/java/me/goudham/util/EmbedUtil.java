package me.goudham.util;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Member;

public interface EmbedUtil {
    EmbedBuilder getBaseEmbed();
    EmbedBuilder getUserEmbed(Member member);
}
