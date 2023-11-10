//? https://learnopengl.com

#![allow(unused)]
#![allow(warnings)]
#![allow(non_upper_case_globals)]

use config::Config;

mod config;
mod gui;
mod collections;
extern crate serde;
extern crate winapi;
extern crate serde_json;
extern crate glfw;
extern crate glow;
extern crate nalgebra_glm;
extern crate nalgebra;
extern crate image;
extern crate fps_clock;
extern crate regex;

use {
    glow::HasContext,
    glfw::{
        Context,
        Action,
        Key,
        MouseButton,
    },
    winapi::{
        shared::windef::HWND__,
        um::{
            wingdi::RGB,
            winuser::{
                SetLayeredWindowAttributes,
                SetWindowLongW,
                SetWindowPos,
                GetShellWindow,
                HWND_TOPMOST,
                SWP_NOMOVE,
                SWP_NOSIZE,
                GWL_EXSTYLE,
                WS_EX_LAYERED,
                WS_EX_NOACTIVATE,
                LWA_COLORKEY,
            },
        }
    },
    std::{
        time::{
            Duration,
            Instant,
        },
        collections::HashMap,
        ptr,
    },
};

const VertexShader: &str = r#"#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

out vec3 ourColor;
out vec2 TexCoord;

void main() {
    gl_position = vec4(aPos, 1.0);
    ourColor = aColor;
    TexCoord = aTexCoord;
}
"#;
const FragmentShader: &str = r#"#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexure;

void main() {
    FragColor = texture(ourTexture, TexCoord);
}
"#;
const TransparentColor: (u8, u8, u8) = (24, 164, 86);

struct Client {
    glfw: glfw::Glfw,
    window: glfw::Window,
    events: std::sync::mpsc::Receiver<(f64, glfw::WindowEvent)>,
    gl: glow::Context,
    clock: fps_clock::FpsClock,
    delta_time: f32,
    settings: Config,
}

impl Client {
    pub fn new(config: config::Config) -> Self {
        let mut glfw_: glfw::Glfw = glfw::init(glfw::fail_on_errors).expect("Failed to initialize GLFW");

        glfw_.window_hint(glfw::WindowHint::ContextVersion(3, 3));
        glfw_.window_hint(glfw::WindowHint::OpenGlProfile(glfw::OpenGlProfileHint::Core));
        glfw_.window_hint(glfw::WindowHint::DoubleBuffer(true));

        let (mut window_, events_) = glfw_.create_window(400, 400, "", glfw::WindowMode::Windowed).expect("Failed to create GLFW window");
        let hwnd: *mut HWND__ = window_.get_win32_window() as *mut _;

        window_.set_resizable(false);
        // window_.set_decorated(false);
        window_.set_key_polling(true);
        window_.make_current();
        glfw_.set_swap_interval(glfw::SwapInterval::None);

        let gl_ctx: glow::Context = unsafe { glow::Context::from_loader_function(|s: &str| window_.get_proc_address(s) as *const _) };

        unsafe {
            gl_ctx.clear_color(
                TransparentColor.0 as f32 / 255.0,
                TransparentColor.1 as f32 / 255.0,
                TransparentColor.2 as f32 / 255.0,
                1.0
            );
            SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
            SetWindowLongW(hwnd, GWL_EXSTYLE, WS_EX_LAYERED as i32 | WS_EX_NOACTIVATE as i32);
            SetLayeredWindowAttributes(hwnd, RGB(TransparentColor.0, TransparentColor.1, TransparentColor.2), 0, LWA_COLORKEY);
        }

        let mut clock_: fps_clock::FpsClock = fps_clock::FpsClock::new(60);

        Self {
            glfw: glfw_,
            window: window_,
            events: events_,
            gl: gl_ctx,
            clock: clock_,
            delta_time: 0.0,
            settings: config,
        }
    }

    //= Functions? IDK what to type here ====================================================
    unsafe fn get_game_window_size(&self) -> (u32, u32) { (0, 0) }
    unsafe fn get_game_window_position(&self) -> (i32, i32) { (0, 0) }
    unsafe fn is_game_windowed(&self) -> bool { false }
    unsafe fn is_game_focused(&self) -> bool { false }
    unsafe fn get_display_pixel(&self) -> (u8, u8, u8) { (0, 0, 0) }
    unsafe fn is_game_process_running(&self) -> bool { false }
    unsafe fn set_window_size(&mut self, width: u32, height: u32) {}
    unsafe fn set_window_position(&mut self, x: i32, y: i32) {}
    unsafe fn hide_window(&mut self, hide: bool) {}
    unsafe fn refresh_window(&mut self, width: u32, height: u32, x: i32, y: i32) {
        self.set_window_size(width, height);
        self.set_window_position(x, y);
    }
    //=======================================================================================

    fn register_quit(&self) {
        std::process::exit(0);
    }

    unsafe fn main_function(&mut self) {
        loop {
            self.gl.clear(glow::COLOR_BUFFER_BIT | glow::DEPTH_BUFFER_BIT);
            let fps: f32 = (1.0 / self.delta_time).round();

            self.glfw.poll_events();
            if self.window.should_close() { self.register_quit(); }
            self.window.set_title(format!("{} {}", fps, (self.delta_time * 100_000.0).round() / 100_000.0).as_str());

            for (_, event) in glfw::flush_messages(&self.events) {
                match event {
                    glfw::WindowEvent::Key(Key::Escape, _, Action::Press, _) => {
                        self.window.set_should_close(true);
                    }
                    glfw::WindowEvent::Size(width, height) => {
                        self.gl.viewport(0, 0, width, height);
                    }
                    _ => {}
                }
            }



            self.window.swap_buffers();
            self.delta_time = self.clock.tick() / 1_000_000_000.0;
        }
    }

    pub fn main(&mut self) {
        unsafe {
            self.main_function();
        }
    }
}

fn main() {
    let config: config::Config = config::get_config("file_path");
    let mut client: Client = Client::new(config);
    client.main();
}

fn make_shader_program(
    gl: &glow::Context,
    fragment_shader: &str,
    vertex_shader: &str,
) -> glow::Program {
    unsafe {
        // Compile vertex shader
        let vs: glow::NativeShader = gl.create_shader(glow::VERTEX_SHADER).unwrap();
        gl.shader_source(vs, vertex_shader);
        gl.compile_shader(vs);

        // Check vertex shader compilation status
        if !gl.get_shader_compile_status(vs) {
            eprintln!("Error: Failed to compile vertex shader:\n{}", gl.get_shader_info_log(vs));
        }

        // Compile fragment shader
        let fs: glow::NativeShader = gl.create_shader(glow::FRAGMENT_SHADER).unwrap();
        gl.shader_source(fs, fragment_shader);
        gl.compile_shader(fs);

        // Check fragment shader compilation status
        if !gl.get_shader_compile_status(fs) {
            eprintln!("Error: Failed to compile fragment shader:\n{}", gl.get_shader_info_log(fs));
        }

        // Create shader program and link shaders
        let program: glow::NativeProgram = gl.create_program().unwrap();
        gl.attach_shader(program, vs);
        gl.attach_shader(program, fs);
        gl.link_program(program);

        // Check program linking status
        if !gl.get_program_link_status(program) {
            eprintln!("Error: Failed to link program:\n{}", gl.get_program_info_log(program));
        }

        // Delete shaders as they are now linked into the program and no longer needed
        gl.delete_shader(vs);
        gl.delete_shader(fs);

        program
    }
}
