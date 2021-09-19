package me.goudham.command.annotation;

import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Qualifier;
import jakarta.inject.Singleton;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Singleton
@Introspected
@Qualifier
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface SlashCommand {
    String name();
    String description();
    boolean isVisible();
    SubCommandGroup[] subCommandGroups() default {};
    SubCommand[] subCommands() default {};
    Option[] options() default {};
}
