# World Circuit Passport Johto Unlock Design

## Intent

After Champion Blue falls, Kanto should not end with a menu jump. Oak must convert Antman's Hall of Fame proof into a real travel credential, then WorldLink opens Johto as the next committed region. This keeps WorldLink as a story route, not a fast-travel selector.

## Player-Facing Flow

Oak's Lab becomes the post-credits handoff. When Antman speaks to Oak after `FLAG_SYS_GAME_CLEAR`, Oak checks whether the World Circuit Passport has already been awarded. If not, he confirms the Hall of Fame record, gives the World Circuit Passport, and explains that Red, Misty, and Brock are waiting at the World Circuit Gate.

Johto becomes live only after this ceremony. Lyra's profile changes from locked preview to a live New Bark Town contact, giving the next region a human face before the player departs.

## Scope

This slice adds the passport flag, Oak Lab ceremony, WorldLink unlock messages, Act 7 event data, rival/companion notifications, and smoke-test coverage. It does not build the Johto map, New Bark arrival, full World Circuit Gate map, or Johto trainer teams; those are the next slices.
