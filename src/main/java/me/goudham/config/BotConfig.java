package me.goudham.config;

import io.micronaut.context.annotation.Factory;
import io.micronaut.context.annotation.Value;
import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.List;
import javax.security.auth.login.LoginException;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.utils.cache.CacheFlag;

@Factory
@Introspected
public class BotConfig {
    private final String token;
    private final String guildId;

    @Inject
    public BotConfig(@Value("${bot.token}") String token,
                     @Value("${bot.guild.id}") String guildId) {
        this.token = token;
        this.guildId = guildId;
    }

    @Singleton
    public Guild guild(JDA jda) {
        Guild ownerGuild = jda.getGuildById(guildId);
        if (ownerGuild == null) {
            throw new RuntimeException("Owner Guild Not Found");
        }
        return ownerGuild;
    }

    @Singleton
    public JDA jda() throws LoginException, InterruptedException {
        return JDABuilder
                .createDefault(token)
                .setActivity(Activity.playing("With Hamothy"))
                .addEventListeners()
                .enableIntents(
                        List.of(
                                GatewayIntent.GUILD_MEMBERS,
                                GatewayIntent.GUILD_PRESENCES,
                                GatewayIntent.GUILD_MESSAGES,
                                GatewayIntent.GUILD_VOICE_STATES,
                                GatewayIntent.GUILD_EMOJIS,
                                GatewayIntent.GUILD_MESSAGE_REACTIONS
                        )
                ).enableCache(CacheFlag.VOICE_STATE)
                .build()
                .awaitReady();
    }
}
