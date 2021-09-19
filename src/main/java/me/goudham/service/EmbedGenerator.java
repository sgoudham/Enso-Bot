package me.goudham.service;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Member;

public interface EmbedGenerator {
    EmbedBuilder getBaseEmbed();
    EmbedBuilder getUserEmbed(Member member);
}
