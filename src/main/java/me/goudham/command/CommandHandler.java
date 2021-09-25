package me.goudham.command;

import net.dv8tion.jda.api.events.Event;

public interface CommandHandler {
    void handle(Event event);
}
