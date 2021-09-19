package me.goudham.service;

import net.dv8tion.jda.api.EmbedBuilder;

public interface EmbedGenerator {
    EmbedBuilder getBaseEmbed();
}
