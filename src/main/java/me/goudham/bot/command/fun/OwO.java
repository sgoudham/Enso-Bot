package me.goudham.bot.command.fun;

import io.micronaut.context.annotation.Executable;
import java.util.List;
import java.util.Random;
import me.goudham.command.annotation.Option;
import me.goudham.command.annotation.SlashCommand;
import me.goudham.domain.Pair;
import net.dv8tion.jda.api.events.interaction.SlashCommandEvent;
import net.dv8tion.jda.api.interactions.commands.OptionMapping;
import net.dv8tion.jda.api.interactions.commands.OptionType;

@SlashCommand(
        name = "owo",
        description = "OwO'ify the given text",
        options = {
                @Option(
                        optionType = OptionType.STRING,
                        name = "text",
                        description = "The text to OwO'ify",
                        isRequired = true
                )
        }
)
public class OwO {
    private final Random random = new Random();
    private final List<Pair<String, String>> prefixAndSuffixList;

    public OwO() {
        this.prefixAndSuffixList = List.of(
                new Pair<>("H-hewwo?? ", " :D"),
                new Pair<>("Huohhhh. ", " >_<"),
                new Pair<>("Huohhhh. ", " >_>"),
                new Pair<>("UwU ", " ʕ•̫͡•ʔ"),
                new Pair<>("UwU ", " ;-;"),
                new Pair<>("OwO ", " :P"),
                new Pair<>("OwO ", " (；ω；)"),
                new Pair<>("OWO ", " x3"),
                new Pair<>("Haiiii! ", " ÙωÙ"),
                new Pair<>("HIII! ", " （＾ｖ＾）")
        );
    }

    @Executable
    public void handle(SlashCommandEvent slashCommandEvent) {
        OptionMapping optionMapping = slashCommandEvent.getOption("text");
        String givenText = optionMapping == null ? "" : optionMapping.getAsString();

        String replace = givenText
                .replace("L", "W")
                .replace("R", "W")
                .replace("l", "w")
                .replace("r", "w");

        StringBuilder outputText = new StringBuilder(replace);
        for (int i = 0; i < replace.length(); i++) {
            Character previousCharacter = replace.charAt(i == 0 ? i : i - 1);
            Character character = replace.charAt(i);

            if (character.equals('O') || character.equals('o')) {
                if (previousCharacter.equals('N') || previousCharacter.equals('n') || previousCharacter.equals('M') || previousCharacter.equals('m')) {
                    outputText.insert(i, "yo");
                }
            }
        }

        Pair<String, String> randomPrefixAndSuffix = getRandomPrefixAndSuffix();
        outputText.insert(0, randomPrefixAndSuffix.left());
        outputText.append(randomPrefixAndSuffix.right());

        slashCommandEvent.reply(outputText.toString()).queue();
    }

    private Pair<String, String> getRandomPrefixAndSuffix() {
        return prefixAndSuffixList.get(random.nextInt(prefixAndSuffixList.size()));
    }
}
