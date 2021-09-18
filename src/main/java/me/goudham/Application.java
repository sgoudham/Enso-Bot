package me.goudham;

import io.micronaut.context.ApplicationContext;
import me.goudham.bot.EnsoBot;

public class Application {
    public static void main(String[] args) throws InterruptedException {
        ApplicationContext applicationContext = ApplicationContext.run();
        EnsoBot ensoBot = applicationContext.getBean(EnsoBot.class);
        ensoBot.startup();

//        GuildsRepository bean = run.getBean(GuildsRepository.class);
//        bean.saveOnConflictDoNothing(new Guilds(1234L, "to", null, 1));
//        bean.saveOnConflictDoNothing(new Guilds(1234L));
//        bean.save(new Guilds(1234L));
//        System.out.println("poggers");

//        BeanDefinition<GuildsRepository> beanDefinition = run.getBeanDefinition(GuildsRepository.class);
//        ExecutableMethod<GuildsRepository, Object> find = beanDefinition.getRequiredMethod("findByPrefix", String.class);
//        Optional<String> string = find.getAnnotationMetadata().stringValue(Query.class);
//        System.out.println(string);
    }
}
