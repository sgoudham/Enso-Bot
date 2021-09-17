package me.goudham.config;

import io.micronaut.context.annotation.Factory;
import io.micronaut.context.annotation.Value;
import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import javax.security.auth.login.LoginException;
import me.goudham.command.ICommand;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.utils.cache.CacheFlag;

@Factory
@Introspected
public class BotConfig {
    private final String token;

    @Inject
    public BotConfig(@Value(value = "${bot.token}") String token) {
        this.token = token;
    }

    @Singleton
    Map<String, List<ICommand>> commandsMap() {
        return Collections.emptyMap();
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
