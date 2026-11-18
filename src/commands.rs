pub fn execute(command: &str) -> String {
    let command = command.trim().trim_start_matches('/');
    let mut parts = command.split_whitespace();
    match parts.next().unwrap_or_default() {
        "gamemode" => match parts.next() {
            Some("c") => "Gamemode changed to creative.".to_string(),
            Some("s") => "Gamemode changed to survival.".to_string(),
            _ => "Usage: /gamemode c|s".to_string(),
        },
        "heal" => "Healed the player.".to_string(),
        "clear" => "Inventory cleared.".to_string(),
        "time" => "Time set.".to_string(),
        "give" => format!("Gave {}.", parts.next().unwrap_or("item")),
        "spawn" => format!("Spawned {}.", parts.next().unwrap_or("entity")),
        "tp" | "teleport" => "Teleported.".to_string(),
        "help" => {
            "Commands: /gamemode, /give, /spawn, /tp, /heal, /clear, /time, /flood".to_string()
        }
        "flood" => "Use the Flood controls in-game.".to_string(),
        _ => format!("Unknown command: /{}", command),
    }
}
