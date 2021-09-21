package me.goudham.command;

import io.micronaut.context.ApplicationContext;
import io.micronaut.context.BeanContext;
import io.micronaut.core.annotation.AnnotationValue;
import io.micronaut.inject.BeanDefinition;
import io.micronaut.inject.qualifiers.Qualifiers;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.OptionalInt;
import java.util.stream.Collectors;
import me.goudham.command.annotation.Choice;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.command.annotation.SubCommandGroup;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.Command;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandGroupData;
import net.dv8tion.jda.internal.utils.tuple.ImmutablePair;
import net.dv8tion.jda.internal.utils.tuple.Pair;

@Singleton
public class SlashCommandLoader implements CommandLoader {
    private final BeanContext beanContext;
    private final ApplicationContext applicationContext;

    @Inject
    public SlashCommandLoader(BeanContext beanContext, ApplicationContext applicationContext) {
        this.beanContext = beanContext;
        this.applicationContext = applicationContext;

    }

    @Override
    public List<CommandData> loadIntoMapAndReturnCommands(Map<String, Pair<Object, Method>> commandMap) {
        Collection<BeanDefinition<?>> slashCommandDefinitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(SlashCommand.class));
        Collection<BeanDefinition<?>> subCommandGroupDefinitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(SubCommandGroup.class));
        Collection<BeanDefinition<?>> subCommandDefinitions = beanContext.getBeanDefinitions(Qualifiers.byStereotype(SubCommand.class));
        Map<String, CommandData> commandDataMap = new HashMap<>();
        List<CommandData> commandDataList = new ArrayList<>();

        for (BeanDefinition<?> slashCommandDefinition : slashCommandDefinitions) {
            AnnotationValue<SlashCommand> slashCommand = slashCommandDefinition.getDeclaredAnnotation(SlashCommand.class);
            if (slashCommand != null) {
                String name = slashCommand.stringValue("name").orElseThrow();
                String description = slashCommand.stringValue("description").orElseThrow();
                boolean isVisible = slashCommand.booleanValue("isVisible").orElseThrow();
                String[] subCommandGroups = slashCommand.stringValues("subCommandGroups");
                String[] subCommands = slashCommand.stringValues("subCommands");

                CommandData commandData = new CommandData(name, description);
                commandData.setDefaultEnabled(isVisible);

                if (subCommandGroups.length == 0 && subCommands.length == 0) {
                    List<OptionData> optionData = loadOptions(slashCommand);
                    if (optionData != null) commandData.addOptions(optionData);

                    storeIntoCommandMap(commandMap, slashCommandDefinition, name, "handle");
                    commandDataMap.put(name, commandData);
                } else {
                    Arrays.stream(subCommandGroups)
                            .map(subCommandGroup -> name + "/" + subCommandGroup)
                            .forEach(subCommandGroupName -> commandDataMap.put(subCommandGroupName, commandData));
                    Arrays.stream(subCommands)
                            .map(subCommand -> name + "/" + subCommand)
                            .forEach(subCommandName -> commandDataMap.put(subCommandName, commandData));
                }

                commandDataList.add(commandData);
            } else {
                throw new RuntimeException("Slash Command Annotation For " + slashCommandDefinition + " Was Null");
            }
        }

        for (BeanDefinition<?> subCommandGroupDefinition : subCommandGroupDefinitions) {
            AnnotationValue<SubCommandGroup> subCommandGroup = subCommandGroupDefinition.getDeclaredAnnotation(SubCommandGroup.class);
            if (subCommandGroup != null) {
                String parent = subCommandGroup.stringValue("parent").orElseThrow();
                String name = subCommandGroup.stringValue("name").orElseThrow();
                String description = subCommandGroup.stringValue("description").orElseThrow();
                String commandPath = parent + "/" + name;

                CommandData commandData = commandDataMap.get(commandPath);
                SubcommandGroupData subcommandGroupData = new SubcommandGroupData(name, description);

                Class<?> beanType = subCommandGroupDefinition.getBeanType();
                List<SubcommandData> subCommandList = new ArrayList<>();
                List<Method> subCommands = Arrays.stream(beanType.getDeclaredMethods())
                        .filter(method -> method.isAnnotationPresent(SubCommand.class))
                        .collect(Collectors.toList());

                for (Method subCommand : subCommands) {
                    SubCommand annotation = subCommand.getDeclaredAnnotation(SubCommand.class);
                    String subCommandName = annotation.name();
                    String subCommandDescription = annotation.description();
                    List<OptionData> optionDataList = Arrays.stream(annotation.options())
                            .map(option -> {
                                OptionData optionData = new OptionData(option.optionType(), option.name(), option.description(), option.isRequired());
                                List<Command.Choice> choiceDataList = Arrays.stream(option.choices())
                                        .map(choice -> {
                                            int intValue = (int) choice.intValue();
                                            double doubleValue = choice.doubleValue();
                                            String stringValue = choice.stringValue();

                                            Command.Choice choiceData = null;
                                            if (intValue != 0) {
                                                choiceData = new Command.Choice(name, intValue);
                                            } else if (!Double.isNaN(doubleValue)) {
                                                choiceData = new Command.Choice(name, doubleValue);
                                            } else if (!stringValue.isBlank()) {
                                                choiceData = new Command.Choice(name, stringValue);
                                            }

                                            return choiceData;
                                        }).collect(Collectors.toList());
                                return optionData.addChoices(choiceDataList);
                            }).collect(Collectors.toList());

                    SubcommandData subcommandData = new SubcommandData(subCommandName, subCommandDescription);
                    subcommandData.addOptions(optionDataList);
                    subCommandList.add(subcommandData);

                    String subCommandPath = parent + "/" + name + "/" + subCommandName;
                    storeIntoCommandMap(commandMap, subCommandGroupDefinition, subCommandPath, subCommandName);
                    commandDataMap.put(subCommandPath, commandData);
                }

                subcommandGroupData.addSubcommands(subCommandList);
                commandData.addSubcommandGroups(subcommandGroupData);
            } else {
                throw new RuntimeException("Sub Command Annotation For " + subCommandGroupDefinition + " Was Null");
            }
        }

        for (BeanDefinition<?> subCommandDefinition : subCommandDefinitions) {
            AnnotationValue<SubCommand> subCommand = subCommandDefinition.getDeclaredAnnotation(SubCommand.class);
            if (subCommand != null) {
                String commandParent = subCommand.stringValue("commandParent").orElseThrow();
                String name = subCommand.stringValue("name").orElseThrow();
                String description = subCommand.stringValue("description").orElseThrow();
                String commandPath = commandParent + "/" + name;

                CommandData commandData = commandDataMap.get(commandPath);
                SubcommandData subcommandData = new SubcommandData(name, description);
                List<OptionData> optionData = loadOptions(subCommand);
                if (optionData != null) subcommandData.addOptions(optionData);

                storeIntoCommandMap(commandMap, subCommandDefinition, commandPath, "handle");
                commandData.addSubcommands(subcommandData);
            } else {
                throw new RuntimeException("Sub Command Annotation For " + subCommandDefinition + " Was Null");
            }
        }
        return commandDataList;
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

    private void storeIntoCommandMap(Map<String, Pair<Object, Method>> commandMap, BeanDefinition<?> beanDefinition, String commandPath, String methodName) {
        Class<?> clazz = beanDefinition.getBeanType();
        Object bean = applicationContext.getBean(clazz);

        Method method = null;
        try {
            method = clazz.getMethod(methodName, SlashCommandEvent.class);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        }

        commandMap.put(commandPath, new ImmutablePair<>(bean, method));
    }
}
