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
public @interface SubCommandGroup {
    String parent();
    String name();
    String description();
}
