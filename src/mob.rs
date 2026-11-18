use crate::{
    player::{Player, Vec3},
    world::World,
};

#[derive(Clone, Copy)]
pub enum MobKind {
    Pig,
    Zombie,
    Aegis,
}

pub struct Mob {
    pub kind: MobKind,
    pub position: Vec3,
    phase: f32,
}

impl Mob {
    pub fn spawn_near_player(world: &World, player: &Player) -> Vec<Self> {
        let offsets = [
            (-6.0, -9.0),
            (5.0, -13.0),
            (9.0, -4.0),
            (-10.0, -3.0),
            (3.0, 8.0),
            (-5.0, 12.0),
        ];
        offsets
            .iter()
            .enumerate()
            .map(|(index, (dx, dz))| {
                let x = (player.position.x + dx).round() as i32;
                let z = (player.position.z + dz).round() as i32;
                let y = world.surface_height(x, z) as f32 + 1.0;
                Self {
                    kind: match index % 3 {
                        0 => MobKind::Pig,
                        1 => MobKind::Zombie,
                        _ => MobKind::Aegis,
                    },
                    position: Vec3::new(x as f32 + 0.5, y, z as f32 + 0.5),
                    phase: index as f32,
                }
            })
            .collect()
    }

    pub fn update(&mut self, world: &World, dt: f32) {
        self.phase += dt;
        if self.phase > 5.0 {
            self.phase = 0.0;
            let dx = ((self.position.x as i32 * 13 + self.position.z as i32 * 7) % 3 - 1) as f32;
            let dz = ((self.position.x as i32 * 3 + self.position.z as i32 * 11) % 3 - 1) as f32;
            let x = (self.position.x + dx).round() as i32;
            let z = (self.position.z + dz).round() as i32;
            self.position.x = x as f32 + 0.5;
            self.position.z = z as f32 + 0.5;
            self.position.y = world.surface_height(x, z) as f32 + 1.0;
        }
    }

    pub fn color(&self) -> u32 {
        match self.kind {
            MobKind::Pig => 0xFFFFA6B2,
            MobKind::Zombie => 0xFF438B4F,
            MobKind::Aegis => 0xFFB7D9F0,
        }
    }
}
