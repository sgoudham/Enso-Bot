package me.goudham.command;

import io.micronaut.context.BeanContext;
import io.micronaut.core.annotation.AnnotationValue;
import io.micronaut.core.beans.BeanIntrospection;
import io.micronaut.core.beans.BeanIntrospector;
import io.micronaut.core.beans.BeanMethod;
import io.micronaut.inject.ExecutableMethod;
import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.OptionalInt;
import me.goudham.command.annotation.Choice;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.command.annotation.SubCommand;
import me.goudham.command.annotation.SubCommandGroup;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionType;
import net.dv8tion.jda.api.interactions.commands.build.CommandData;
import net.dv8tion.jda.api.interactions.commands.build.OptionData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandData;
import net.dv8tion.jda.api.interactions.commands.build.SubcommandGroupData;
import net.dv8tion.jda.internal.utils.tuple.ImmutablePair;
import net.dv8tion.jda.internal.utils.tuple.Pair;

@Singleton
public class SlashCommandLoader implements CommandLoader {
    private final Collection<BeanIntrospection<Object>> slashCommandIntrospections = BeanIntrospector.forClassLoader(ClassLoader.getSystemClassLoader()).findIntrospections(SlashCommand.class);
    private final Collection<BeanIntrospection<Object>> subCommandGroupIntrospections = BeanIntrospector.forClassLoader(ClassLoader.getSystemClassLoader()).findIntrospections(SubCommandGroup.class);
    private final Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap;
    private final BeanContext beanContext;

    @Inject
    public SlashCommandLoader(Map<String, Pair<Object, ExecutableMethod<Object, Object>>> commandMap, BeanContext beanContext) {
        this.commandMap = commandMap;
        this.beanContext = beanContext;
    }

    @Override
    public void populateCommandMap() {
        for (BeanIntrospection<Object> slashCommandIntrospection : slashCommandIntrospections) {
            AnnotationValue<SlashCommand> slashCommand = slashCommandIntrospection.getDeclaredAnnotation(SlashCommand.class);
            Collection<BeanMethod<Object, Object>> subCommands = slashCommandIntrospection.getBeanMethods();

            boolean noHandleMethod = subCommands.stream().noneMatch(method -> method.getName().equals("handle"));
            if (subCommands.size() > 1 && !noHandleMethod) {
                throw new RuntimeException("Cannot Have Multiple Methods Including Main 'handle' Method In -> " + slashCommandIntrospection);
            }

            if (slashCommand != null) {
                String name = slashCommand.stringValue("name").orElseThrow();
                String[] subCommandGroups = slashCommand.stringValues("subCommandGroups");

                if (subCommandGroups.length < 1 && !noHandleMethod) {
                    storeIntoCommandMap(slashCommandIntrospection, name, "handle");
                } else {
                    for (BeanMethod<Object, Object> subCommandMethod : subCommands) {
                        AnnotationValue<SubCommand> subCommand = subCommandMethod.getDeclaredAnnotation(SubCommand.class);
                        if (subCommand != null) {
                            String subCommandName = subCommand.stringValue("name").orElseThrow();
                            String subCommandPath = name + "/" + subCommandName;
                            storeIntoCommandMap(slashCommandIntrospection, subCommandPath, subCommandMethod.getName());
                        }
                    }
                }

            } else {
                throw new RuntimeException("Slash Command Annotation For " + slashCommandIntrospection + " Was Null");
            }
        }

        for (BeanIntrospection<Object> subCommandGroupIntrospection : subCommandGroupIntrospections) {
            AnnotationValue<SubCommandGroup> subCommandGroup = subCommandGroupIntrospection.getDeclaredAnnotation(SubCommandGroup.class);
            Collection<BeanMethod<Object, Object>> subCommands = subCommandGroupIntrospection.getBeanMethods();

            if (subCommandGroup != null) {
                String parent = subCommandGroup.stringValue("parent").orElseThrow();
                String name = subCommandGroup.stringValue("name").orElseThrow();

                for (BeanMethod<Object, Object> subCommandMethod : subCommands) {
                    AnnotationValue<SubCommand> subCommand = subCommandMethod.getDeclaredAnnotation(SubCommand.class);
                    if (subCommand != null) {
                        String subCommandName = subCommand.stringValue("name").orElseThrow();
                        String subCommandPath = parent + "/" + name + "/" + subCommandName;
                        storeIntoCommandMap(subCommandGroupIntrospection, subCommandPath, subCommandMethod.getName());
                    }
                }

            } else {
                throw new RuntimeException("SubCommandGroup Annotation For " + subCommandGroupIntrospection + " Was Null");
            }
        }
    }


    @Override
    public List<CommandData> registerSlashCommands() {
        Map<String, CommandData> commandDataMap = new HashMap<>();
        List<CommandData> commandDataList = new ArrayList<>();

        for (BeanIntrospection<Object> slashCommandIntrospection : slashCommandIntrospections) {
            AnnotationValue<SlashCommand> slashCommand = slashCommandIntrospection.getDeclaredAnnotation(SlashCommand.class);
            Collection<BeanMethod<Object, Object>> subCommands = slashCommandIntrospection.getBeanMethods();

            if (slashCommand != null) {
                String name = slashCommand.stringValue("name").orElseThrow();
                String description = slashCommand.stringValue("description").orElse("No Description");
                boolean isVisible = slashCommand.booleanValue("isVisible").orElse(true);
                String[] subCommandGroups = slashCommand.stringValues("subCommandGroups");

                CommandData commandData = new CommandData(name, description).setDefaultEnabled(isVisible);
                Arrays.stream(subCommandGroups)
                        .map(subCommandGroup -> name + "/" + subCommandGroup)
                        .forEach(subCommandGroupName -> commandDataMap.put(subCommandGroupName, commandData));

                boolean noHandleMethod = subCommands.stream().noneMatch(method -> method.getName().equals("handle"));
                if (subCommands.size() > 1 && !noHandleMethod) {
                    throw new RuntimeException("Cannot Have Multiple Methods Including Main 'handle' Method In -> " + slashCommandIntrospection);
                }

                if (subCommandGroups.length < 1 && !noHandleMethod) {
                    List<OptionData> optionData = loadOptions(slashCommand);
                    if (optionData != null) commandData.addOptions(optionData);
                    storeIntoCommandMap(slashCommandIntrospection, name, "handle");
                } else {
                    List<SubcommandData> subCommandList = new ArrayList<>();
                    for (BeanMethod<Object, Object> subCommandMethod : subCommands) {
                        AnnotationValue<SubCommand> subCommand = subCommandMethod.getDeclaredAnnotation(SubCommand.class);
                        if (subCommand != null) {
                            SubcommandData subcommandData = getSubCommandData(subCommand);
                            subCommandList.add(subcommandData);

                            String subCommandPath = name + "/" + subcommandData.getName();
                            storeIntoCommandMap(slashCommandIntrospection, subCommandPath, subCommandMethod.getName());
                        }
                    }
                    commandData.addSubcommands(subCommandList);
                }
                commandDataList.add(commandData);
            } else {
                throw new RuntimeException("Slash Command Annotation For " + slashCommandIntrospection + " Was Null");
            }
        }

        for (BeanIntrospection<Object> subCommandGroupIntrospection : subCommandGroupIntrospections) {
            AnnotationValue<SubCommandGroup> subCommandGroup = subCommandGroupIntrospection.getDeclaredAnnotation(SubCommandGroup.class);
            Collection<BeanMethod<Object, Object>> subCommands = subCommandGroupIntrospection.getBeanMethods();

            if (subCommandGroup != null) {
                String parent = subCommandGroup.stringValue("parent").orElseThrow();
                String name = subCommandGroup.stringValue("name").orElseThrow();
                String description = subCommandGroup.stringValue("description").orElseThrow();
                String commandPath = parent + "/" + name;

                CommandData commandData = commandDataMap.get(commandPath);
                SubcommandGroupData subcommandGroupData = new SubcommandGroupData(name, description);

                List<SubcommandData> subCommandList = new ArrayList<>();
                for (BeanMethod<Object, Object> subCommandMethod : subCommands) {
                    AnnotationValue<SubCommand> subCommand = subCommandMethod.getDeclaredAnnotation(SubCommand.class);
                    if (subCommand != null) {
                        SubcommandData subcommandData = getSubCommandData(subCommand);
                        subCommandList.add(subcommandData);

                        String subCommandPath = parent + "/" + name + "/" + subcommandData.getName();
                        storeIntoCommandMap(subCommandGroupIntrospection, subCommandPath, subCommandMethod.getName());
                    }
                }
                subcommandGroupData.addSubcommands(subCommandList);
                commandData.addSubcommandGroups(subcommandGroupData);
            } else {
                throw new RuntimeException("SubCommandGroup Annotation For " + subCommandGroupIntrospection + " Was Null");
            }
        }

        commandDataMap.clear();
        return commandDataList;
    }

    private SubcommandData getSubCommandData(AnnotationValue<SubCommand> subCommand) {
        String subCommandName = subCommand.stringValue("name").orElseThrow();
        String subCommandDescription = subCommand.stringValue("description").orElseThrow();
        List<OptionData> optionDataList = loadOptions(subCommand);

        SubcommandData subcommandData = new SubcommandData(subCommandName, subCommandDescription);
        if (optionDataList != null) subcommandData.addOptions(optionDataList);

        return subcommandData;
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

    private void storeIntoCommandMap(BeanIntrospection<Object> beanIntrospection, String commandPath, String methodName) {
        Class<Object> clazz = beanIntrospection.getBeanType();
        Object beanInstance = beanContext.getBean(clazz);

        ExecutableMethod<Object, Object> executableMethod = null;
        try {
            executableMethod = beanContext.getExecutableMethod(clazz, methodName, SlashCommandEvent.class);
        } catch (NoSuchMethodException nsme) {
            nsme.printStackTrace();
        }

        commandMap.put(commandPath, new ImmutablePair<>(beanInstance, executableMethod));
    }
}
