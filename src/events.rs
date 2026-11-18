use crate::world::{World, STONE, WATER};

pub struct WorldEvents {
    pub flood_active: bool,
    warning_ticks: i32,
    pub messages: Vec<String>,
}

impl Default for WorldEvents {
    fn default() -> Self {
        Self {
            flood_active: false,
            warning_ticks: 0,
            messages: Vec::new(),
        }
    }
}

impl WorldEvents {
    pub fn start_flood(&mut self) -> String {
        self.flood_active = true;
        self.warning_ticks = 30;
        "Build an ark - Noah's Flood begins in 30 seconds.".to_string()
    }

    pub fn stop_flood(&mut self) -> String {
        self.flood_active = false;
        self.warning_ticks = 0;
        "Noah's Flood stopped.".to_string()
    }

    pub fn status(&self) -> String {
        if self.flood_active {
            format!("Noah's Flood: {} seconds remaining.", self.warning_ticks)
        } else {
            "Noah's Flood is stopped.".to_string()
        }
    }

    pub fn update(&mut self, world: &mut World) {
        if !self.flood_active {
            return;
        }
        if self.warning_ticks > 0 {
            self.warning_ticks -= 1;
            return;
        }
        for z in 1..world.length - 1 {
            for y in 1..world.height - 1 {
                for x in 1..world.width - 1 {
                    let block = world.get_block(x as i32, y as i32, z as i32);
                    if block == STONE || block == crate::world::DIRT || block == crate::world::GRASS
                    {
                        world.set_block(x as i32, y as i32, z as i32, AIR);
                    }
                    if block == AIR {
                        world.set_block(x as i32, y as i32, z as i32, WATER);
                    }
                }
            }
        }
        self.messages.push("The rain begins.".to_string());
        self.flood_active = false;
    }
}

use crate::world::AIR;
