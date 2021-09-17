package me.goudham.command;

import io.micronaut.context.BeanContext;
import io.micronaut.core.annotation.AnnotationValue;
import io.micronaut.inject.BeanDefinition;
import io.micronaut.inject.qualifiers.Qualifiers;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.lang.annotation.Annotation;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import me.goudham.command.annotation.Command;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.requests.restaction.CommandListUpdateAction;

@Singleton
public class CommandManager {
    private final Map<String, ICommand> commandList;
    private final BeanContext beanContext;
    private final JDA bot;

    @Inject
    public CommandManager(BeanContext beanContext, JDA jda) {
        this.beanContext = beanContext;
        this.bot = jda;
        this.commandList = new HashMap<>();
    }

    void registerSlashCommands() {
        CommandListUpdateAction commands = bot.getGuildById("").updateCommands();
        List<CommandData> commandDataList = new ArrayList<>();

        Collection<BeanDefinition<?>> definitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(Command.class));
        for (BeanDefinition<?> definition : definitions) {
            AnnotationValue<Annotation> command = definition.getDeclaredAnnotation("me.goudham.command.annotation.Command");

            String commandName = command.stringValue("name").get();
            String commandDescription = command.stringValue("description").get();
            boolean isVisible = command.booleanValue("isVisible").get();



            CommandData commandData = new CommandData(commandName, commandDescription);
            commandData.setDefaultEnabled(isVisible);
//            commandData.

//            commandDataList.add(new CommandData(commandName, ))
        }

        commands.addCommands();
    }
}
