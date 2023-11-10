use glow::HasContext;



fn create_vao(
    gl: &glow::Context,
    vertices: &Vec<(
        f32, f32, f32,
        f32, f32, f32,
        f32, f32,
    )>, // Position(x, y, z) Color(r, g, b) tex_coords(x, y)
    indices: &Vec<(u32, u32, u32)>
) -> (glow::VertexArray, glow::Buffer) {
    let vao: glow::NativeVertexArray = unsafe { gl.create_vertex_array().unwrap() };
    let vbo: glow::NativeBuffer = unsafe { gl.create_buffer().unwrap() };
    let ebo: glow::NativeBuffer = unsafe { gl.create_buffer().unwrap() };
    unsafe {
        gl.bind_vertex_array(Some(vao));

        gl.bind_buffer(glow::ARRAY_BUFFER, Some(vbo));
        gl.buffer_data_u8_slice(
            glow::ARRAY_BUFFER,
            &vertices.align_to::<u8>().1,
            glow::STATIC_DRAW,
        );

        gl.bind_buffer(glow::ELEMENT_ARRAY_BUFFER, Some(ebo));
        gl.buffer_data_u8_slice(
            glow::ELEMENT_ARRAY_BUFFER,
            &indices.align_to::<u8>().1,
            glow::STATIC_DRAW,
        );

        // Position attribute
        gl.enable_vertex_attrib_array(0);
        gl.vertex_attrib_pointer_f32(0, 3, glow::FLOAT, false, 8 * 4, 0);

        // Color attribute
        gl.enable_vertex_attrib_array(1);
        gl.vertex_attrib_pointer_f32(1, 3, glow::FLOAT, false, 8 * 4, 3 * 4);

        // Tex Coords attribute
        gl.enable_vertex_attrib_array(2);
        gl.vertex_attrib_pointer_f32(2, 2, glow::FLOAT, false, 8 * 4, 6 * 4);


        gl.bind_buffer(glow::ARRAY_BUFFER, None);
        gl.bind_vertex_array(None);
    }

    (vao, ebo)
}
