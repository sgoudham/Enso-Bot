package me.goudham.command.annotation;

import jakarta.inject.Qualifier;
import jakarta.inject.Singleton;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Singleton
@Qualifier
@Retention(RetentionPolicy.RUNTIME)
public @interface SubCommand {
    String commandParent() default "";
    String name();
    String description();
    Option[] options() default {};
}
