mod commands;
mod events;
mod mob;
mod player;
mod world;

use mob::Mob;
use player::{Player, Vec3};
use softbuffer::{Context, Surface};
use std::collections::HashSet;
use std::num::NonZeroU32;
use std::sync::Arc;
use std::time::{Duration, Instant};
use winit::{
    application::ApplicationHandler,
    event::{ElementState, KeyEvent, MouseButton, WindowEvent},
    event_loop::{ActiveEventLoop, ControlFlow, EventLoop},
    keyboard::{KeyCode, PhysicalKey},
    window::{Window, WindowAttributes},
};
use world::{World, AIR, BEDROCK, DIRT, GRASS, LEAF, LUCKY, SAND, STONE, TNT, WATER, WOOD};

const HOTBAR: [u8; 7] = [GRASS, DIRT, STONE, WOOD, SAND, TNT, LUCKY];

struct App {
    window: Option<Arc<Window>>,
    surface: Option<Surface<Arc<Window>, Arc<Window>>>,
    world: World,
    player: Player,
    events: events::WorldEvents,
    keys: HashSet<KeyCode>,
    cursor: Option<(f32, f32)>,
    last_frame: Instant,
    width: u32,
    height: u32,
    textures: TerrainTextures,
    mobs: Vec<Mob>,
    screen: Screen,
    inventory: [u8; 27],
    hotbar: [u8; 7],
    left_mouse_down: bool,
    break_progress: f32,
    break_target: Option<(i32, i32, i32)>,
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Screen {
    Title,
    Playing,
    Paused,
    Inventory,
}

impl App {
    fn new() -> Self {
        let world = World::new(96, 48, 96);
        let player = Player::spawn(&world);
        let mobs = Mob::spawn_near_player(&world, &player);
        Self {
            window: None,
            surface: None,
            world,
            player,
            events: events::WorldEvents::default(),
            keys: HashSet::new(),
            cursor: None,
            last_frame: Instant::now(),
            width: 960,
            height: 540,
            textures: TerrainTextures::load(),
            mobs,
            screen: Screen::Title,
            inventory: [
                GRASS, DIRT, STONE, WOOD, SAND, TNT, LUCKY, STONE, DIRT, STONE, DIRT, SAND, WOOD,
                LEAF, GRASS, STONE, DIRT, WOOD, SAND, STONE, GRASS, DIRT, STONE, WOOD, SAND, DIRT,
                STONE,
            ],
            hotbar: HOTBAR,
            left_mouse_down: false,
            break_progress: 0.0,
            break_target: None,
        }
    }

    fn update(&mut self) {
        let now = Instant::now();
        let elapsed = (now - self.last_frame).min(Duration::from_millis(50));
        self.last_frame = now;
        let dt = elapsed.as_secs_f32();
        if self.screen != Screen::Playing {
            return;
        }
        self.world.tick();
        if self.left_mouse_down {
            if let Some((target, _)) = raycast(&self.world, &self.player, 6.0) {
                if self.break_target != Some(target) {
                    self.break_target = Some(target);
                    self.break_progress = 0.0;
                }
                if self.world.get_block(target.0, target.1, target.2) == BEDROCK {
                    self.break_progress = 0.0;
                } else {
                    self.break_progress += dt / 0.8;
                    if self.break_progress >= 1.0 {
                        self.world.set_block(target.0, target.1, target.2, AIR);
                        self.break_progress = 0.0;
                        self.break_target = None;
                    }
                }
            } else {
                self.break_target = None;
                self.break_progress = 0.0;
            }
        } else {
            self.break_target = None;
            self.break_progress = 0.0;
        }

        let move_x = if self.keys.contains(&KeyCode::KeyD) {
            1.0
        } else if self.keys.contains(&KeyCode::KeyA) {
            -1.0
        } else {
            0.0
        };
        let move_z = if self.keys.contains(&KeyCode::KeyW) {
            1.0
        } else if self.keys.contains(&KeyCode::KeyS) {
            -1.0
        } else {
            0.0
        };
        let jump = self.keys.contains(&KeyCode::Space);

        let yaw = self.player.yaw;
        let forward = Vec3::new(-yaw.sin(), 0.0, -yaw.cos()).normalize();
        let right = Vec3::new(yaw.cos(), 0.0, -yaw.sin()).normalize();
        let desired = forward.scale(move_z).add(right.scale(move_x)).scale(4.8);
        self.player.position.x += desired.x * dt;
        if self.player.collides(&self.world) {
            self.player.position.x -= desired.x * dt;
        }
        self.player.position.z += desired.z * dt;
        if self.player.collides(&self.world) {
            self.player.position.z -= desired.z * dt;
        }
        if jump && self.player.grounded {
            self.player.velocity_y = 7.4;
        }
        self.player.velocity_y -= 20.0 * dt;
        self.player.position.y += self.player.velocity_y * dt;
        if self.player.collides(&self.world) {
            self.player.position.y -= self.player.velocity_y * dt;
            self.player.grounded = self.player.velocity_y < 0.0;
            self.player.velocity_y = 0.0;
        } else {
            self.player.grounded = false;
        }

        self.events.update(&mut self.world);
        for mob in &mut self.mobs {
            mob.update(&self.world, dt);
        }
    }

    fn render(&mut self) {
        let Some(surface) = self.surface.as_mut() else {
            return;
        };
        let width = (self.width / 2).max(320);
        let height = (self.height / 2).max(180);
        let nw = NonZeroU32::new(width).unwrap();
        let nh = NonZeroU32::new(height).unwrap();
        let _ = surface.resize(nw, nh);

        let mut pixels = vec![0u32; (width * height) as usize];
        let mut depth = vec![f32::INFINITY; (width * height) as usize];
        let sky = 0xFF78_B6F4;
        pixels.fill(sky);

        let cx = self.player.position.x as i32;
        let cy = self.player.position.y as i32;
        let cz = self.player.position.z as i32;
        let range = 24;
        for y in (0i32.max(cy - range))..(self.world.height as i32).min(cy + range) {
            for z in (0i32.max(cz - range))..(self.world.length as i32).min(cz + range) {
                for x in (0i32.max(cx - range))..(self.world.width as i32).min(cx + range) {
                    let block = self.world.get_block(x, y, z);
                    if block == AIR || block == WATER {
                        continue;
                    }
                    draw_cube(
                        &mut pixels,
                        &mut depth,
                        width as usize,
                        height as usize,
                        &self.player,
                        &self.textures,
                        x,
                        y,
                        z,
                        block,
                    );
                }
            }
        }

        for mob in &self.mobs {
            draw_mob(
                &mut pixels,
                &mut depth,
                width as usize,
                height as usize,
                &self.player,
                mob,
            );
        }

        match self.screen {
            Screen::Title => draw_menu(
                &mut pixels,
                width as usize,
                height as usize,
                "MINECRAFT",
                "PLAY",
                "QUIT",
            ),
            Screen::Paused => draw_menu(
                &mut pixels,
                width as usize,
                height as usize,
                "PAUSED",
                "RESUME",
                "TITLE",
            ),
            Screen::Inventory => draw_inventory(
                &mut pixels,
                width as usize,
                height as usize,
                &self.inventory,
                &self.hotbar,
                self.player.selected_slot,
                &self.textures,
            ),
            Screen::Playing => {
                draw_crosshair(&mut pixels, width as usize, height as usize);
                draw_break_animation(
                    &mut pixels,
                    width as usize,
                    height as usize,
                    self.break_progress,
                );
                draw_hotbar(
                    &mut pixels,
                    width as usize,
                    height as usize,
                    &self.hotbar,
                    self.player.selected_slot,
                    &self.textures,
                );
                draw_first_person_hand(
                    &mut pixels,
                    width as usize,
                    height as usize,
                    self.hotbar[self.player.selected_slot],
                    &self.textures,
                    self.left_mouse_down,
                );
            }
        }

        if let Ok(mut buffer) = surface.buffer_mut() {
            buffer.copy_from_slice(&pixels);
            let _ = buffer.present();
        }
    }
}

impl ApplicationHandler for App {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.window.is_some() {
            return;
        }
        let attributes = WindowAttributes::default()
            .with_title("Minecraft: Rust Edition")
            .with_inner_size(winit::dpi::PhysicalSize::new(1280u32, 720u32));
        let window = Arc::new(event_loop.create_window(attributes).unwrap());
        let context = Context::new(window.clone()).unwrap();
        let surface = Surface::new(&context, window.clone()).unwrap();
        self.width = window.inner_size().width;
        self.height = window.inner_size().height;
        self.window = Some(window);
        self.surface = Some(surface);
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _id: winit::window::WindowId,
        event: WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => event_loop.exit(),
            WindowEvent::Resized(size) => {
                self.width = size.width;
                self.height = size.height;
            }
            WindowEvent::KeyboardInput {
                event:
                    KeyEvent {
                        physical_key,
                        state,
                        ..
                    },
                ..
            } => {
                if let PhysicalKey::Code(code) = physical_key {
                    if state == ElementState::Pressed {
                        if code == KeyCode::Escape {
                            self.screen = match self.screen {
                                Screen::Playing => Screen::Paused,
                                Screen::Paused | Screen::Inventory => Screen::Playing,
                                Screen::Title => Screen::Playing,
                            };
                            self.cursor = None;
                        } else if code == KeyCode::Enter && self.screen == Screen::Title {
                            self.screen = Screen::Playing;
                            self.cursor = None;
                        } else if code == KeyCode::KeyI {
                            self.screen = match self.screen {
                                Screen::Playing => Screen::Inventory,
                                Screen::Inventory => Screen::Playing,
                                other => other,
                            };
                            self.cursor = None;
                        }
                        if self.screen != Screen::Playing {
                            self.keys.remove(&code);
                            return;
                        }
                        self.keys.insert(code);
                        if code == KeyCode::Digit1 {
                            self.player.selected_slot = 0;
                        }
                        if code == KeyCode::Digit2 {
                            self.player.selected_slot = 1;
                        }
                        if code == KeyCode::Digit3 {
                            self.player.selected_slot = 2;
                        }
                        if code == KeyCode::Digit4 {
                            self.player.selected_slot = 3;
                        }
                        if code == KeyCode::Digit5 {
                            self.player.selected_slot = 4;
                        }
                        if code == KeyCode::Digit6 {
                            self.player.selected_slot = 5;
                        }
                        if code == KeyCode::Digit7 {
                            self.player.selected_slot = 6;
                        }
                        if code == KeyCode::F5 {
                            let _ = self.world.save(std::path::Path::new("world.json"));
                        }
                        if code == KeyCode::F9 {
                            if let Ok(world) = World::load(std::path::Path::new("world.json")) {
                                self.world = world;
                                self.player = Player::spawn(&self.world);
                            }
                        }
                    } else {
                        self.keys.remove(&code);
                    }
                }
            }
            WindowEvent::CursorMoved { position, .. } => {
                let position = (position.x as f32, position.y as f32);
                if self.screen == Screen::Playing {
                    if let Some(previous) = self.cursor {
                        apply_mouse_look(
                            &mut self.player,
                            position.0 - previous.0,
                            position.1 - previous.1,
                        );
                    }
                }
                self.cursor = Some(position);
            }
            WindowEvent::MouseInput { state, button, .. } => {
                if button == MouseButton::Left {
                    if state == ElementState::Pressed && self.screen == Screen::Playing {
                        self.left_mouse_down = true;
                    } else if state == ElementState::Released {
                        self.left_mouse_down = false;
                    }
                }
                if state != ElementState::Pressed {
                    return;
                }
                let Some((mouse_x, mouse_y)) = self.cursor else {
                    return;
                };
                let x = mouse_x / 2.0;
                let y = mouse_y / 2.0;
                match self.screen {
                    Screen::Title => {
                        if menu_button_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                            0,
                        ) {
                            self.screen = Screen::Playing;
                            self.cursor = None;
                        } else if menu_button_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                            1,
                        ) {
                            event_loop.exit();
                        }
                    }
                    Screen::Paused => {
                        if menu_button_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                            0,
                        ) {
                            self.screen = Screen::Playing;
                            self.cursor = None;
                        } else if menu_button_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                            1,
                        ) {
                            self.screen = Screen::Title;
                            self.cursor = None;
                        }
                    }
                    Screen::Inventory => {
                        if let Some(slot) = inventory_hotbar_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                        ) {
                            self.player.selected_slot = slot.min(self.hotbar.len() - 1);
                            self.screen = Screen::Playing;
                        } else if let Some(slot) = inventory_item_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                        ) {
                            self.hotbar[self.player.selected_slot] = self.inventory[slot];
                            self.screen = Screen::Playing;
                        } else if menu_button_hit(
                            x,
                            y,
                            self.width as usize / 2,
                            self.height as usize / 2,
                            0,
                        ) {
                            self.screen = Screen::Playing;
                        }
                    }
                    Screen::Playing => {
                        if button == MouseButton::Left || button == MouseButton::Right {
                            let placement = button == MouseButton::Right;
                            if let Some((target, previous)) =
                                raycast(&self.world, &self.player, 6.0)
                            {
                                let position = if placement {
                                    previous.unwrap_or(target)
                                } else {
                                    target
                                };
                                if placement {
                                    self.world.set_block(
                                        position.0,
                                        position.1,
                                        position.2,
                                        self.hotbar[self.player.selected_slot],
                                    );
                                }
                            }
                        }
                    }
                }
            }
            WindowEvent::RedrawRequested => {
                self.update();
                self.render();
            }
            _ => {}
        }
    }

    fn about_to_wait(&mut self, event_loop: &ActiveEventLoop) {
        let _ = event_loop;
        if let Some(window) = &self.window {
            window.request_redraw();
        }
    }
}

fn main() {
    let event_loop = EventLoop::new().unwrap();
    event_loop.set_control_flow(ControlFlow::Poll);
    event_loop.run_app(&mut App::new()).unwrap();
}

fn apply_mouse_look(player: &mut Player, delta_x: f32, delta_y: f32) {
    player.yaw -= delta_x * 0.003;
    player.pitch = (player.pitch + delta_y * 0.003).clamp(-1.55, 1.55);
}

fn raycast(
    world: &World,
    player: &Player,
    reach: f32,
) -> Option<((i32, i32, i32), Option<(i32, i32, i32)>)> {
    let direction = Vec3::new(
        -player.yaw.sin() * player.pitch.cos(),
        -player.pitch.sin(),
        -player.yaw.cos() * player.pitch.cos(),
    )
    .normalize();
    let mut previous = None;
    let mut distance = 0.1;
    while distance <= reach {
        let point = player.position.add(direction.scale(distance));
        let position = (
            point.x.floor() as i32,
            point.y.floor() as i32,
            point.z.floor() as i32,
        );
        let block = world.get_block(position.0, position.1, position.2);
        if block != AIR && block != WATER {
            return Some((position, previous));
        }
        previous = Some(position);
        distance += 0.05;
    }
    None
}

fn menu_button_hit(x: f32, y: f32, width: usize, height: usize, index: usize) -> bool {
    let left = width as f32 * 0.5 - 60.0;
    let top = height as f32 * 0.5 + 15.0 + index as f32 * 42.0;
    (left..=left + 120.0).contains(&x) && (top..=top + 30.0).contains(&y)
}

fn draw_menu(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    title: &str,
    first: &str,
    second: &str,
) {
    for pixel in pixels.iter_mut() {
        *pixel = blend(*pixel, 0xD0000000);
    }
    let center_x = width as i32 / 2;
    let center_y = height as i32 / 2;
    draw_bitmap_text(
        pixels,
        width,
        height,
        title,
        center_x - title.len() as i32 * 4,
        center_y - 40,
        0xFFFFFFFF,
        2,
    );
    draw_menu_button(pixels, width, height, first, center_y + 15);
    draw_menu_button(pixels, width, height, second, center_y + 57);
    if title == "INVENTORY" {
        for i in 0..HOTBAR.len() {
            let x = center_x - 63 + i as i32 * 18;
            fill_rect(pixels, width, height, x, center_y - 8, 16, 16, 0xFF333333);
        }
    }
}

fn draw_menu_button(pixels: &mut [u32], width: usize, height: usize, label: &str, top: i32) {
    let left = width as i32 / 2 - 60;
    fill_rect(pixels, width, height, left, top, 120, 30, 0xFF606060);
    fill_rect(
        pixels,
        width,
        height,
        left + 2,
        top + 2,
        116,
        26,
        0xFF343434,
    );
    draw_bitmap_text(
        pixels,
        width,
        height,
        label,
        width as i32 / 2 - label.len() as i32 * 2,
        top + 12,
        0xFFFFFFFF,
        1,
    );
}

fn fill_rect(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    x: i32,
    y: i32,
    w: i32,
    h: i32,
    color: u32,
) {
    for py in y.max(0)..(y + h).min(height as i32) {
        for px in x.max(0)..(x + w).min(width as i32) {
            pixels[py as usize * width + px as usize] = color;
        }
    }
}

fn blend(background: u32, foreground: u32) -> u32 {
    let alpha = ((foreground >> 24) & 255) as u32;
    let inv = 255 - alpha;
    let channel = |shift: u32| {
        ((((foreground >> shift) & 255) * alpha + ((background >> shift) & 255) * inv) / 255) & 255
    };
    0xFF000000 | channel(16) << 16 | channel(8) << 8 | channel(0)
}

fn draw_bitmap_text(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    text: &str,
    x: i32,
    y: i32,
    color: u32,
    scale: i32,
) {
    let mut cursor_x = x;
    for character in text.chars() {
        if let Some(rows) = glyph(character) {
            for (row, bits) in rows.iter().enumerate() {
                for column in 0..3 {
                    if bits & (1 << (2 - column)) != 0 {
                        fill_rect(
                            pixels,
                            width,
                            height,
                            cursor_x + column * scale,
                            y + row as i32 * scale,
                            scale,
                            scale,
                            color,
                        );
                    }
                }
            }
        }
        cursor_x += 4 * scale;
    }
}

fn glyph(character: char) -> Option<[u8; 5]> {
    Some(match character {
        'A' => [2, 5, 7, 5, 5],
        'B' => [6, 5, 6, 5, 6],
        'C' => [3, 4, 4, 4, 3],
        'D' => [6, 5, 5, 5, 6],
        'E' => [7, 4, 6, 4, 7],
        'F' => [7, 4, 6, 4, 4],
        'G' => [3, 4, 5, 5, 3],
        'H' => [5, 5, 7, 5, 5],
        'I' => [7, 2, 2, 2, 7],
        'J' => [1, 1, 1, 5, 2],
        'K' => [5, 5, 6, 5, 5],
        'L' => [4, 4, 4, 4, 7],
        'M' => [5, 7, 7, 5, 5],
        'N' => [5, 7, 7, 7, 5],
        'O' => [2, 5, 5, 5, 2],
        'P' => [6, 5, 6, 4, 4],
        'Q' => [2, 5, 5, 7, 3],
        'R' => [6, 5, 6, 5, 5],
        'S' => [3, 4, 2, 1, 6],
        'T' => [7, 2, 2, 2, 2],
        'U' => [5, 5, 5, 5, 7],
        'V' => [5, 5, 5, 5, 2],
        'W' => [5, 5, 7, 7, 5],
        'X' => [5, 5, 2, 5, 5],
        'Y' => [5, 5, 2, 2, 2],
        'Z' => [7, 1, 2, 4, 7],
        ' ' => [0; 5],
        _ => return None,
    })
}

fn draw_mob(
    pixels: &mut [u32],
    depth: &mut [f32],
    width: usize,
    height: usize,
    player: &Player,
    mob: &Mob,
) {
    let Some((sx, sy, distance)) = project(
        player,
        mob.position.add(Vec3::new(0.0, 0.7, 0.0)),
        width,
        height,
    ) else {
        return;
    };
    if distance > 30.0 {
        return;
    }
    let unit = (height as f32 * 0.65 / distance).clamp(2.0, 42.0);
    let body_width = (unit * 0.7).round() as i32;
    let body_height = (unit * 0.8).round() as i32;
    let left = sx.round() as i32 - body_width / 2;
    let top = sy.round() as i32 - body_height / 2;
    let base_color = mob.color();
    draw_depth_rect(
        pixels,
        depth,
        width,
        height,
        left,
        top,
        body_width,
        body_height,
        distance,
        shade(base_color, 0.82),
    );
    let head_size = (unit * 0.38).round() as i32;
    draw_depth_rect(
        pixels,
        depth,
        width,
        height,
        sx.round() as i32 - head_size / 2,
        top - head_size + 1,
        head_size,
        head_size,
        distance - 0.01,
        shade(base_color, 1.15),
    );
    let leg_width = (body_width / 4).max(1);
    for offset in [body_width / 6, body_width * 2 / 3] {
        draw_depth_rect(
            pixels,
            depth,
            width,
            height,
            left + offset,
            top + body_height - 1,
            leg_width,
            (unit * 0.28).round() as i32,
            distance + 0.01,
            shade(base_color, 0.68),
        );
    }
}

fn shade(color: u32, factor: f32) -> u32 {
    let scale = |shift: u32| ((((color >> shift) & 255) as f32 * factor).clamp(0.0, 255.0)) as u32;
    0xFF000000 | scale(16) << 16 | scale(8) << 8 | scale(0)
}

fn draw_depth_rect(
    pixels: &mut [u32],
    depth: &mut [f32],
    width: usize,
    height: usize,
    x: i32,
    y: i32,
    w: i32,
    h: i32,
    z: f32,
    color: u32,
) {
    for py in y.max(0)..(y + h).min(height as i32) {
        for px in x.max(0)..(x + w).min(width as i32) {
            let index = py as usize * width + px as usize;
            if z < depth[index] {
                depth[index] = z;
                pixels[index] = color;
            }
        }
    }
}

struct TerrainTextures {
    tiles: Vec<Vec<u32>>,
}

impl TerrainTextures {
    fn load() -> Self {
        let mut tiles = Vec::with_capacity(256);
        for index in 0..256 {
            let path = format!("mc/resources/texture/terrain/tiles/tile_{index:03}.png");
            let image = match image::open(path) {
                Ok(image) => image.to_rgba8(),
                Err(_) => image::RgbaImage::new(16, 16),
            };
            let pixels = image
                .pixels()
                .map(|pixel| {
                    let [r, g, b, a] = pixel.0;
                    (a as u32) << 24 | (r as u32) << 16 | (g as u32) << 8 | b as u32
                })
                .collect();
            tiles.push(pixels);
        }
        Self { tiles }
    }

    fn pixel(&self, tile: usize, u: f32, v: f32) -> u32 {
        if let Some(pixels) = self.tiles.get(tile) {
            let x = ((u.clamp(0.0, 1.0) * 15.0).round() as usize).min(15);
            let y = (((1.0 - v.clamp(0.0, 1.0)) * 15.0).round() as usize).min(15);
            return pixels[y * 16 + x];
        }
        0xFFFF00FF
    }
}

fn block_texture_tile(block: u8, face: usize) -> usize {
    match block {
        GRASS => match face {
            4 => 0,
            5 => 2,
            _ => 3,
        },
        DIRT => 2,
        STONE => 1,
        SAND => 18,
        WOOD => match face {
            4 | 5 => 21,
            _ => 20,
        },
        LEAF => 52,
        BEDROCK => 17,
        TNT => match face {
            4 => 9,
            5 => 10,
            _ => 8,
        },
        LUCKY => match face {
            4 => 225,
            5 => 226,
            _ => 224,
        },
        WATER => 205,
        _ => 1,
    }
}

fn camera_vectors(player: &Player) -> (Vec3, Vec3, Vec3) {
    let forward = Vec3::new(
        -player.yaw.sin() * player.pitch.cos(),
        -player.pitch.sin(),
        -player.yaw.cos() * player.pitch.cos(),
    )
    .normalize();
    let right = Vec3::new(player.yaw.cos(), 0.0, -player.yaw.sin()).normalize();
    let up = right.cross(forward).normalize();
    (forward, right, up)
}

fn project(
    player: &Player,
    world_point: Vec3,
    width: usize,
    height: usize,
) -> Option<(f32, f32, f32)> {
    let (forward, right, up) = camera_vectors(player);
    let relative = world_point.sub(player.position);
    let depth = relative.dot(forward);
    if depth < 0.05 {
        return None;
    }
    let focal = height as f32 * 0.9;
    let x = width as f32 * 0.5 + relative.dot(right) / depth * focal;
    let y = height as f32 * 0.5 - relative.dot(up) / depth * focal;
    Some((x, y, depth))
}

fn draw_cube(
    pixels: &mut [u32],
    depth: &mut [f32],
    width: usize,
    height: usize,
    player: &Player,
    textures: &TerrainTextures,
    x: i32,
    y: i32,
    z: i32,
    block: u8,
) {
    let cx = x as f32;
    let cy = y as f32;
    let cz = z as f32;
    let faces = [
        [
            (cx, cy, cz + 1.0),
            (cx + 1.0, cy, cz + 1.0),
            (cx + 1.0, cy + 1.0, cz + 1.0),
            (cx, cy + 1.0, cz + 1.0),
        ],
        [
            (cx + 1.0, cy, cz),
            (cx, cy, cz),
            (cx, cy + 1.0, cz),
            (cx + 1.0, cy + 1.0, cz),
        ],
        [
            (cx, cy, cz),
            (cx, cy, cz + 1.0),
            (cx, cy + 1.0, cz + 1.0),
            (cx, cy + 1.0, cz),
        ],
        [
            (cx + 1.0, cy, cz + 1.0),
            (cx + 1.0, cy, cz),
            (cx + 1.0, cy + 1.0, cz),
            (cx + 1.0, cy + 1.0, cz + 1.0),
        ],
        [
            (cx, cy + 1.0, cz + 1.0),
            (cx + 1.0, cy + 1.0, cz + 1.0),
            (cx + 1.0, cy + 1.0, cz),
            (cx, cy + 1.0, cz),
        ],
        [
            (cx, cy, cz),
            (cx + 1.0, cy, cz),
            (cx + 1.0, cy, cz + 1.0),
            (cx, cy, cz + 1.0),
        ],
    ];
    for (face_index, face) in faces.iter().enumerate() {
        let mut points = [None; 4];
        let uv = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)];
        for i in 0..4 {
            let p = face[i];
            points[i] = project(player, Vec3::new(p.0, p.1, p.2), width, height);
        }
        if points.iter().any(|p| p.is_none()) {
            continue;
        }
        let tile = block_texture_tile(block, face_index);
        let a = (
            points[0].unwrap().0,
            points[0].unwrap().1,
            points[0].unwrap().2,
            uv[0].0,
            uv[0].1,
        );
        let b = (
            points[1].unwrap().0,
            points[1].unwrap().1,
            points[1].unwrap().2,
            uv[1].0,
            uv[1].1,
        );
        let c = (
            points[2].unwrap().0,
            points[2].unwrap().1,
            points[2].unwrap().2,
            uv[2].0,
            uv[2].1,
        );
        let d = (
            points[3].unwrap().0,
            points[3].unwrap().1,
            points[3].unwrap().2,
            uv[3].0,
            uv[3].1,
        );
        fill_textured_triangle(pixels, depth, width, height, textures, tile, a, b, c);
        fill_textured_triangle(pixels, depth, width, height, textures, tile, a, c, d);
    }
}

fn fill_textured_triangle(
    pixels: &mut [u32],
    depth: &mut [f32],
    width: usize,
    height: usize,
    textures: &TerrainTextures,
    tile: usize,
    a: (f32, f32, f32, f32, f32),
    b: (f32, f32, f32, f32, f32),
    c: (f32, f32, f32, f32, f32),
) {
    let min_x = a.0.min(b.0).min(c.0).floor().max(0.0) as i32;
    let max_x = a.0.max(b.0).max(c.0).ceil().min(width as f32 - 1.0) as i32;
    let min_y = a.1.min(b.1).min(c.1).floor().max(0.0) as i32;
    let max_y = a.1.max(b.1).max(c.1).ceil().min(height as f32 - 1.0) as i32;
    let area = (b.0 - a.0) * (c.1 - a.1) - (b.1 - a.1) * (c.0 - a.0);
    if area.abs() < 0.001 {
        return;
    }
    for y in min_y..=max_y {
        for x in min_x..=max_x {
            let px = x as f32 + 0.5;
            let py = y as f32 + 0.5;
            let w0 = ((b.0 - px) * (c.1 - py) - (b.1 - py) * (c.0 - px)) / area;
            let w1 = ((c.0 - px) * (a.1 - py) - (c.1 - py) * (a.0 - px)) / area;
            let w2 = 1.0 - w0 - w1;
            if w0 >= 0.0 && w1 >= 0.0 && w2 >= 0.0 {
                let z = w0 * a.2 + w1 * b.2 + w2 * c.2;
                let u = w0 * a.3 + w1 * b.3 + w2 * c.3;
                let v = w0 * a.4 + w1 * b.4 + w2 * c.4;
                let index = y as usize * width + x as usize;
                if z < depth[index] {
                    let color = textures.pixel(tile, u, v);
                    if color & 0xFF000000 != 0 {
                        depth[index] = z;
                        pixels[index] = color;
                    }
                }
            }
        }
    }
}

fn draw_crosshair(pixels: &mut [u32], width: usize, height: usize) {
    let x = width / 2;
    let y = height / 2;
    for dx in -4i32..=4 {
        if x as i32 + dx >= 0 && x as i32 + dx < width as i32 {
            pixels[y * width + (x as i32 + dx) as usize] = 0xFFFFFFFF;
        }
    }
    for dy in -4i32..=4 {
        if y as i32 + dy >= 0 && y as i32 + dy < height as i32 {
            pixels[(y as i32 + dy) as usize * width + x] = 0xFFFFFFFF;
        }
    }
}

fn draw_hotbar(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    hotbar: &[u8],
    selected: usize,
    textures: &TerrainTextures,
) {
    let slot = 14usize;
    let gap = 3usize;
    let total = hotbar.len() * slot + (hotbar.len() - 1) * gap;
    let start = (width - total) / 2;
    let top = height - slot - 8;
    for (i, block) in hotbar.iter().enumerate() {
        let x = start + i * (slot + gap);
        for py in top..top + slot {
            for px in x..x + slot {
                let border = i == selected
                    && (px - x < 2
                        || x + slot - 1 - px < 2
                        || py - top < 2
                        || top + slot - 1 - py < 2);
                let tile = block_texture_tile(*block, 4);
                let u = (px - x) as f32 / (slot - 1) as f32;
                let v = (py - top) as f32 / (slot - 1) as f32;
                pixels[py * width + px] = if border {
                    0xFFFFFF00
                } else {
                    textures.pixel(tile, u, v)
                };
            }
        }
    }
}

fn inventory_panel(width: usize, height: usize) -> (i32, i32) {
    (width as i32 / 2 - 78, height as i32 / 2 - 67)
}

fn inventory_item_hit(x: f32, y: f32, width: usize, height: usize) -> Option<usize> {
    let (left, top) = inventory_panel(width, height);
    let local_x = x - (left + 7) as f32;
    let local_y = y - (top + 23) as f32;
    if local_x < 0.0 || local_y < 0.0 {
        return None;
    }
    let col = (local_x / 16.0) as usize;
    let row = (local_y / 16.0) as usize;
    if col < 9 && row < 3 && local_x % 16.0 < 14.0 && local_y % 16.0 < 14.0 {
        Some(row * 9 + col)
    } else {
        None
    }
}

fn inventory_hotbar_hit(x: f32, y: f32, width: usize, height: usize) -> Option<usize> {
    let (left, top) = inventory_panel(width, height);
    let local_x = x - (left + 7) as f32;
    let local_y = y - (top + 81) as f32;
    if local_x < 0.0 || !(0.0..48.0).contains(&local_y) {
        return None;
    }
    let slot = (local_x / 16.0) as usize;
    if slot < 7 && local_x % 16.0 < 14.0 {
        Some(slot)
    } else {
        None
    }
}

fn draw_inventory(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    inventory: &[u8; 27],
    hotbar: &[u8; 7],
    selected: usize,
    textures: &TerrainTextures,
) {
    for pixel in pixels.iter_mut() {
        *pixel = blend(*pixel, 0xD0000000);
    }
    let (left, top) = inventory_panel(width, height);
    fill_rect(pixels, width, height, left, top, 156, 134, 0xFFB8B8B8);
    fill_rect(
        pixels,
        width,
        height,
        left + 2,
        top + 2,
        152,
        130,
        0xFF373737,
    );
    draw_bitmap_text(
        pixels,
        width,
        height,
        "INVENTORY",
        left + 8,
        top + 8,
        0xFFFFFFFF,
        1,
    );
    for (index, item) in inventory.iter().enumerate() {
        let x = left + 7 + (index % 9) as i32 * 16;
        let y = top + 23 + (index / 9) as i32 * 16;
        draw_item_slot(pixels, width, x, y, *item, textures, false);
    }
    for (index, item) in hotbar.iter().enumerate() {
        let x = left + 7 + index as i32 * 16;
        let y = top + 81;
        draw_item_slot(pixels, width, x, y, *item, textures, index == selected);
    }
    draw_bitmap_text(
        pixels,
        width,
        height,
        "CLICK ITEM TO EQUIP",
        left + 8,
        top + 113,
        0xFFFFFFFF,
        1,
    );
}

fn draw_item_slot(
    pixels: &mut [u32],
    width: usize,
    x: i32,
    y: i32,
    item: u8,
    textures: &TerrainTextures,
    selected: bool,
) {
    fill_rect(
        pixels,
        width,
        pixels.len() / width,
        x,
        y,
        14,
        14,
        if selected { 0xFFFFFF55 } else { 0xFF777777 },
    );
    fill_rect(
        pixels,
        width,
        pixels.len() / width,
        x + 1,
        y + 1,
        12,
        12,
        0xFF242424,
    );
    let tile = block_texture_tile(item, 4);
    for py in 0..10 {
        for px in 0..10 {
            pixels[(y + 2 + py) as usize * width + (x + 2 + px) as usize] =
                textures.pixel(tile, px as f32 / 9.0, py as f32 / 9.0);
        }
    }
}

fn draw_break_animation(pixels: &mut [u32], width: usize, height: usize, progress: f32) {
    if progress <= 0.0 {
        return;
    }
    let x = width as i32 / 2;
    let y = height as i32 / 2;
    let stage = (progress * 10.0).ceil() as i32;
    let cracks = [
        (-5, -4, 4, 1),
        (-2, -3, 1, 5),
        (1, -1, 4, 1),
        (2, 0, 1, 5),
        (-4, 2, 4, 1),
        (-5, 1, 1, 4),
        (0, 4, 4, 1),
        (-1, -5, 1, 3),
    ];
    for (index, (dx, dy, w, h)) in cracks.iter().enumerate() {
        if index < stage as usize {
            fill_rect(pixels, width, height, x + dx, y + dy, *w, *h, 0xFF171717);
        }
    }
    let bar_width = 48;
    fill_rect(
        pixels,
        width,
        height,
        x - bar_width / 2,
        y + 15,
        bar_width,
        4,
        0xFF202020,
    );
    fill_rect(
        pixels,
        width,
        height,
        x - bar_width / 2 + 1,
        y + 16,
        ((bar_width - 2) as f32 * progress.clamp(0.0, 1.0)) as i32,
        2,
        0xFFFFD040,
    );
}

fn draw_first_person_hand(
    pixels: &mut [u32],
    width: usize,
    height: usize,
    held_block: u8,
    textures: &TerrainTextures,
    swinging: bool,
) {
    let offset = if swinging { 6 } else { 0 };
    let x = width as i32 - 56 + offset;
    let y = height as i32 - 72 + offset;
    fill_rect(pixels, width, height, x + 10, y + 18, 30, 48, 0xFF31598A);
    fill_rect(pixels, width, height, x + 15, y + 8, 20, 38, 0xFFD59B72);
    fill_rect(pixels, width, height, x + 9, y + 40, 31, 24, 0xFF426FA5);
    let tile = block_texture_tile(held_block, 4);
    for py in 0..16 {
        for px in 0..16 {
            let screen_x = x - 5 + px;
            let screen_y = y - 9 + py;
            if screen_x >= 0 && screen_y >= 0 && screen_x < width as i32 && screen_y < height as i32
            {
                pixels[screen_y as usize * width + screen_x as usize] =
                    textures.pixel(tile, px as f32 / 15.0, py as f32 / 15.0);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mouse_look_follows_pointer_direction() {
        let world = World::new(16, 24, 16);
        let mut player = Player::spawn(&world);
        apply_mouse_look(&mut player, 10.0, -10.0);
        assert!(player.yaw < 0.0);
        assert!(player.pitch < 0.0);
    }

    #[test]
    fn menu_button_hit_testing_uses_screen_coordinates() {
        assert!(menu_button_hit(160.0, 150.0, 320, 240, 0));
        assert!(!menu_button_hit(20.0, 20.0, 320, 240, 0));
    }

    #[test]
    fn several_mobs_spawn_with_visible_kinds() {
        let world = World::new(64, 32, 64);
        let player = Player::spawn(&world);
        let mobs = Mob::spawn_near_player(&world, &player);
        assert!(mobs.len() >= 3);
        assert!(mobs.iter().any(|mob| mob.color() != 0));
    }

    #[test]
    fn inventory_slots_are_clickable() {
        assert_eq!(inventory_item_hit(126.0, 51.0, 320, 180), Some(2));
        assert_eq!(inventory_hotbar_hit(90.0, 105.0, 320, 180), Some(0));
        assert_eq!(inventory_item_hit(50.0, 50.0, 320, 180), None);
    }

    #[test]
    fn mining_progress_draws_cracks_and_hand_is_rendered() {
        let (width, height) = (320, 180);
        let mut pixels = vec![0xFF78B6F4; width * height];
        draw_break_animation(&mut pixels, width, height, 0.6);
        assert!(pixels.iter().any(|pixel| *pixel == 0xFF171717));

        let textures = TerrainTextures { tiles: Vec::new() };
        draw_first_person_hand(&mut pixels, width, height, GRASS, &textures, false);
        assert!(pixels.iter().any(|pixel| *pixel == 0xFF31598A));
    }
}
