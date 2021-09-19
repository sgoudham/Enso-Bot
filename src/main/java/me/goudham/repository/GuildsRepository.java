package me.goudham.repository;

import io.micronaut.core.annotation.NonNull;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.repository.CrudRepository;
import java.util.Optional;
import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import me.goudham.entity.Guilds;

@Repository
public abstract class GuildsRepository implements CrudRepository<Guilds, Long> {
    private final EntityManager entityManager;

    public GuildsRepository(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Transactional
    public <T extends Guilds> T saveOnConflictDoNothing(@Valid @NotNull @NonNull T entity) {
        Optional<Guilds> optionalGuilds = findById(entity.getGuildId());
        optionalGuilds.ifPresentOrElse(
                guilds -> {},
                () -> entityManager.persist(entity)
        );

        return entity;
    }
}
