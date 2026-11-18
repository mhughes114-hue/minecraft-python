use crate::world::World;
use std::ops::{Add, Mul};

#[derive(Clone, Copy, Default)]
pub struct Vec3 {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Vec3 {
    pub const fn new(x: f32, y: f32, z: f32) -> Self {
        Self { x, y, z }
    }

    pub fn normalize(self) -> Self {
        let length = (self.x * self.x + self.y * self.y + self.z * self.z).sqrt();
        if length > 0.0 {
            self * (1.0 / length)
        } else {
            self
        }
    }

    pub fn scale(self, rhs: f32) -> Self {
        Self::new(self.x * rhs, self.y * rhs, self.z * rhs)
    }

    pub fn add(self, rhs: Self) -> Self {
        Self::new(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
    }

    pub fn sub(self, rhs: Self) -> Self {
        Self::new(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
    }

    pub fn dot(self, rhs: Self) -> f32 {
        self.x * rhs.x + self.y * rhs.y + self.z * rhs.z
    }

    pub fn cross(self, rhs: Self) -> Self {
        Self::new(
            self.y * rhs.z - self.z * rhs.y,
            self.z * rhs.x - self.x * rhs.z,
            self.x * rhs.y - self.y * rhs.x,
        )
    }
}

impl Add for Vec3 {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Self::new(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
    }
}

impl Mul<f32> for Vec3 {
    type Output = Self;
    fn mul(self, rhs: f32) -> Self {
        Self::new(self.x * rhs, self.y * rhs, self.z * rhs)
    }
}

#[derive(Clone)]
pub struct Player {
    pub position: Vec3,
    pub yaw: f32,
    pub pitch: f32,
    pub velocity_y: f32,
    pub grounded: bool,
    pub health: i32,
    pub debt: i64,
    pub selected_slot: usize,
}

impl Player {
    pub fn spawn(world: &World) -> Self {
        let x = world.width as f32 / 2.0;
        let z = world.length as f32 / 2.0;
        let surface = (x as i32 - 1..=x as i32 + 1)
            .flat_map(|surface_x| {
                (z as i32 - 1..=z as i32 + 1)
                    .map(move |surface_z| world.surface_height(surface_x, surface_z))
            })
            .max()
            .unwrap_or(0);
        let y = surface as f32 + 2.62;
        Self {
            position: Vec3::new(x, y, z),
            yaw: 0.0,
            pitch: 0.0,
            velocity_y: 0.0,
            grounded: false,
            health: 20,
            debt: 0,
            selected_slot: 0,
        }
    }

    pub fn aabb(&self) -> (Vec3, Vec3) {
        (
            Vec3::new(
                self.position.x - 0.32,
                self.position.y - 1.62,
                self.position.z - 0.32,
            ),
            Vec3::new(
                self.position.x + 0.32,
                self.position.y + 0.18,
                self.position.z + 0.32,
            ),
        )
    }

    pub fn collides(&self, world: &World) -> bool {
        let (min, max) = self.aabb();
        let x0 = min.x.floor() as i32;
        let x1 = max.x.floor() as i32;
        let y0 = min.y.floor() as i32;
        let y1 = max.y.floor() as i32;
        let z0 = min.z.floor() as i32;
        let z1 = max.z.floor() as i32;
        for y in y0..=y1 {
            for z in z0..=z1 {
                for x in x0..=x1 {
                    if world.is_solid(x, y, z) {
                        return true;
                    }
                }
            }
        }
        false
    }

    pub fn tick(&mut self, world: &World, move_x: f32, move_z: f32, jump: bool) {
        let yaw = self.yaw;
        let forward = Vec3::new(-yaw.sin(), 0.0, -yaw.cos()).normalize();
        let right = Vec3::new(yaw.cos(), 0.0, -yaw.sin()).normalize();
        let speed = 4.8;
        let desired = (forward * move_z + right * move_x) * speed;

        let dt = 1.0 / 60.0;
        let mut next = self.position;
        next.x += desired.x * dt;
        if !self.with_position_collides(world, next) {
            self.position.x = next.x;
        }

        next = self.position;
        next.z += desired.z * dt;
        if !self.with_position_collides(world, next) {
            self.position.z = next.z;
        }

        if jump && self.grounded {
            self.velocity_y = 7.4;
        }
        self.velocity_y -= 20.0 * dt;

        next = self.position;
        next.y += self.velocity_y * dt;
        if self.with_position_collides(world, next) {
            self.grounded = self.velocity_y < 0.0;
            self.velocity_y = 0.0;
        } else {
            self.grounded = false;
            self.position.y = next.y;
        }

        if world.ticks % 20 == 0 {
            self.debt = self.debt.saturating_sub(1);
        }
    }

    fn with_position_collides(&self, world: &World, position: Vec3) -> bool {
        let old = self.position;
        let mut copy = self.clone();
        copy.position = position;
        copy.position = position;
        let result = copy.collides(world);
        let _ = old;
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn spawned_player_is_above_the_ground_and_can_walk() {
        let world = World::new(32, 32, 32);
        let mut player = Player::spawn(&world);
        let start_z = player.position.z;

        assert!(!player.collides(&world));
        player.tick(&world, 0.0, 1.0, false);
        assert!(player.position.z < start_z);
    }
}
