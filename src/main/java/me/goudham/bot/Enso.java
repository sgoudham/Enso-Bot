package me.goudham.bot;

import io.micronaut.context.BeanContext;
import io.micronaut.core.annotation.AnnotationValue;
import io.micronaut.inject.BeanDefinition;
import io.micronaut.inject.qualifiers.Qualifiers;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.lang.annotation.Annotation;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import me.goudham.command.annotation.Choice;
import me.goudham.command.annotation.Command;
import me.goudham.command.annotation.Option;
import net.dv8tion.jda.api.JDA;

@Singleton
public class Enso implements Bot {
    private final JDA bot;
    private final BeanContext beanContext;


    @Inject
    public Enso(JDA bot, BeanContext beanContext) {
        this.bot = bot;
        this.beanContext = beanContext;
    }

    @Override
    public void startup() {
        System.out.println("pog");
        Set<Class<?>> classes = collectConsumedAnnotatedClasses();
//        CommandListUpdateAction commands = bot.updateCommands();
//        CommandData commandData = new CommandData("", "");
//        SubcommandGroupData subcommandGroupData = new SubcommandGroupData();
//        SubcommandData subcommandData = new SubcommandData();
//        OptionData optionData = new OptionData(OptionType.BOOLEAN, "", "");
//        Guild guildById = bot.getGuildById(1234);
//        guildById.upsertCommand()
//        commands.addCommands(
//                commandData
//        );
    }

    private Set<Class<?>> collectConsumedAnnotatedClasses() {
        Set<Class<?>> classes = new HashSet<>();
        Collection<BeanDefinition<?>> definitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(Command.class));
        definitions.forEach(definition -> {
            AnnotationValue<Annotation> command = definition.getDeclaredAnnotation("me.goudham.command.annotation.Command");
            Optional<String> name = command.stringValue("name");

            if (command.contains("options")) {
                List<AnnotationValue<Option>> optionAnnotations = command.getAnnotations("options", Option.class);
                for (AnnotationValue<Option> optionAnnotationValue : optionAnnotations) {
                    // do option stuff
                    if (command.contains("choices")) {
                        List<AnnotationValue<Choice>> choiceAnnotations = optionAnnotationValue.getAnnotations("choices", Choice.class);
                        for (AnnotationValue<Choice> choiceAnnotationValue : choiceAnnotations) {
                            // do choice stuff
                        }
                    }
                }
            }
        });
        return classes;
    }

}
