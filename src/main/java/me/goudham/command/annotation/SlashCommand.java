package me.goudham.command.annotation;

import io.micronaut.core.annotation.Introspected;
import jakarta.inject.Qualifier;
import jakarta.inject.Singleton;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Qualifier
@Singleton
@Introspected
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface SlashCommand {
    String name();
    String description();
    boolean isVisible() default true;
    String[] subCommandGroups() default {};
    Option[] options() default {};
}
