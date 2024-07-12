extraction_prompt = """
<instructions>
Version: 1.1
Workflow: Step 1 - Extract key information from the strategy text

- Identify the names of bosses mentioned in the <strategy_text> tags.
- For each boss, identify the distinct phases or sections of the fight.
- Extract key mechanics and abilities for each phase.
- Use <encounter>...</encounter> tags to wrap the extracted information for each boss and its phases.
- Extract the boss names, phases, abilities, mechanics, and strategy and wrap them in the following tags:
  - Boss names: <span class="boss">...</span>
  - Phases: <span class="phase">...</span>
  - Ability names: <span class="ability">...</span>
  - Ability descriptions: <span class="description">...</span>
  - Player actions to deal with abilities: <span class="strategy">...</span>
- Output the entire extracted information wrapped in <duty>...</duty> tags.
- Ignore any irrelevant or non-duty related information.
- The output format should follow this structure:
    <duty>
        <encounter>
            <span class="boss">Boss Name</span>
            <span class="phase">Phase 1</span>
            <span class="ability">Ability Name</span>: <span class="description">Brief description</span> with <span class="strategy">important mechanic information to deal with or mitigate action or mechanic</span>
            <span class="phase">Phase 2 (75% HP)</span>
            ...
        </encounter>
        <encounter>
            ...
        </encounter>
    </duty>

- If there are any issues with the input text, provide an error message wrapped in <error>...</error> tags.
</instructions>
"""

enhancement_prompt = """
<instructions>
Version: 1.1
Workflow: Step 2 - Enhance extracted information with emojis and formatting

- Analyze the provided <duty> text from the extraction step.
- Use the ffxiv_glossary to identify and add relevant emojis to abilities and mechanics.
- Add formatting tags to highlight important terms or phrases:
  • <em>...</em> for emphasis
  • <strong>...</strong> for strong emphasis
  • <span class="tankbuster">...</span> for tankbusters
  • <span class="raidwide">...</span> for party-wide damage and unavoidable AoEs
- Highlight abilities that require paying attention to the name with 
- Ensure the emojis and formatting tags enhance readability without cluttering the text.
- Use <span class="role-tank">...</span>, <span class="role-healer">...</span>, and <span class="role-dps">...</span> to highlight role-specific mechanics.
- Maintain the existing structure and tags from the extraction step.
- The output format should follow this structure:
<duty>
    <encounter>
        <span class="boss">Boss Name</span>
        <span class="phase">Phase 1</span>
            <span class="ability">Ability Name</span>: <span class="description">Brief description</span> with <span class="strategy">important mechanic information to deal with or mitigate action or mechanic</span>
        <span class="ability">Ability Name</span>: 🛡️ <span class="tankbuster">Tankbuster</span> Additional description if applicable
        ...
    </encounter>
    ...
</duty>
- If there are any issues with the input text, provide an error message wrapped in <error>...</error> tags.
</instructions>
"""

compilation_prompt = """
<instructions>
Version: 1.1
Workflow: Step 3 - Compile a concise, HUD-friendly summary
<instructions>
- Use the provided <strategy_text>...</strategy_text> as additional context to understand the overall flow and mechanics of the boss fight.
- Combine the enhanced bullet points into a final summary, using the strategy_text as a reference.
- Ensure the summary is concise, informative, and well-structured for easy reference during gameplay.
- Add any additional context or information necessary inside <span class="notes">...</span> tags.
- Format the summary for clear display in a HUD, ensuring readability at a glance.
- Use the following structure for the output summary:
<summary_text>
    <span class="boss">Boss Name</span><br>
        <span class="phase">Phase 1</span><br>
        - <span class="note">Important information</span><br>
        - <span class="ability">Ability Name</span>: [emoji] <span class="description>Description </span><span class="strategy">key action</span><br>
        - <span class="ability">Ability Name</span>: 🛡️ <span class="tankbuster">Tankbuster</span> Additional info<br>
        - <span class="ability">Ability Name</span>: 💥💥 <span class="raidwide">Party-wide AoE</span> Additional info<br>
    <span class="phase">Phase 2 (75% HP)</span><br>
        - ...<br>
    <br>
    <span class="boss">Next Boss Name</span><br>
    ...
</summary_text>
- Maintain the order of mechanics as they appear in the fight.
- Ensure proper indentation and line breaks for readability.
- Use <br> tags for line breaks and spacing.
- Use only the following span classes: boss, phase, note, ability, strategy, description, tankbuster, raidwide, role-tank, role-healer, role-dps.
- If there are any issues with the input text, provide an error message wrapped in <error>...</error> tags.
</instructions>
<example>
    <summary_text>
    <span class="boss">Oschon</span><br>
        <span class="phase">Phase 1</span><br>
        - <span class="note">The arena is surrounded by a dangerous 💥 AoE.</span><br>
        - <span class="ability">Sudden Downpour</span>: 💥💥 <span class="raidwide">Party-wide AoE</span>.<br>
        - <span class="ability">Trek Shot</span>: 📐 <span class="description">Wide frontal cone AoE</span>. <span class="strategy">🏃 Avoid cone.</span><br>
        - <span class="ability">Reproduce</span>: 👾 Summons untargetable <span class="ability">Oschon's Avatar</span> using 🟠 <span class="description">Swinging Draw attack</span>. <span class="strategy">🏃 Avoid AoEs.</span><br>
        - <span class="ability">Flinted Foehn</span>: 🤝 <span class="description">Multi-hit stack AoE</span>. <span class="strategy">🤝 Stack and split.</span><br>
        - <span class="ability">Soaring Minuet</span>: 🪓 <span class="tankbuster">270 degree frontal cleave</span>. <span class="strategy">🏃 Get behind boss.</span><br>
        - <span class="ability">The Arrow</span>: 🛡️ <span class="tankbuster">AoE tankbusters on all tanks.<br>
        - <span class="ability">Downhill</span>: 💥🟠 <span class="description>Circle AoEs combined with 💨 Climbing Shot knockback. </span><span class="strategy">🏃 Position with knockback to avoid avoid. </span><br>
        <br>
        <span class="phase">Phase 2</span><br>
        - <span class="ability">Lofty Peaks</span>: 🌐 Transitions to new arena, boss transforms.<br>
        - <span class="ability">Piton Pull</span>: 💥 <span class="description">Massive circular AoEs on two quadrants</span>. <span class="strategy">🏃 Avoid AoE quadrants.</span><br>
        - <span class="ability">Altitude</span>: 💥🟠 <span class="description">Delayed resolving green circle AoEs</span>. <span class="strategy">🏃 Get out after delay.</span><br>
        - <span class="ability">Wandering Shot</span>: 💥🟠 <span class="description">Massive circular AoE with 💨 knockback</span>. <span class="strategy">🏃 Avoid AoE and knockback.</span><br>
        - <span class="ability">The Arrow</span>: 🛡️ <span class="tankbuster">Large AoE tankbusters</span>.<br>
        - <span class="ability">Arrow Trail</span>: 💥📏<span class="description">Arrows traveling down columns</span> combined with 🟠 <span class="description">baited circle AoEs</span>. <span class="strategy">🏃 Avoid arrows and baits.</span><br>
        - <span class="ability">Downhill</span>: 💥🟠 <span class="description">Circle AoEs at edge</span> combined with 💨 <span class="description">Wandering Volley horizontal knockback</span>. <span class="strategy">🏃 Avoid AoEs and knockback.</span><br>
    </summary_text>
</example>

"""

final_check_and_polish = """
<instructions>
Version: 1.1
Workflow: Step 4 - Final Check and Polish
- Review the <summary_text> for consistency, readability, and HUD-appropriateness.
- Using the context in the <strategy_text>, ensure all key mechanics and abilities are included.
- Ensure all mechanics are described concisely and clearly.
- Verify that emojis and formatting enhance readability without cluttering the display.
- Check that any role-specific information is clearly marked.
- Confirm that the summary follows a logical flow matching the progression of the fight.
- Make any necessary adjustments to improve clarity and conciseness.
- If any critical information is missing, add it using the appropriate tags and formatting.
- Ensure there is enough detail to understand certain mechanics, especially those that are unique to the fight.
- If any issues are found or clarifications needed, make the necessary corrections. Return the updated <summary_text> with the changes.
- If no issues are found, return the <summary_text> unchanged with a confirmation message.
<emphasis>Be sure to output the final version in <summary_text> tags. The program that calls this function expects the final summary to be wrapped in these tags.</emphasis>
</instructions>
<example>
    <summary_text>
    <span class="boss">Oschon</span><br>
        <span class="phase">Phase 1</span><br>
        - <span class="note">The arena is surrounded by a dangerous 💥 AoE.</span><br>
        - <span class="ability">Sudden Downpour</span>: 💥💥 <span class="raidwide">Party-wide AoE</span>.<br>
        - <span class="ability">Trek Shot</span>: 📐 <span class="description">Wide frontal cone AoE</span>. <span class="strategy">🏃 Avoid cone.</span><br>
        - <span class="ability">Reproduce</span>: 👾 Summons untargetable <span class="ability">Oschon's Avatar</span> using 🟠 <span class="description">Swinging Draw attack</span>. <span class="strategy">🏃 Avoid AoEs.</span><br>
        - <span class="ability">Flinted Foehn</span>: 🤝 <span class="description">Multi-hit stack AoE</span>. <span class="strategy">🤝 Stack and split.</span><br>
        - <span class="ability">Soaring Minuet</span>: 🪓 <span class="tankbuster">270 degree frontal cleave</span>. <span class="strategy">🏃 Get behind boss.</span><br>
        - <span class="ability">The Arrow</span>: 🛡️ <span class="tankbuster">AoE tankbusters on all tanks.<br>
        - <span class="ability">Downhill</span>: 💥🟠 <span class="description>Circle AoEs combined with 💨 Climbing Shot knockback. </span><span class="strategy">🏃 Position with knockback to avoid avoid. </span><br>
        <br>
        <span class="phase">Phase 2</span><br>
        - <span class="ability">Lofty Peaks</span>: 🌐 Transitions to new arena, boss transforms.<br>
        - <span class="ability">Piton Pull</span>: 💥 <span class="description">Massive circular AoEs on two quadrants</span>. <span class="strategy">🏃 Avoid AoE quadrants.</span><br>
        - <span class="ability">Altitude</span>: 💥🟠 <span class="description">Delayed resolving green circle AoEs</span>. <span class="strategy">🏃 Get out after delay.</span><br>
        - <span class="ability">Wandering Shot</span>: 💥🟠 <span class="description">Massive circular AoE</span> with <span class="description">💨 knockback</span>. <span class="strategy">🏃 Avoid AoE and knockback.</span><br>
        - <span class="ability">The Arrow</span>: 🛡️ <span class="tankbuster">Large AoE tankbusters</span>.<br>
        - <span class="ability">Arrow Trail</span>: 💥📏<span class="description">Arrows traveling down columns</span> combined with 🟠 <span class="description">baited circle AoEs</span>. <span class="strategy">🏃 Avoid arrows and baits.</span><br>
        - <span class="ability">Downhill</span>: 💥🟠 <span class="description">Circle AoEs at edge</span> combined with 💨 <span class="description">Wandering Volley horizontal knockback</span>. <span class="strategy">🏃 Avoid AoEs and knockback.</span><br>
    </summary_text>
</example>
"""

glossary_prompt = """
<ffxiv_glossary>
Version: 1.1
<note>
This glossary should be referenced in all stages of the HUD creation process to ensure consistent terminology and emoji usage. When adding emojis to the HUD display, prioritize clarity and avoid cluttering the view.
</note>
## General Terms
- AoE: 💥 Area of Effect, damage covering an area
- Add: 👾 Additional enemy in a fight
- Buff/Debuff: 🌟 Beneficial / 🤢 Harmful status effect
- DPS: ⚔️ Damage Per Second (also a role)
- Mechanic: ⚙️ Specific rule or challenge in an encounter
- Pull: 🎣 Start an encounter with enemies
- Wipe: 💀 Entire party dies, resetting the encounter
- Move: 🏃 Adjust position to avoid damage
- Phase: 🔄 Distinct part of an encounter

## FFXIV-Specific Terms
- Limit Break: 💪 Powerful team ability
- Positionals:🧭 Attacks stronger from certain positions
- Provoke: 👊 Ability to force enemy attention

## Common Mechanics
- Cleave: 🪓 Wide frontal attack
- DPS Check: ⏱️ Phase requiring specific damage output
- Enrage: ⏳ Final phase/attack if DPS check fails
- Gaze: 👁️ Attack requiring facing away
- Knockback: 💨 Force pushing players away
- Stack: 🤝 Players group to split damage
- Spread: 🏃↔️🏃 Players move apart to avoid sharing damage
- Tank Swap: 🛡️🔁 Tanks exchange enemy attention
- Edge mechanic: 👁️🔍 Watch the arena edge for attacks/effects
- Tankbuster: 🛡️ Powerful attack targeting the main tank
- Party-wide AoE/Raid-wide AoE: 💥💥 Damage affecting the entire party
- AoE Types: 
    • Cone: 💥📐 Triangular-shaped area
    • Line: 💥📏 Narrow, straight-line area
    • Proximity: 💥🎯 Damage decreases with distance
    • Donut AoE: 💥🍩 Damage inside and outside with safe spot in the middle
- Vulnerability Up: 🤮⬆️ Debuff increasing damage taken
- Ultimate: ☠️ Extremely powerful attack, often party-wide

## Roles
- Tank: 🛡️ Damage-absorbing role
  • Main Tank (MT): 🛡️1️⃣ Primary enemy target
  • Off Tank (OT): 🛡️2️⃣ Secondary tank, handles mechanics
- Healer: 💚 Restores HP and removes debuffs
- DPS: ⚔️ Damage-dealing role

## Markers and Tells
- Stack marker: 🤝 Circular marker with inward arrows
- AoE telegraph: 🟠⚠️ Visual indicator on ground
- Tether: 🔗 Line connecting entities
- Telegraph: ⚠️ Visual indicator of upcoming attack

## Positioning
- Safe spot: 💠 Area that avoids damage
- Danger zone: ⚠️ Area that will receive damage/effects
- Kite: 🪁 Lead an enemy around without engaging directly

## Instructions
- "Watch for the message": 👀 Pay attention to on-screen text
- Highlight key mechanics with associated symbols
- Display role-specific information clearly
</ffxiv_glossary>
"""
