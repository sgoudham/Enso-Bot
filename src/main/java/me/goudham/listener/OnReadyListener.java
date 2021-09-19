package me.goudham.listener;

import jakarta.inject.Singleton;
import net.dv8tion.jda.api.events.ReadyEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Singleton
public class OnReadyListener extends ListenerAdapter {
    private static final Logger logger = LoggerFactory.getLogger(OnReadyListener.class);

    @Override
    public void onReady(@NotNull ReadyEvent event) {
        logger.info("\uD835\uDCE4\uD835\uDD00\uD835\uDCE4 Senpaii. Ready!");
    }
}
