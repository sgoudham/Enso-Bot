package me.goudham.command;

import io.micronaut.inject.BeanDefinition;
import java.util.List;
import java.util.Map;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;

public interface CommandLoader {
    List<CommandData> loadIntoMapAndReturnCommands(Map<String, BeanDefinition<?>> commandMap);
}
