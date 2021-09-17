package me.goudham.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "guilds", schema = "public")
public class Guilds {
    @Id
    @Column(name = "guild_id", unique = true, nullable = false)
    private Long guildId;

    @Column(length = 5, nullable = false)
    private String prefix = ".";

    @Column(name = "modlogs")
    private Long modlogs;

    @Column(name = "roles_persist")
    private Integer rolePersist = 0;

    public Guilds() {

    }

    public Guilds(Long guildId) {
        this.guildId = guildId;
    }

    public Guilds(Long guildId, String prefix) {
        this.guildId = guildId;
        this.prefix = prefix;
    }

    public Guilds(Long guildId, String prefix, Long modlogs, Integer rolePersist) {
        this.guildId = guildId;
        this.prefix = prefix;
        this.modlogs = modlogs;
        this.rolePersist = rolePersist;
    }

    public Long getGuildId() {
        return guildId;
    }

    public void setGuildId(Long guildId) {
        this.guildId = guildId;
    }

    public String getPrefix() {
        return prefix;
    }

    public void setPrefix(String prefix) {
        this.prefix = prefix;
    }

    public Long getModlogs() {
        return modlogs;
    }

    public void setModlogs(Long modlogs) {
        this.modlogs = modlogs;
    }

    public Integer getRolePersist() {
        return rolePersist;
    }

    public void setRolePersist(Integer rolePersist) {
        this.rolePersist = rolePersist;
    }
}
