use serde::{Deserialize, Serialize};

pub const AIR: u8 = 0;
pub const STONE: u8 = 1;
pub const GRASS: u8 = 2;
pub const DIRT: u8 = 3;
pub const WATER: u8 = 4;
pub const SAND: u8 = 5;
pub const WOOD: u8 = 6;
pub const LEAF: u8 = 7;
pub const BEDROCK: u8 = 8;
pub const TNT: u8 = 9;
pub const LUCKY: u8 = 10;

#[derive(Clone, Serialize, Deserialize)]
pub struct World {
    pub width: usize,
    pub height: usize,
    pub length: usize,
    pub water_level: usize,
    blocks: Vec<u8>,
    pub ticks: u64,
}

impl World {
    pub fn new(width: usize, height: usize, length: usize) -> Self {
        let mut world = Self {
            width,
            height,
            length,
            water_level: height / 4,
            blocks: vec![AIR; width * height * length],
            ticks: 0,
        };
        world.generate();
        world
    }

    pub fn index(&self, x: i32, y: i32, z: i32) -> Option<usize> {
        if x < 0 || y < 0 || z < 0 {
            return None;
        }
        let (x, y, z) = (x as usize, y as usize, z as usize);
        if x >= self.width || y >= self.height || z >= self.length {
            return None;
        }
        Some(x + z * self.width + y * self.width * self.length)
    }

    pub fn get_block(&self, x: i32, y: i32, z: i32) -> u8 {
        self.index(x, y, z)
            .map(|i| self.blocks[i])
            .unwrap_or(BEDROCK)
    }

    pub fn set_block(&mut self, x: i32, y: i32, z: i32, block: u8) -> bool {
        if let Some(i) = self.index(x, y, z) {
            self.blocks[i] = block;
            true
        } else {
            false
        }
    }

    pub fn is_solid(&self, x: i32, y: i32, z: i32) -> bool {
        matches!(
            self.get_block(x, y, z),
            STONE | GRASS | DIRT | SAND | WOOD | LEAF | BEDROCK | TNT | LUCKY
        )
    }

    fn generate(&mut self) {
        for z in 0..self.length {
            for x in 0..self.width {
                let dx = (x as f32 - self.width as f32 / 2.0) / 13.0;
                let dz = (z as f32 - self.length as f32 / 2.0) / 13.0;
                let hills =
                    (dx.sin() * 3.0 + dz.cos() * 2.5 + ((x * 5 + z * 3) % 7) as f32 * 0.22) as i32;
                let surface =
                    (self.height as i32 / 4 + hills).clamp(5, self.height as i32 - 10) as usize;

                for y in 0..surface {
                    let block = if y == 0 {
                        BEDROCK
                    } else if y + 3 >= surface {
                        if surface <= self.water_level + 2 {
                            SAND
                        } else {
                            GRASS
                        }
                    } else {
                        STONE
                    };
                    let i = x + z * self.width + y * self.width * self.length;
                    self.blocks[i] = block;
                }

                for y in surface..self.water_level {
                    let i = x + z * self.width + y * self.width * self.length;
                    self.blocks[i] = WATER;
                }
            }
        }

        for z in 3..self.length - 3 {
            for x in 3..self.width - 3 {
                if (x * 17 + z * 29) % 97 == 0 {
                    let mut y = self.surface_height(x as i32, z as i32) as i32;
                    if self.get_block(x as i32, y as i32, z as i32) == GRASS {
                        y += 1;
                        for dy in 0..5 {
                            self.set_block(x as i32, y + dy, z as i32, WOOD);
                        }
                        for oy in 3i32..6 {
                            for oz in -2i32..=2 {
                                for ox in -2i32..=2 {
                                    if ox.abs() + oz.abs() + (oy - 4).abs() < 5 {
                                        self.set_block(x as i32 + ox, y + oy, z as i32 + oz, LEAF);
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    pub fn surface_height(&self, x: i32, z: i32) -> usize {
        for y in (0..self.height).rev() {
            if self.is_solid(x, y as i32, z) {
                return y;
            }
        }
        0
    }

    pub fn tick(&mut self) {
        self.ticks = self.ticks.wrapping_add(1);
    }

    pub fn save(&self, path: &std::path::Path) -> Result<(), String> {
        let json = serde_json::to_vec(self).map_err(|e| e.to_string())?;
        std::fs::write(path, json).map_err(|e| e.to_string())
    }

    pub fn load(path: &std::path::Path) -> Result<Self, String> {
        let json = std::fs::read(path).map_err(|e| e.to_string())?;
        serde_json::from_slice(&json).map_err(|e| e.to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn world_generation_has_bedrock_and_a_surface() {
        let world = World::new(16, 32, 16);
        assert_eq!(world.get_block(8, 0, 8), BEDROCK);
        assert!(world.surface_height(8, 8) > 0);
    }

    #[test]
    fn out_of_bounds_is_blocked() {
        let mut world = World::new(8, 16, 8);
        assert_eq!(world.get_block(-1, 1, 1), BEDROCK);
        assert!(!world.set_block(99, 1, 1, STONE));
    }
}
