package me.goudham.config;

import io.micronaut.context.annotation.Factory;
import io.micronaut.context.annotation.Value;
import io.micronaut.core.annotation.Introspected;
import io.micronaut.core.annotation.Order;
import io.micronaut.inject.ExecutableMethod;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.security.auth.login.LoginException;
import me.goudham.command.CommandHandler;
import me.goudham.domain.Pair;
import me.goudham.listener.OnReadyListener;
import me.goudham.listener.SlashCommandListener;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.entities.Activity;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.requests.GatewayIntent;
import net.dv8tion.jda.api.utils.MemberCachePolicy;
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
    public Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap() {
        return new HashMap<>();
    }

    @Singleton
    @Order(1)
    public JDA jda(CommandHandler commandHandler) throws LoginException, InterruptedException {
        return JDABuilder
                .createDefault(token)
                .setActivity(Activity.playing("With Hamothy"))
                .setMemberCachePolicy(MemberCachePolicy.ALL)
                .addEventListeners(
                        new OnReadyListener(),
                        new SlashCommandListener(commandHandler)
                )
                .enableIntents(
                        List.of(
                                GatewayIntent.GUILD_MESSAGE_REACTIONS,
                                GatewayIntent.GUILD_VOICE_STATES,
                                GatewayIntent.GUILD_PRESENCES,
                                GatewayIntent.GUILD_MESSAGES,
                                GatewayIntent.GUILD_MEMBERS,
                                GatewayIntent.GUILD_EMOJIS
                        )
                )
                .enableCache(
                        CacheFlag.MEMBER_OVERRIDES,
                        CacheFlag.ONLINE_STATUS,
                        CacheFlag.VOICE_STATE,
                        CacheFlag.ROLE_TAGS,
                        CacheFlag.ACTIVITY,
                        CacheFlag.EMOTE
                )
                .build()
                .awaitReady();
    }

    @Singleton
    @Order(2)
    public Guild ownerGuild(JDA jda) {
        Guild ownerGuild = jda.getGuildById(guildId);
        if (ownerGuild == null) {
            throw new RuntimeException("Owner Guild Not Found");
        }
        return ownerGuild;
    }
}
