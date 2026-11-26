-- Insert order: matches -> teams/subteams -> participants.
-- Arena subteams must exist before participants are inserted.

USE lolmatrixdb;

-- summoners

CREATE TABLE IF NOT EXISTS summoners (

    puuid               VARCHAR(78)  NOT NULL,
    summoner_name       VARCHAR(16)  NOT NULL,
    tag_line            VARCHAR(5)   NOT NULL,
    region              VARCHAR(16)  NOT NULL,
    profile_icon_id     INT          NOT NULL,
    summoner_level      INT          NOT NULL,
    revision_date       BIGINT       NOT NULL,
    last_updated        DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (puuid, region),
    INDEX idx_summoner_region (region)

);

-- matches

CREATE TABLE IF NOT EXISTS matches (

    match_id              VARCHAR(20) NOT NULL, -- "server_id"
    platform_id           VARCHAR(8)  NOT NULL, -- "server"
    game_id               BIGINT      NOT NULL, -- "id"
    end_of_game_result    VARCHAR(32) NULL,
    data_version          VARCHAR(8)  NOT NULL, 
    game_creation         BIGINT      NOT NULL,
    game_duration         INT         NOT NULL,
    game_end_timestamp    BIGINT      NOT NULL,
    game_start_timestamp  BIGINT      NOT NULL,
    map_id                INT         NOT NULL,
    queue_id              INT         NOT NULL,
    game_mode             VARCHAR(20) NOT NULL,
    game_type             VARCHAR(20) NOT NULL,
    game_version          VARCHAR(32) NOT NULL,
    patch                 VARCHAR(5)  NOT NULL,

    PRIMARY KEY (match_id),
    UNIQUE KEY uq_matches_platform_game (platform_id, game_id)

);

CREATE TABLE IF NOT EXISTS teams (

    match_id            VARCHAR(20) NOT NULL,
    team_id             SMALLINT    NOT NULL,
    win                 BOOLEAN     NOT NULL,
    bans                JSON        NULL,

    champion_kills       SMALLINT     NOT NULL,
    first_blood          BOOLEAN      NOT NULL,
    baron_kills          TINYINT      NOT NULL,
    baron_first          BOOLEAN      NOT NULL,
    dragon_kills         TINYINT      NOT NULL,
    dragon_first         BOOLEAN      NOT NULL,
    inhibitor_kills      TINYINT      NOT NULL,
    inhibitor_first      BOOLEAN      NOT NULL,
    rift_herald_kills    TINYINT      NOT NULL,
    rift_herald_first    BOOLEAN      NOT NULL,
    tower_kills          TINYINT      NOT NULL,
    tower_first          BOOLEAN      NOT NULL,

    PRIMARY KEY (match_id, team_id),
    CONSTRAINT fk_match_id
        FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE

);

-- Arena's six placement groups; separate from conventional teams.
CREATE TABLE IF NOT EXISTS subteams (
    match_id            VARCHAR(20) NOT NULL,
    subteam_id          SMALLINT    NOT NULL,
    placement           TINYINT     NOT NULL,

    PRIMARY KEY (match_id, subteam_id),
    UNIQUE KEY uq_subteams_placement (match_id, placement),
    CONSTRAINT fk_subteams_match
        FOREIGN KEY (match_id) REFERENCES matches (match_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS participants (

    match_id                           VARCHAR(20)  NOT NULL,
    participant_id                     TINYINT      NOT NULL,
    team_id                            SMALLINT     NOT NULL,
    puuid                              VARCHAR(78)  NOT NULL,
    riot_id_game_name                  VARCHAR(32)  NULL,    
    riot_id_tagline                    VARCHAR(16)  NULL,    
    summoner_level                     INT          NOT NULL,
    win                                BOOLEAN      NOT NULL,
    champion_id                        INT          NOT NULL,
    champion_name                      VARCHAR(32)  NOT NULL,
    champion_level                     TINYINT      NOT NULL,
    champion_experience                INT          NOT NULL,
    team_position                      VARCHAR(16) NULL,
    individual_position                VARCHAR(16) NULL,
    lane                               VARCHAR(16) NULL,
    player_role                        VARCHAR(16) NULL,
    kills                              SMALLINT     NOT NULL,
    deaths                             SMALLINT     NOT NULL,
    assists                            SMALLINT     NOT NULL,
    total_minions_killed               SMALLINT     NOT NULL,
    neutral_minions_killed             SMALLINT     NOT NULL,
    total_ally_jungle_minions_killed   SMALLINT     NOT NULL,
    total_enemy_jungle_minions_killed  SMALLINT     NOT NULL,
    killing_sprees                     SMALLINT     NOT NULL,
    largest_killing_spree              SMALLINT     NOT NULL,
    largest_multi_kill                 TINYINT      NOT NULL,
    largest_crit_strike                INT          NOT NULL,
    double_kills                       TINYINT      NOT NULL,
    triple_kills                       TINYINT      NOT NULL,
    quadra_kills                       TINYINT      NOT NULL,
    penta_kills                        TINYINT      NOT NULL,
    unreal_kills                       TINYINT      NOT NULL,
    longest_time_spent_living          INT          NOT NULL,
    total_time_spent_dead              INT          NOT NULL,
    time_played                        INT          NOT NULL,
    gold_earned                        INT          NOT NULL,
    gold_spent                         INT          NOT NULL,
    item0                              INT          NOT NULL,
    item1                              INT          NOT NULL,
    item2                              INT          NOT NULL,
    item3                              INT          NOT NULL,
    item4                              INT          NOT NULL,
    item5                              INT          NOT NULL,
    item6                              INT          NOT NULL,
    items_purchased                    SMALLINT     NOT NULL,
    total_dmg_dealt                    INT          NOT NULL,
    magic_dmg_dealt                    INT          NOT NULL,
    phy_dmg_dealt                      INT          NOT NULL,
    true_dmg_dealt                     INT          NOT NULL,
    total_dmg_dealt_champions          INT          NOT NULL,
    magic_dmg_dealt_champions          INT          NOT NULL,
    phy_dmg_dealt_champions            INT          NOT NULL,
    true_dmg_dealt_champions           INT          NOT NULL,
    total_dmg_taken                    INT          NOT NULL,
    magic_dmg_taken                    INT          NOT NULL,
    phy_dmg_taken                      INT          NOT NULL,
    true_dmg_taken                     INT          NOT NULL,
    self_mitigated_dmg                 INT          NOT NULL,
    total_heal                         INT          NOT NULL,
    total_heals_on_teammates           INT          NOT NULL,
    total_dmg_shielded_on_teammates    INT          NOT NULL,
    time_cc_others                     INT          NOT NULL,
    total_time_cc_dealt                INT          NOT NULL,
    dmg_dealt_to_buildings             INT          NOT NULL,
    dmg_dealt_to_epic_monsters         INT          NOT NULL,
    dmg_dealt_to_objectives            INT          NOT NULL,
    dmg_dealt_to_turrets               INT          NOT NULL,
    baron_kills                        TINYINT      NOT NULL,
    dragon_kills                       TINYINT      NOT NULL,
    turret_kills                       SMALLINT     NOT NULL,
    turret_takedowns                   SMALLINT     NOT NULL,
    turrets_lost                       SMALLINT     NOT NULL,
    inhibitor_kills                    TINYINT      NOT NULL,
    inhibitor_takedowns                TINYINT      NOT NULL,
    inhibitors_lost                    TINYINT      NOT NULL,
    nexus_kills                        TINYINT      NOT NULL,
    nexus_lost                         TINYINT      NOT NULL,
    nexus_takedowns                    TINYINT      NOT NULL,
    objectives_stolen                  TINYINT      NOT NULL,
    objectives_stolen_assists          TINYINT      NOT NULL,
    first_blood_kill                   BOOLEAN      NOT NULL,
    first_blood_assist                 BOOLEAN      NOT NULL,
    first_tower_kill                   BOOLEAN      NOT NULL,
    first_tower_assist                 BOOLEAN      NOT NULL,
    vision_score                       SMALLINT     NOT NULL,
    wards_placed                       SMALLINT     NOT NULL,
    wards_killed                       SMALLINT     NOT NULL,
    detector_wards_placed              SMALLINT     NOT NULL,
    sight_wards_bought                 SMALLINT     NOT NULL,
    vision_wards_bought                SMALLINT     NOT NULL,
    spell1_casts                       SMALLINT     NOT NULL,
    spell2_casts                       SMALLINT     NOT NULL,
    spell3_casts                       SMALLINT     NOT NULL,
    spell4_casts                       SMALLINT     NOT NULL,
    summoner1_id                       INT          NOT NULL,
    summoner2_id                       INT          NOT NULL,
    summoner1_casts                    SMALLINT     NOT NULL,
    summoner2_casts                    SMALLINT     NOT NULL,
    primary_style_id                   INT NULL,
    primary_perk_0                     INT NULL,
    primary_perk_1                     INT NULL,
    primary_perk_2                     INT NULL,
    primary_perk_3                     INT NULL,
    sub_style_id                       INT NULL,
    sub_perk_0                         INT NULL,
    sub_perk_1                         INT NULL,
    stat_defense                       INT NULL,
    stat_flex                          INT NULL,
    stat_offense                       INT NULL,
    all_in_pings                       SMALLINT     NOT NULL,
    assist_me_pings                    SMALLINT     NOT NULL,
    basic_pings                        SMALLINT     NOT NULL,
    command_pings                      SMALLINT     NOT NULL,
    danger_pings                       SMALLINT     NOT NULL,
    enemy_missing_pings                SMALLINT     NOT NULL,
    enemy_vision_pings                 SMALLINT     NOT NULL,
    get_back_pings                     SMALLINT     NOT NULL,
    hold_pings                         SMALLINT     NOT NULL,
    need_vision_pings                  SMALLINT     NOT NULL,
    omw_pings                          SMALLINT     NOT NULL,
    push_pings                         SMALLINT     NOT NULL,
    retreat_pings                      SMALLINT     NOT NULL,
    vision_cleared_pings               SMALLINT     NOT NULL,
    game_ended_in_surrender            BOOLEAN      NOT NULL,
    game_ended_in_early_surrender      BOOLEAN      NOT NULL,
    was_afk                            BOOLEAN      NOT NULL,

    -- Arena-specific fields (NULL when not applicable)
    subteam_id                         SMALLINT     NULL,
    player_augment_1                   INT          NULL,
    player_augment_2                   INT          NULL,
    player_augment_3                   INT          NULL,
    player_augment_4                   INT          NULL,
    player_augment_5                   INT          NULL,
    player_augment_6                   INT          NULL,

    -- Preserve Riot's nested participant data as JSON
    challenges                         JSON         NULL,
    missions                           JSON         NULL,

    PRIMARY KEY (match_id, participant_id),
    INDEX idx_participants_puuid (puuid),
    INDEX idx_participants_champion (champion_id, team_position),
    CONSTRAINT fk_participants_match
        FOREIGN KEY (match_id) REFERENCES matches (match_id) ON DELETE CASCADE,
    CONSTRAINT fk_participants_subteam
        FOREIGN KEY (match_id, subteam_id)
        REFERENCES subteams (match_id, subteam_id)
        ON DELETE CASCADE

);

CREATE TABLE match_timelines (
    match_id            VARCHAR(20) PRIMARY KEY,
    frame_interval      INT NOT NULL,
    end_of_game_result  VARCHAR(50),

    FOREIGN KEY (match_id)
        REFERENCES matches(match_id)
);

CREATE TABLE timeline_frames (
    match_id                VARCHAR(20) NOT NULL,
    frame_index             SMALLINT UNSIGNED NOT NULL,
    timestamp_ms            INT UNSIGNED NOT NULL,

    PRIMARY KEY (match_id, frame_index),

    FOREIGN KEY (match_id)
        REFERENCES match_timelines(match_id)
);

CREATE TABLE timeline_events (
    event_id        BIGINT AUTO_INCREMENT PRIMARY KEY,

    match_id        VARCHAR(20) NOT NULL,
    frame_index     SMALLINT UNSIGNED NOT NULL,
    timestamp_ms    INT UNSIGNED NOT NULL,

    event_type      VARCHAR(50) NOT NULL,
    event_data      JSON NOT NULL,

    INDEX idx_match_timestamp (match_id, timestamp_ms),
    INDEX idx_event_type (event_type),

    FOREIGN KEY (match_id, frame_index)
        REFERENCES timeline_frames(match_id, frame_index)
);

CREATE TABLE participant_frames (
    match_id                        VARCHAR(20) NOT NULL,
    frame_index                     SMALLINT UNSIGNED NOT NULL,
    participant_id                  TINYINT UNSIGNED NOT NULL,
    puuid                           VARCHAR(78) NOT NULL,

    level                           TINYINT UNSIGNED,
    current_gold                    INT,
    total_gold                      INT,
    xp                              INT,
    minions_killed                  INT,
    jungle_minions_killed           INT,
    gold_per_second                 INT,
    time_enemy_spent_controlled     INT,

    position_x                      INT,
    position_y                      INT,

    champion_stats                  JSON,
    damage_stats                    JSON,

    PRIMARY KEY (match_id, frame_index, participant_id),

    FOREIGN KEY (match_id, frame_index)
        REFERENCES timeline_frames(match_id, frame_index)
);

CREATE TABLE rank_snapshots (
    rank_snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    puuid               VARCHAR(78) NOT NULL,
    region              VARCHAR(16) NOT NULL,

    queue_type          VARCHAR(40) NOT NULL,
    tier                VARCHAR(20) NOT NULL,
    division            VARCHAR(5) NOT NULL,
    league_points       SMALLINT UNSIGNED NOT NULL,
    wins                INT UNSIGNED NOT NULL,
    losses              INT UNSIGNED NOT NULL,
    veteran             BOOLEAN NOT NULL,
    inactive            BOOLEAN NOT NULL,
    fresh_blood         BOOLEAN NOT NULL,
    hot_streak          BOOLEAN NOT NULL,

    captured_at         DATETIME NOT NULL,

    INDEX idx_rank_history (puuid, region, queue_type, captured_at),

    INDEX idx_rank_lookup (queue_type, tier, division),

    FOREIGN KEY (puuid, region)
        REFERENCES summoners (puuid, region)
        ON DELETE CASCADE
);