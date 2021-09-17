package me.goudham.command;

import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Singleton;
import me.goudham.command.annotation.Command;

@Singleton
@Introspected
@Command(name = "ping", description = "", isVisible = true)
public class Ping implements ICommand {

    @Override
    public void handle() {

    }
}