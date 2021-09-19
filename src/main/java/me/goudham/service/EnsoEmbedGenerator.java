package me.goudham.service;

import jakarta.inject.Singleton;
import java.awt.Color;
import java.time.Instant;
import java.util.Random;
import net.dv8tion.jda.api.EmbedBuilder;

@Singleton
public class EnsoEmbedGenerator implements EmbedGenerator {
    private final Random random = new Random();

    @Override
    public EmbedBuilder getBaseEmbed() {
        Color randomColor = new Color(random.nextFloat(), random.nextFloat(), random.nextFloat());

        return new EmbedBuilder()
                .setColor(randomColor)
                .setTimestamp(Instant.now())
                .setFooter("\uD835\uDCE4\uD835\uDD00\uD835\uDCE4");
    }
}
