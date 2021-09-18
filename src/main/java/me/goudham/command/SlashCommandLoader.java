package me.goudham.command;

import io.micronaut.context.BeanContext;
import io.micronaut.core.annotation.AnnotationValue;
import io.micronaut.core.annotation.Introspected;
import io.micronaut.inject.BeanDefinition;
import io.micronaut.inject.qualifiers.Qualifiers;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.lang.annotation.Annotation;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.OptionalInt;
import me.goudham.command.annotation.Choice;
import me.goudham.command.annotation.Command;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SubCommand;
import me.goudham.command.annotation.SubCommandGroup;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandGroupData;

@Singleton
@Introspected
public class SlashCommandLoader implements CommandLoader {
    private final BeanContext beanContext;

    @Inject
    public SlashCommandLoader(BeanContext beanContext) {
        this.beanContext = beanContext;
    }

    @Override
    public List<CommandData> loadIntoMapAndReturnCommands(Map<String, BeanDefinition<?>> commandMap) {
        Collection<BeanDefinition<?>> beanDefinitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(Command.class));
        List<CommandData> commandDataList = new ArrayList<>();

        for (BeanDefinition<?> beanDefinition : beanDefinitions) {
            AnnotationValue<Annotation> slashCommand = beanDefinition.getDeclaredAnnotation("me.goudham.command.annotation.Command");
            if (slashCommand != null) {
                String name = slashCommand.stringValue("name").orElseThrow();
                String description = slashCommand.stringValue("description").orElseThrow();
                boolean isVisible = slashCommand.booleanValue("isVisible").orElseThrow();

                CommandData commandData = new CommandData(name, description);
                commandData.setDefaultEnabled(isVisible);

                List<SubcommandGroupData> subcommandGroupDataList = loadSubCommandGroups(slashCommand);
                List<SubcommandData> subcommandData = loadSubCommands(slashCommand);
                List<OptionData> optionData = loadOptions(slashCommand);

                if (subcommandGroupDataList != null) commandData.addSubcommandGroups(subcommandGroupDataList);
                if (subcommandData != null) commandData.addSubcommands(subcommandData);
                if (optionData != null) commandData.addOptions(optionData);

                commandDataList.add(commandData);
                commandMap.put(name, beanDefinition);
            } else {
                throw new RuntimeException();
            }
        }

         return commandDataList;
    }

    private List<SubcommandGroupData> loadSubCommandGroups(AnnotationValue<?> slashCommand) {
        if (slashCommand.contains("subCommandGroups")) {
            List<SubcommandGroupData> subcommandGroupDataList = new ArrayList<>();
            List<AnnotationValue<SubCommandGroup>> subCommandGroupAnnotations = slashCommand.getAnnotations("subCommandGroups", SubCommandGroup.class);
            for (AnnotationValue<SubCommandGroup> subCommandGroup : subCommandGroupAnnotations) {
                String name = subCommandGroup.stringValue("name").orElseThrow();
                String description = subCommandGroup.stringValue("description").orElseThrow();

                SubcommandGroupData subcommandGroupData = new SubcommandGroupData(name, description);
                List<SubcommandData> subcommandData = loadSubCommands(subCommandGroup);
                if (subcommandData != null) subcommandGroupData.addSubcommands(subcommandData);

                subcommandGroupDataList.add(subcommandGroupData);
            }

            return subcommandGroupDataList;
        }

        return null;
    }

    private List<SubcommandData> loadSubCommands(AnnotationValue<?> slashCommand) {
        if (slashCommand.contains("subCommands")) {
            List<SubcommandData> subcommandDataList = new ArrayList<>();
            List<AnnotationValue<SubCommand>> subCommandAnnotations = slashCommand.getAnnotations("subCommands", SubCommand.class);

            for (AnnotationValue<SubCommand> subCommand : subCommandAnnotations) {
                String name = subCommand.stringValue("name").orElseThrow();
                String description = subCommand.stringValue("description").orElseThrow();

                SubcommandData subCommandData = new SubcommandData(name, description);
                List<OptionData> optionData = loadOptions(subCommand);
                if (optionData != null) subCommandData.addOptions(optionData);


                subcommandDataList.add(subCommandData);
            }

            return subcommandDataList;
        }

        return null;
    }

    private List<OptionData> loadOptions(AnnotationValue<?> slashCommand) {
        if (slashCommand.contains("options")) {
            List<OptionData> optionList = new ArrayList<>();
            List<AnnotationValue<Option>> optionAnnotations = slashCommand.getAnnotations("options", Option.class);

            for (AnnotationValue<Option> option : optionAnnotations) {
                OptionType optionType = option.enumValue("optionType", OptionType.class).orElseThrow();
                String name = option.stringValue("name").orElseThrow();
                String description = option.stringValue("description").orElseThrow();
                boolean isRequired = option.booleanValue("isRequired").orElseThrow();

                OptionData optionData = new OptionData(optionType, name, description, isRequired);
                List<net.dv8tion.jda.api.interactions.commands.Command.Choice> choiceList = loadChoices(option);
                if (choiceList != null) optionData.addChoices(choiceList);

               optionList.add(optionData);
            }

            return optionList;
        }

        return null;
    }

    private List<net.dv8tion.jda.api.interactions.commands.Command.Choice> loadChoices(AnnotationValue<?> slashCommand) {
        if (slashCommand.contains("choices")) {
            List<net.dv8tion.jda.api.interactions.commands.Command.Choice> choiceList = new ArrayList<>();
            List<AnnotationValue<Choice>> choiceAnnotations = slashCommand.getAnnotations("choices", Choice.class);

            for (AnnotationValue<Choice> choice : choiceAnnotations) {
                net.dv8tion.jda.api.interactions.commands.Command.Choice choiceData = null;
                String name = choice.stringValue("name").orElseThrow();

                OptionalInt optionalInt = choice.intValue("intValue");
                int intValue = 0;
                if (optionalInt.isPresent()) {
                    intValue = optionalInt.getAsInt();
                }

                OptionalDouble optionalDouble = choice.doubleValue("doubleValue");
                double doubleValue = Double.NaN;
                if (optionalDouble.isPresent()) {
                    doubleValue = optionalDouble.getAsDouble();
                }

                Optional<String> optionalString = choice.stringValue("stringValue");
                String stringValue = "";
                if (optionalString.isPresent()) {
                    stringValue = optionalString.get();
                }

                if (intValue != 0) {
                   choiceData = new net.dv8tion.jda.api.interactions.commands.Command.Choice(name, intValue);
                } else if (!Double.isNaN(doubleValue)) {
                    choiceData = new net.dv8tion.jda.api.interactions.commands.Command.Choice(name, doubleValue);
                } else if (!stringValue.isBlank()) {
                    choiceData = new net.dv8tion.jda.api.interactions.commands.Command.Choice(name, stringValue);
                }

                choiceList.add(choiceData);
            }

            return choiceList;
        }

        return null;
    }
}
