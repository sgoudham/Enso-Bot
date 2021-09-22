package me.goudham.service;

import jakarta.inject.Singleton;
import java.awt.Color;
import java.time.Instant;
import java.util.Random;
import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.Member;

@Singleton
public class EnsoEmbedService implements EmbedService {
    private final Random random = new Random();

    @Override
    public EmbedBuilder getBaseEmbed() {
        return new EmbedBuilder()
                .setColor(getRandomColour())
                .setTimestamp(Instant.now())
                .setFooter("\uD835\uDCE4\uD835\uDD00\uD835\uDCE4");
    }

    @Override
    public EmbedBuilder getUserEmbed(Member member) {
       Color userColour = member.getColor() == null ? getRandomColour() : member.getColor();
       return getBaseEmbed().setColor(userColour);
    }

    private Color getRandomColour() {
        return new Color(random.nextFloat(), random.nextFloat(), random.nextFloat());
    }
}
