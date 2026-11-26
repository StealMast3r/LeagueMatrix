# LeagueMatrix — Complete Match Statistics & Analysis Specification

**Version:** 1.0  
**Scope:** Match, participant, team, Arena, timeline frame, participant frame, and timeline event data  
**Purpose:** A comprehensive inventory of statistics, rankings, tables, visualizations, and analytical questions that can be derived from the current database.

---

## 0. Data model, conventions, and analysis rules

### 0.1 Available datasets

| Dataset | Grain | Main identifiers | Intended use |
|---|---|---|---|
| `participants_df` | One row per match played by the tracked player | `match_id`, `participant_id`, `puuid` | The tracked player's match history |
| `matches_df` | One row per match | `match_id` | Match metadata, mode, patch, duration, timestamps |
| `teams_df` | One row per team per match | `match_id`, `team_id` | Team result and team objectives |
| `subteams_df` | One row per Arena subteam per match | `match_id`, `subteam_id` | Arena placement |
| `all_participants_df` | One row per participant per match, including the tracked player | `match_id`, `participant_id`, `puuid` | Teammate, opponent, team, and lobby comparisons |
| `match_timelines_df` | One row per match timeline | `match_id` | Timeline metadata and frame interval |
| `timeline_frames_df` | One row per match frame | `match_id`, `frame_index` | Frame timestamps and frame sequence |
| `participant_frames_df` | One row per participant per frame | `match_id`, `frame_index`, `participant_id` | Gold, XP, level, CS, position, champion and damage snapshots |
| `timeline_events_df` | One row per event | `event_id`, `match_id`, `frame_index`, `timestamp_ms` | Chronological match events |

**Important relationship:** `participants_df` is the tracked player's subset of `all_participants_df`. The latter includes the tracked player and the other participants in those same matches. Do not count the tracked player's row twice when aggregating all-player data.

### 0.2 General calculation rules

- **0.2.1 — Totals:** Sum additive values across matches (kills, assists, gold earned, damage, wards, etc.).
- **0.2.2 — Per-game averages:** Divide the total by the number of eligible games. Also report the median.
- **0.2.3 — Per-minute rates:** Divide by actual minutes played, not by the number of games. Use a consistent duration unit.
- **0.2.4 — Team rates:** Aggregate players within a team first; do not average player averages when a true team total is required.
- **0.2.5 — Win rate:** Wins divided by eligible completed games. Exclude remakes or games with missing/invalid results where appropriate.
- **0.2.6 — KDA ratio:** `(kills + assists) / deaths`; define a consistent zero-death convention, such as displaying infinity or `(kills + assists)` with a zero-death flag.
- **0.2.7 — Kill participation:** `(player kills + player assists) / team champion kills`. Handle zero team kills and duplicate/missing team records.
- **0.2.8 — Sample sizes:** Always display games played beside rates. Use configurable minimum sample sizes for champion, rune, item, and matchup rankings.
- **0.2.9 — Mode separation:** Keep Ranked, Normal, ARAM, Arena, and other queues separate unless a page explicitly compares them.
- **0.2.10 — Patch separation:** Allow patch filters and show patch context for comparisons across balance changes.
- **0.2.11 — Missing values:** Distinguish zero from NULL / unavailable. Do not silently replace missing data with zero.
- **0.2.12 — Duplicate prevention:** Use the correct grain and keys for every aggregation. In particular, do not join two one-to-many tables together and then sum duplicated values.
- **0.2.13 — Percentiles:** Where useful, show median, 25th percentile, 75th percentile, and 90th percentile in addition to mean.
- **0.2.14 — Outliers:** Keep exceptional games visible in leaderboards, but also provide robust summaries that are not dominated by one extreme match.
- **0.2.15 — Confidence:** Show sample size and, where practical, confidence intervals for win rates. Avoid treating tiny samples as reliable evidence.
- **0.2.16 — Comparison groups:** Make comparisons selectable by champion, role, queue, patch, date range, and game result.
- **0.2.17 — Tracked-player identity:** Use `puuid` to identify the tracked player, not Riot ID text, which can change.
- **0.2.18 — Time conversion:** Convert timestamps to a readable timezone for display, while retaining original UTC/epoch values for storage and sorting.
- **0.2.19 — Timeline alignment:** Use `timestamp_ms` / frame timestamps to align events and participant snapshots. Confirm whether timestamps are match-relative before interpreting them.
- **0.2.20 — Event schema:** Treat `event_type` as an extensible category. Preserve unknown event types and inspect `event_data` rather than discarding events that are not in a known list.

---

# 1. Overall performance dashboard

## 1.1 Career / database overview

### 1.1.1 Core volume
- Total eligible matches. 1.1.1.1
- Total wins and losses. 1.1.1.2
- Overall win rate. 1.1.1.2
- Total playtime and average match duration.
- Games per day, week, month, and year.
- Unique champions played.
- Unique roles played.
- Unique patches represented.
- Unique queues / game modes represented.

### 1.1.2 Overall performance
- Total kills, deaths, assists.
- Average and median kills, deaths, assists per game.
- Overall KDA ratio.
- Average and median kill participation.
- Average champion damage and damage per minute.
- Average gold earned and gold per minute.
- Average CS and CS per minute.
- Average vision score and vision score per minute.
- Average healing, shielding, crowd-control time, and damage taken.
- Average champion level at game end.

### 1.1.3 Personal records
- Highest kills, assists, KDA, damage, damage/minute, gold, gold/minute, CS, CS/minute, vision score, healing, shielding, crowd-control time, and kill participation.
- Lowest deaths in a full-length game.
- Longest match and shortest match.
- Longest winning and losing streak.
- Best 5-, 10-, and 20-game stretches by win rate and selected performance metrics.

## 1.2 Summary cards
Display cards for games, win rate, KDA, kills/game, deaths/game, assists/game, damage/minute, gold/minute, CS/minute, vision/minute, and current streak.

## 1.3 Core charts
- Win/loss donut.
- Games played by month.
- Win rate by month.
- Rolling 5-, 10-, and 20-game win rate.
- Rolling KDA and damage/minute.
- Cumulative wins and losses.
- Match duration distribution.
- Performance percentile cards.

## 1.4 Match leaderboards
Create Top 10 and Bottom 10 tables, with match date, champion, role, result, patch, queue, duration, and the ranked metric:
- Highest KDA.
- Most kills.
- Most assists.
- Most deaths.
- Fewest deaths (with minimum duration filter).
- Highest kill participation.
- Highest champion damage.
- Highest physical, magic, and true champion damage.
- Highest damage/minute.
- Highest gold and gold/minute.
- Highest CS and CS/minute.
- Highest vision score and vision score/minute.
- Highest healing, shielding, and crowd-control time.
- Highest team damage contribution.
- Highest team gold contribution.
- Highest objective contribution.
- Longest and shortest games.

---

# 2. Champion analysis

## 2.1 Champion summary table
For every champion:
- Games, wins, losses, win rate, pick frequency.
- Average and median K/D/A and KDA.
- Average kill participation.
- Average champion damage and damage/minute.
- Average damage taken, healing, shielding, and crowd control.
- Average gold and gold/minute.
- Average CS and CS/minute.
- Average vision score and vision/minute.
- Average game duration and champion level.
- First-item / final-build popularity where data permits.
- Most-used keystone and rune page.
- Most-used summoner spell combination.
- Most common role and lane.

## 2.2 Champion leaderboards
- Most played champions.
- Highest win rate with minimum sample threshold.
- Highest KDA, kills, assists, damage/minute, gold/minute, CS/minute, vision/minute, and kill participation.
- Lowest deaths and lowest death rate.
- Best champions by role and queue.
- Worst champions by win rate and selected performance metrics.

## 2.3 Champion performance charts
- Games played by champion.
- Win rate by champion with sample-size labels.
- KDA and damage/minute by champion.
- Champion win rate versus games played scatter plot.
- Champion performance radar chart.
- Champion pick frequency over time.
- Champion win rate and KDA over time.
- Champion performance by patch.
- Champion performance by role.

## 2.4 Champion consistency
- Standard deviation and interquartile range for kills, deaths, assists, KDA, damage, gold, CS/min, and vision.
- Percentage of games above personal overall average.
- Percentage of games with positive KDA.
- Percentage with 10+ kills, 10+ assists, or fewer than 5 deaths.
- Best and worst match for each champion.
- Consistency score based on selected metrics.

## 2.5 Champion-specific matchups
Using `all_participants_df`:
- Games against each opposing champion.
- Win rate and sample size against each champion.
- KDA, damage, gold, and CS/min in those matchups.
- Same-lane opponent comparisons when role/lane data is reliable.
- Champion matchup matrix / heatmap.
- Best and worst opposing champion matchups.
- Performance against each champion by patch and role.

---

# 3. Role, lane, and position analysis

## 3.1 Role distribution
- Games, wins, losses, win rate, and pick frequency by `team_position`.
- Repeat for `individual_position`, `lane`, and `player_role`.
- Identify missing, unknown, and inconsistent role labels.

## 3.2 Role performance
- K/D/A, KDA, kill participation.
- Damage and damage/minute.
- Gold and gold/minute.
- CS and CS/minute.
- Vision score and vision/minute.
- Healing, shielding, damage taken, and crowd-control time.
- Objectives and structure takedowns.
- Game duration and win rate.

## 3.3 Role comparisons
- Five-role comparison table.
- Role radar chart.
- Win rate by role.
- Damage/minute and gold/minute by role.
- CS/minute and vision/minute by role.
- Champion-role combinations.
- Best and worst champions within each role.

## 3.4 Lane matchup comparisons
- Tracked player versus opposing lane opponent: kills, deaths, assists, CS, gold, level, and damage.
- Gold difference at 5, 10, 15, and 20 minutes.
- CS difference at 5, 10, 15, and 20 minutes.
- XP / level difference at selected timestamps.
- Lane matchup outcome versus final match result.
- Caveat: lane opponent identification must be validated; role labels can be missing or unusual.

---

# 4. KDA, kills, deaths, assists, and combat

## 4.1 Core combat totals
- Total and average kills, deaths, assists.
- KDA ratio and kill/death ratio.
- Kills, deaths, and assists per minute / per 10 minutes.
- Kill participation and kill share.
- Team kill share and death share.
- Largest killing spree and average killing sprees.
- Largest multikill and counts of double, triple, quadra, penta, and unreal kills.

## 4.2 Combat leaderboards
- Top 10 KDA games.
- Top 10 kills, assists, killing sprees, and multikills.
- Top 10 kill participation.
- Top 10 fewest deaths, with duration threshold.
- Bottom 10 KDA and highest-death games.
- Best combat games by champion, role, queue, and patch.

## 4.3 Combat distributions and relationships
- Kills, deaths, assists, and KDA histograms.
- Kills versus deaths scatter plot.
- Kills versus assists scatter plot.
- KDA versus game duration.
- Kill participation versus win/loss.
- Deaths per 10 minutes by champion and role.
- Deaths in wins versus losses.
- Percentage of games with positive KDA.
- Percentage of games with 0, 1–3, 4–5, 6–9, and 10+ deaths.

## 4.4 Survival
- Total and average time spent dead.
- Percentage of match spent dead.
- Longest time spent living.
- Deaths per 10 minutes.
- Time spent dead by champion, role, and result.
- Relationship between time dead, missed CS, objectives, and match outcome.

---

# 5. Damage, durability, healing, shielding, and crowd control

## 5.1 Damage dealt
- Total damage dealt to all targets.
- Physical, magic, and true damage dealt.
- Total champion damage.
- Physical, magic, and true champion damage.
- Damage to buildings, turrets, epic monsters, and objectives.
- Champion damage per minute.
- Total damage per minute.
- Damage composition percentages.
- Champion damage as a percentage of all damage dealt.

## 5.2 Damage received and mitigation
- Total, physical, magic, and true damage taken.
- Self-mitigated damage.
- Damage taken per minute.
- Mitigation percentage / ratio where definitions permit.
- Damage taken relative to game duration and champion role.

## 5.3 Healing and shielding
- Total healing.
- Healing on teammates.
- Damage shielded on teammates.
- Healing and shielding per minute.
- Healing / shielding by champion and role.
- Healing and shielding in wins versus losses.

## 5.4 Crowd control
- `time_cc_others`.
- `total_time_cc_dealt`.
- Crowd-control time per minute.
- Crowd-control time by champion and role.
- Crowd-control contribution relative to team.
- Relationship between crowd control, assists, and team kills.

## 5.5 Damage leaderboards and charts
- Top 10 champion damage, physical/magic/true champion damage, damage/minute, damage taken, healing, shielding, and crowd control.
- Damage composition stacked bars.
- Damage dealt versus damage taken.
- Damage versus gold.
- Damage versus game duration.
- Damage by champion, role, patch, and result.
- Tracked player's share of team damage.

---

# 6. Farming and economy

## 6.1 Farming totals
- Total minions killed.
- Neutral minions killed.
- Ally jungle minions killed.
- Enemy jungle minions killed.
- CS per game and CS/minute.
- Lane CS/minute and jungle CS/minute.
- Enemy jungle CS/minute.
- Farming split between lane and jungle.

## 6.2 Gold economy
- Total gold earned and spent.
- Average / median gold earned and spent.
- Gold per minute.
- Gold remaining (`gold_earned - gold_spent`), interpreted cautiously.
- Gold spent as percentage of gold earned.
- Gold per CS.
- Gold per kill.
- Gold by champion, role, patch, and result.

## 6.3 Farming and economy leaderboards
- Top 10 CS, CS/minute, gold, gold/minute, gold spent, enemy jungle CS, and jungle CS.
- Bottom 10 CS/minute and gold/minute, with duration and role context.
- Best farming games by champion and role.

## 6.4 Timeline economy analysis
At 5, 10, 15, 20, 25, and 30 minutes, where frames exist:
- Current gold.
- Total gold.
- Gold difference against lane opponent.
- Gold difference against opposing team.
- XP and level difference.
- Minion and jungle CS.
- Gold per second / gold accumulation rate.
- Gold lead / deficit trajectories.
- Time to reach selected gold milestones.
- Time to reach level 6, 11, and 16.
- First-item timing only if item purchase events exist.
- Farming pace between consecutive snapshots.

## 6.5 Charts
- CS/min and gold/min distributions.
- Gold and CS over time.
- Gold difference over time.
- CS difference over time.
- Gold versus damage.
- Gold versus kills.
- Farming versus win rate.
- Champion / role farming comparisons.

---

# 7. Vision and map awareness

## 7.1 Vision totals
- Vision score.
- Wards placed and killed.
- Detector wards placed.
- Sight wards bought.
- Vision wards bought.
- Vision score/minute.
- Wards placed and killed per 10 minutes.
- Ward clearing ratio.
- Vision score per ward placed.

## 7.2 Vision leaderboards
- Top 10 vision score and vision/minute.
- Top 10 wards placed and killed.
- Top 10 detector wards placed.
- Lowest vision games by support / non-support role.

## 7.3 Vision comparisons
- Vision by champion, role, queue, patch, and result.
- Vision in wins versus losses.
- Tracked player versus teammates and opposing support.
- Vision versus KDA, objectives, and win rate.

## 7.4 Timeline vision
From `WARD_PLACED` and `WARD_KILL` events, where event data includes the required details:
- Wards placed / removed over match time.
- Ward type and subtype distribution.
- Placement and removal coordinates.
- Ward lifetime.
- Ward placement heatmap.
- Ward clearing heatmap.
- Time between ward placements.
- Vision activity before major objectives.
- Ward activity by side of map and game phase.

---

# 8. Runes and stat shards

## 8.1 Rune popularity
- Primary style popularity.
- Secondary style popularity.
- Keystone popularity.
- Primary minor rune popularity.
- Secondary minor rune popularity.
- Defense, flex, and offense shard popularity.
- Full rune-page popularity.

## 8.2 Rune performance
For each keystone, rune, style, shard, and complete rune page:
- Games and sample size.
- Wins, losses, win rate.
- KDA, kills, deaths, assists.
- Damage and damage/minute.
- Gold and gold/minute.
- CS/minute.
- Vision/minute.
- Performance by champion, role, queue, and patch.

## 8.3 Rune leaderboards and charts
- Most-used runes.
- Highest win-rate runes with sample threshold.
- Best keystone by champion.
- Best secondary tree by champion.
- Most successful complete pages.
- Rune popularity over time.
- Rune win-rate heatmap by champion.
- Rune selection before and after patches.

## 8.4 Rune caveats
Rune IDs identify selections, not necessarily rune-generated damage, healing, shielding, or other effects. Actual rune value requires a source that records those effects, if available.

---

# 9. Items and builds

## 9.1 Item popularity
From final item slots:
- Most-used items.
- Boots popularity.
- Consumable popularity.
- Item popularity by champion, role, queue, and patch.
- Final item-slot distribution.
- Common final item combinations.

## 9.2 Item performance
For each item:
- Games containing the item.
- Wins, losses, and win rate.
- KDA, damage, gold, CS/minute, and vision.
- Champion and role distribution.
- Patch distribution.
- Performance with and without the item, with suitable controls and caveats.

## 9.3 Build analysis
- Most common final builds.
- Highest win-rate final builds with minimum sample.
- Builds by champion and role.
- First / second / third item only when purchase-order data is available.
- Boot choices.
- Item pair and item trio combinations.
- Build performance by patch.
- Build performance by game duration.

## 9.4 Timeline item events
Recognize and analyze event types such as:
- `ITEM_PURCHASED`
- `ITEM_SOLD`
- `ITEM_DESTROYED`
- `ITEM_UNDO`

For these events, if `event_data` supplies item ID, participant ID, and timestamp:
- Purchase order.
- First completed item timing.
- Item completion timing.
- Purchase and sale counts.
- Item undo frequency.
- Gold spent on items over time.
- Build path comparisons.
- Purchases before / after objectives.
- Item purchase heatmap by match time.

## 9.5 Item caveats
Final inventory slots do not preserve purchase order. `items_purchased` is a count, not an item-level purchase history. Use timeline item events for build paths and timing.

---

# 10. Summoner spells, abilities, levels, and skill order

## 10.1 Summoner spells
- Spell 1 and spell 2 popularity.
- Spell combination popularity.
- Win rate by spell and combination.
- Spell selection by champion and role.
- Cast counts and casts per minute.
- Spell use in wins versus losses.

## 10.2 Ability casts
- Q / W / E / R cast totals and averages.
- Casts per minute.
- Ability usage by champion and role.
- Ability casts versus damage.
- Ability casts versus game duration.
- Ability usage in wins versus losses.

## 10.3 Skill level-up timeline
From `SKILL_LEVEL_UP` events:
- First ability selected.
- Skill order by champion.
- Most common skill order.
- Skill order win rate with minimum sample.
- Level at which each ability is upgraded.
- Time to level 6 / 11 / 16.
- Skill order differences by patch.

## 10.4 Level progression
From participant frames and `LEVEL_UP` events, where present:
- Level over time.
- Time to each level.
- Level lead / deficit against lane opponent.
- Level lead / deficit against opposing team.
- XP accumulation over time.
- XP per minute.
- Level distribution at selected timestamps.

---

# 11. Teammate, opponent, and lobby analysis

## 11.1 Team totals
Using `all_participants_df`, grouped by match and team:
- Team kills, deaths, assists.
- Team gold and CS.
- Team champion damage.
- Team damage taken.
- Team vision.
- Team healing, shielding, and crowd control.
- Team objective and structure statistics from `teams_df`.
- Team average level.
- Team performance per minute.

## 11.2 Tracked-player contribution
- Percentage of team kills and assists.
- Kill participation.
- Percentage of team champion damage.
- Percentage of team gold.
- Percentage of team CS.
- Percentage of team vision.
- Share of team healing / shielding.
- Within-team rank for kills, deaths, assists, KDA, damage, gold, CS, and vision.

## 11.3 Teammate analysis
- Average teammate KDA and performance.
- Teammate performance in wins versus losses.
- Highest-performing teammate in each game.
- Games where tracked player led the team.
- Games where tracked player was not the top contributor.
- Team consistency and performance spread.
- Repeated teammate combinations, if player identities are retained.

## 11.4 Opponent analysis
- Enemy team kills, deaths, assists, gold, CS, damage, vision.
- Highest- and lowest-performing enemy.
- Tracked player versus direct lane opponent.
- Tracked player versus opposing same-role player.
- Champion matchup statistics.
- Games where tracked player outperformed / was outperformed by opponent.

## 11.5 Lobby and team balance
- Total team gold and damage differences.
- Team KDA / level / CS differences.
- Distribution of performance within each team.
- Team result versus team total statistics.
- Tracked player's contribution relative to the other nine players.

## 11.6 Leaderboards and charts
- Top 10 games by damage share, gold share, kill participation, and lane-opponent advantage.
- Tracked player versus team average.
- Team versus enemy team.
- Player ranking within each match.
- Team contribution stacked bars.
- Lane matchup scatter plots.

---

# 12. Objectives, structures, and macro

## 12.1 Personal objective statistics
- Baron kills.
- Dragon kills.
- Turret kills and takedowns.
- Turrets lost.
- Inhibitor kills and takedowns.
- Inhibitors lost.
- Nexus kills, takedowns, and losses.
- Objectives stolen and steal assists.
- Damage to epic monsters, objectives, turrets, and buildings.

## 12.2 Team objective statistics
From `teams_df`:
- Champion kills.
- First blood.
- Baron kills and first baron.
- Dragon kills and first dragon.
- Tower kills and first tower.
- Inhibitor kills and first inhibitor.
- Rift Herald kills and first Herald.

## 12.3 Objective impact
- Win rate with first blood / tower / dragon / baron / inhibitor.
- Win rate with at least one dragon / baron / Herald.
- Average objectives in wins versus losses.
- Objective steals and match outcomes.
- Turret / inhibitor differential.
- Personal objective contribution by champion and role.
- Objective performance by patch and game duration.

## 12.4 Timeline objective events
Recognize:
- `ELITE_MONSTER_KILL`
- `BUILDING_KILL`
- `TURRET_PLATE_DESTROYED`

Analyze:
- Dragon type, killer, team, and timestamp.
- Baron / Herald / other epic monster kills.
- First objective timing.
- Time between objectives.
- Objective sequence.
- Objective control by side.
- Turret destruction order and location.
- Inhibitor destruction timing.
- Nexus destruction timing.
- Turret plate timing and distribution.
- Objective fights: kills and deaths shortly before / after objective events, where event timestamps allow.
- Objective control versus gold lead and final result.

## 12.5 Objective charts
- Objective timeline.
- Dragons / barons / towers by match.
- First objective versus win rate.
- Objective differential versus win rate.
- Objective timing distribution.
- Map objective heatmap if coordinates exist.

---

# 13. Pings, communication, surrender, and AFK

## 13.1 Ping totals
- All-in, assist-me, basic, command, danger, enemy-missing, enemy-vision, get-back, hold, need-vision, on-my-way, push, retreat, and vision-cleared pings.
- Total pings per game.
- Pings per minute and per 10 minutes.
- Ping composition by type.
- Pings by champion, role, queue, patch, and result.

## 13.2 Ping leaderboards and charts
- Top 10 total pings.
- Top 10 by ping type.
- Ping distribution.
- Pings over time.
- Pings in wins versus losses.
- Ping count versus kill participation / objective control.
- Avoid interpreting ping volume alone as communication quality.

## 13.3 Match behavior
- Surrendered games.
- Early surrender games.
- Surrender rates by queue, patch, and champion.
- Win rate in games with / without surrender.
- AFK match frequency.
- AFK frequency by champion and role.
- Performance in games marked AFK.
- Separate player AFK indicators from match-level surrender outcomes.

---

# 14. Game mode, queue, patch, map, and time analysis

## 14.1 Queue and mode
- Games, wins, losses, win rate by queue ID.
- Game mode and game type distribution.
- Map ID distribution.
- Performance by queue and game mode.
- Champion popularity and performance by mode.
- Match duration by mode.

## 14.2 Patch and version
- Games played by patch and game version.
- Win rate by patch.
- KDA, damage, gold, CS/minute, and vision/minute by patch.
- Champion performance changes between patches.
- Rune and item selection changes by patch.
- Before / after patch comparisons.

## 14.3 Calendar analysis
- Games by hour, weekday, month, and year.
- Win rate by hour and weekday.
- Average KDA and performance by hour.
- Games per session.
- Time between matches.
- Longest session.
- Performance over consecutive games.
- First game versus later games in a session.

## 14.4 Streaks and form
- Current win / loss streak.
- Longest winning / losing streak.
- Rolling 5 / 10 / 20-game win rate.
- Best / worst 10- and 20-game periods.
- Performance after a win versus after a loss.
- Performance after long breaks versus short breaks, if session gaps are defined.

## 14.5 Time charts
- Games and win rate by month.
- Patch performance trend.
- Heatmap of games by weekday and hour.
- Rolling performance.
- Cumulative playtime.
- Session length distribution.

---

# 15. Arena, subteams, and augments

## 15.1 Arena placements
Using `subteams_df`:
- Arena games.
- Placement distribution.
- Average and median placement.
- First-place finishes.
- Top-four finishes.
- Placement by champion, patch, and augment.
- Placement versus KDA, damage, gold, and game duration.

## 15.2 Subteam comparisons
Using `subteam_id` in participant rows:
- Players in each subteam.
- Subteam kills, damage, gold, and other available totals.
- Tracked player's contribution within subteam.
- Subteam composition and placement.
- Subteam performance by champion combinations.

## 15.3 Augments
- Popularity of each augment slot.
- Augment frequency and combinations.
- Placement / win rate by augment.
- Average damage, KDA, and other stats by augment.
- Augment combinations by champion.
- Augment popularity and performance over time / patch.

## 15.4 Arena charts
- Placement distribution.
- Augment popularity.
- Augment performance.
- Champion / augment heatmap.
- Subteam composition and placement comparisons.

---

# 16. Challenges and missions

## 16.1 Challenges
Inspect the structure and available keys inside `challenges` before defining metrics.
- Challenge values and scores.
- Challenge distribution.
- Highest and average challenge scores.
- Challenge values by champion, role, queue, and patch.
- Challenge performance over time.
- Combat, farming, vision, objective, and other challenge groupings where keys support them.

## 16.2 Missions
Inspect the structure of `missions` before defining metrics.
- Mission keys and values.
- Mission progress / completion where represented.
- Mission data by mode and date.
- Mission changes over time.
- Do not assume a mission field is a completion count without verifying its meaning.

---

# 17. Timeline frame analysis

## 17.1 Timeline metadata
From `match_timelines_df`:
- Frame interval.
- End-of-game result.
- Timeline availability rate.
- Timeline coverage versus match duration.
- Matches with missing or incomplete timelines.

## 17.2 Frame sequence
From `timeline_frames_df`:
- Number of frames per match.
- Frame interval consistency.
- First and last frame timestamps.
- Missing frame indices.
- Timestamp gaps.
- Actual timeline coverage.

## 17.3 Participant frame snapshots
From `participant_frames_df`:
- Level.
- Current gold.
- Total gold.
- XP.
- Minions killed.
- Jungle minions killed.
- Gold per second.
- Time enemy spent controlled.
- Position X and Y.
- Champion stats JSON / object.
- Damage stats JSON / object.

## 17.4 Time-based player progression
At standard timestamps (5, 10, 15, 20, 25, 30 minutes), if available:
- Level, XP, current gold, total gold.
- Lane CS and jungle CS.
- Gold/minute and XP/minute.
- Gold and XP difference versus lane opponent.
- Gold and XP difference versus team / enemy team.
- Position and movement.
- Champion stats and damage stats.
- Progression curves for tracked player and all nine other participants.

## 17.5 Frame-derived metrics
- Gold gained between frames.
- XP gained between frames.
- CS gained between frames.
- Level-up timing.
- Gold accumulation rate.
- CS accumulation rate.
- Time spent in different map regions, if position sampling is sufficient.
- Distance moved between frames, with caution about sampling interval.
- Position heatmaps.
- Lane / jungle / river / base occupancy estimates, if map-coordinate mapping is implemented.

## 17.6 Frame charts
- Gold over time.
- XP over time.
- Level over time.
- CS over time.
- Gold difference over time.
- XP / level difference over time.
- Player position heatmap.
- Team position snapshots.
- Damage / champion stats over time where nested fields support them.

---

# 18. Timeline event analysis

## 18.1 Event system and event inventory
`event_type` can contain multiple event categories and may evolve. Build an event-type inventory from the actual database:
- Count events by `event_type`.
- Count unique event types.
- Count events by patch, queue, and match.
- Identify event types with missing or inconsistent `event_data`.
- Record all observed `event_data` keys per event type.
- Track newly observed event types over time.
- Preserve unknown event types for future analysis.
- Build a normalized event dictionary / schema registry based on observed data.

## 18.2 Champion kill events
Common event type: `CHAMPION_KILL`
- Total kills and deaths from event records.
- Killer, victim, and assisting participants.
- Team and champion involved.
- Timestamp of each kill.
- First blood event and timestamp.
- Kill location (position X/Y) if present.
- Kill participation from event records.
- Solo kills versus assisted kills, if assister list is present.
- Multi-kill sequences from event timing.
- Kill streaks and shutdown / bounty information if present.
- Kill timing by early, mid, and late game.
- Death heatmaps.
- Kill heatmaps.
- Kill / death timeline.
- Kills before and after objectives.
- Gank timing and lane kill analysis where position and roles support it.

## 18.3 Elite monster events
Common event type: `ELITE_MONSTER_KILL`
- Monster type.
- Killer and killer team.
- Assisting participants if present.
- Monster timestamp.
- Monster position if present.
- Dragon elemental type and soul / elder details if represented.
- Baron, Rift Herald, Void Grub, and other elite monster counts where event data supports them.
- First monster timing.
- Time between monster kills.
- Objective sequence and team control.
- Steals and opposing-team kills.
- Team kills shortly before / after monster events.
- Monster kill heatmap and timeline.

## 18.4 Building and structure events
Common event type: `BUILDING_KILL`
- Building type.
- Tower / inhibitor / nexus type and lane where present.
- Killer and killer team.
- Assisting participants if present.
- Timestamp and location.
- First tower / first structure.
- Tower destruction order.
- Structure takedowns by team and player.
- Time to first tower.
- Time to inhibitor and nexus.
- Structure progression timeline.
- Structure location map.

## 18.5 Turret plate events
Common event type: `TURRET_PLATE_DESTROYED`
- Participant and team credited.
- Timestamp.
- Turret / lane / location if present.
- Plate count per player and team.
- First plate timing.
- Plates by lane and game phase.
- Plate gold estimates only if the relevant event data or game-version rules are available.
- Plate events versus lane gold lead.

## 18.6 Item events
Common event types:
- `ITEM_PURCHASED`
- `ITEM_SOLD`
- `ITEM_DESTROYED`
- `ITEM_UNDO`

Analyze purchase / sale / destroy / undo timestamps, participant, item ID, item sequence, first item, completed item timing, inventory path, and item changes around objectives.

## 18.7 Ward events
Common event types:
- `WARD_PLACED`
- `WARD_KILL`

Analyze ward type, creator, killer, team, timestamp, position, ward lifetime, placement / removal heatmaps, and objective-area vision activity.

## 18.8 Skill and level events
Common event types:
- `SKILL_LEVEL_UP`
- `LEVEL_UP`

Analyze ability upgrades, skill order, level-up timestamps, time to level milestones, and XP progression. Cross-check event values against participant frame snapshots.

## 18.9 Other / less common event types
Depending on game mode, patch, and Riot timeline payload, inspect for:
- `GAME_END`
- `CHAMPION_SPECIAL_KILL`
- `ASCENDED_EVENT`
- `CAPTURE_POINT`
- `PORO_KING_SUMMON`
- `OBJECTIVE_BOUNTY_PRESTART`
- `OBJECTIVE_BOUNTY_ACTIVATED`
- `OBJECTIVE_BOUNTY_FINISH`
- `TURRET_PLATE_DESTROYED`
- Mode-specific events, Arena events, or future API event types.

For every unfamiliar type, retain raw `event_data`, record its keys, and document its meaning only after verifying actual payloads. Do not assume every listed event appears in every queue or patch.

## 18.10 Event sequencing and event windows
- Events per minute.
- Events by game phase.
- Time between events of the same type.
- Kill sequences and teamfight windows.
- Kills / deaths within configurable windows before and after an objective.
- Wards placed before objectives.
- Purchases before / after recalls or objectives, if recall events exist.
- First event of each category.
- Event density by match.
- Event timelines with filters by type, player, team, and time.

## 18.11 Event charts and maps
- Event count by type.
- Event timeline / raster plot.
- Kill and death timeline.
- Objective timeline.
- Ward placement / kill heatmaps.
- Building destruction map.
- Kill locations by champion / role.
- Event map with selectable categories.
- Event count per minute by category.

---

# 19. Advanced analytics and statistical discovery

## 19.1 Correlation analysis
Explore correlations between:
- KDA and win rate.
- Deaths and win rate.
- Damage and win rate.
- Gold and win rate.
- CS/minute and win rate.
- Vision and win rate.
- Kill participation and win rate.
- Objective participation and win rate.
- Damage taken and deaths.
- Gold and damage.
- CS and gold.
- Game duration and KDA.
- Pings and objective participation.
- Early gold / XP lead and final result.

Use correlation coefficients and scatter plots. Correlation is not causation.

## 19.2 Performance profiles
Classify matches into configurable profiles:
- Carry: high damage and / or kill participation.
- Farming: high CS and gold.
- Supportive: high assists, vision, healing, shielding, or crowd control.
- Durable: high damage taken / mitigation with reasonable deaths.
- Objective-focused: high objective contribution.
- Dominant: strong performance across several metrics.
- Struggling: below personal baseline across several metrics.

Clearly label these as analytical classifications, not official game ratings.

## 19.3 Composite performance score
Optional weighted score using normalized metrics such as:
- KDA / kill participation.
- Damage/minute.
- Gold/minute.
- CS/minute.
- Vision/minute.
- Objective contribution.
- Death rate (negative contribution).
- Role-specific weights.

Provide the score components and allow weights to be changed. Compare only similar roles, queues, and patches where possible.

## 19.4 Consistency and form
- Mean, median, standard deviation, and interquartile range.
- Rolling 5 / 10 / 20-game metrics.
- Best / worst 5-, 10-, and 20-game periods.
- Win rate volatility.
- Performance after wins versus losses.
- Performance by session game number.
- Champion-specific consistency.
- Performance percentile against own history.

## 19.5 Statistical significance and fairness
- Minimum sample thresholds.
- Confidence intervals for win rates.
- Sample-size labels on all rankings.
- Role / queue / patch stratification.
- Avoid comparing raw averages from very different match lengths.
- Avoid ranking builds or runes based on tiny samples.
- Consider opponent and team context before interpreting individual performance.

---

# 20. Match explorer — individual match report

## 20.1 Match header
- Date and time.
- Match ID.
- Queue / game mode / map.
- Patch and game version.
- Duration.
- Result.
- Champion and role.
- Timeline availability indicator.

## 20.2 Tracked-player performance
- Full participant statistics.
- KDA and kill participation.
- Damage breakdown.
- Gold and farming.
- Vision.
- Healing, shielding, mitigation, crowd control.
- Objectives.
- Runes and shards.
- Summoner spells and casts.
- Ability casts.
- Final items.
- Pings.
- AFK / surrender flags.
- Challenges and missions.

## 20.3 Ten-player scoreboard
For every participant:
- Riot ID (if retained).
- Team and participant ID.
- Champion and role.
- K/D/A and KDA.
- Damage dealt to champions.
- Damage taken.
- Gold.
- CS and jungle CS.
- Vision score.
- Healing / shielding.
- Crowd-control time.
- Final items.
- Runes.
- Summoner spells.
- Within-team and lobby rankings for selected metrics.

## 20.4 Team comparison
- Team kills, gold, damage, CS, vision.
- Objective totals.
- Team gold / damage / kill differences.
- Player contribution charts.
- Team performance versus opponent.

## 20.5 Timeline replay-style report
- Gold / XP / CS progression.
- Level progression.
- Kill / death / assist events.
- Objective events.
- Ward events.
- Item purchases.
- Skill level-ups.
- Building destruction.
- Map event visualization.
- Filters by player, team, event type, and match time.

---

# 21. Additional data and limitations

## 21.1 Available now from match / participant data
The current participant and match tables support most end-of-game statistics: KDA, champion damage, gold, CS, vision, healing, shielding, crowd control, objectives, runes, final items, summoner spells, pings, champions, roles, patch, queue, and duration.

## 21.2 Available now from timeline frames
The current frame tables support time-series analysis of level, current / total gold, XP, minions, jungle minions, gold per second, crowd-control time, position, and nested champion / damage stats.

## 21.3 Available now from timeline events
The event table supports event-frequency analysis and, depending on each event's `event_data`, kill, objective, building, turret plate, item, ward, skill, and other event analysis.

## 21.4 Requires additional sources or richer event payloads
Potential future metrics:
- Exact item purchase order: requires item events with item IDs and participant IDs.
- Exact recall timing: requires recall events if provided.
- Damage dealt during a specific fight: generally requires more detailed combat telemetry than ordinary match timeline events.
- Gold / CS at exact timestamps: use nearest available frame; do not imply exact values between frames.
- Vision coverage / what a player could see: requires more than ward placement events and may not be reconstructable.
- Jungle pathing: requires sufficiently frequent position samples and / or monster events.
- Lane assignment: role fields can be unreliable; validate with early positions and matchup context.
- Rune effect contribution: rune selections alone do not provide rune-specific damage / healing values.
- Item completion timing: requires item purchase events and item metadata.
- True damage / mitigation source attribution: only possible if the nested damage payload contains the relevant breakdown.

## 21.5 Timeline event types are not a closed list
The event types above are a practical starting inventory, not a guarantee that every event exists in every match. Riot can vary event payloads by game mode, patch, and API version. The database should preserve raw events and unknown types. Generate a live event-type catalogue from the actual stored data before finalizing event-specific metrics.

---

# 22. Suggested dashboard navigation

1. Overview
2. Champions
3. Roles & Lanes
4. Combat
5. Damage & Durability
6. Farming & Economy
7. Vision
8. Runes
9. Items & Builds
10. Summoner Spells & Abilities
11. Teammates & Opponents
12. Objectives & Macro
13. Pings & Behavior
14. Game Modes & History
15. Arena & Augments
16. Challenges & Missions
17. Timeline Frames
18. Timeline Events
19. Advanced Analytics
20. Match Explorer

---

# 23. Suggested implementation order

## 23.1 Phase 1 — End-of-game foundation
- Overview.
- Match leaderboards.
- Champion and role statistics.
- KDA and combat.
- Damage.
- Farming and economy.
- Vision.

## 23.2 Phase 2 — Builds and comparisons
- Runes.
- Items.
- Summoner spells and abilities.
- Teammate / opponent analysis.
- Objectives.
- Patch and queue comparisons.

## 23.3 Phase 3 — Timeline progression
- Frame-based gold, XP, level, and CS.
- Lane matchup differences.
- Position charts and heatmaps.
- Timeline event inventory.
- Kill, ward, item, skill, and objective event analysis.

## 23.4 Phase 4 — Advanced analytics
- Rolling performance.
- Consistency.
- Correlations.
- Composite scores.
- Arena / augment analysis.
- Challenges and missions.
- Match explorer timeline.

---

## 24. Final data-quality checklist

Before trusting the dashboards, validate:
- [ ] `participants_df` contains only the tracked player's rows.
- [ ] `all_participants_df` contains the tracked player exactly once per match, plus the other participants.
- [ ] Participant and team IDs are consistent within each match.
- [ ] Team totals are not duplicated by joins.
- [ ] Match duration units are consistent.
- [ ] Timestamp units and timezone interpretation are confirmed.
- [ ] Timeline frames are ordered and frame intervals are checked.
- [ ] Participant frame rows map to the correct participant IDs.
- [ ] `champion_stats`, `damage_stats`, `challenges`, and `missions` structures are inspected.
- [ ] `event_data` is inspected by event type.
- [ ] Unknown event types are retained.
- [ ] Missing values are not confused with zero.
- [ ] Queue / game mode categories are separated.
- [ ] Patch is included in relevant comparisons.
- [ ] Leaderboards show sample size and match context.
- [ ] Rates are normalized by match duration where appropriate.
- [ ] Small-sample win rates are clearly flagged.
