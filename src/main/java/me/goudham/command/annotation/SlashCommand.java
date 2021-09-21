package me.goudham.command.annotation;

import jakarta.inject.Qualifier;
import jakarta.inject.Singleton;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Singleton
@Qualifier
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface SlashCommand {
    String name();
    String description();
    boolean isVisible();
    String[] subCommandGroups() default {};
    String[] subCommands() default {};
    Option[] options() default {};
}
