use std::fs;
use std::str::FromStr;

use ab_glyph::{FontArc, PxScale};
use anyhow::Result;
use imageproc::drawing::draw_text_mut;
use imageproc::image::{Rgba, RgbaImage};
use log::{debug, info};
use resvg::tiny_skia::{Pixmap, PremultipliedColorU8};
use uuid::Uuid;

use crate::encode;

use super::Milk;

#[derive(Debug)]
pub struct Label {
    pub volume: i32,
    pub additives: String,
    pub mother: String,
    pub baby: String,
    pub expiry: String,
    pub id: String,
    pub code: String,
}

impl Label {
    pub fn to_milk(self) -> Result<Milk> {
        Ok(Milk {
            id: uuid::Uuid::from_str(&self.id)?,
            volume: self.volume,
            additives: Some(self.additives),
            expiry: chrono::NaiveDateTime::parse_from_str(&self.expiry, "%Y-%m-%d")?,
            expressed_at: chrono::Utc::now().naive_utc(),
            expressed_by: 00000000000,
        })
    }
}

pub fn generate_label(
    volume: i32,
    additives: &str,
    mother: &str,
    baby: &str,
    id: Option<&str>,
) -> Result<Label> {
    let id = match id {
        Some(id) => id.to_string(),
        None => Uuid::new_v4().to_string(),
    };
    let output_path = format!("labels/label_{}.png", id);

    info!("Generating label with ID: {}", id);
    encode(&id, &output_path)?;

    let label = Label {
        volume,
        additives: additives.to_string(),
        mother: mother.to_string(),
        baby: baby.to_string(),
        expiry: (chrono::Utc::now() + chrono::Duration::days(10))
            .format("%Y-%m-%d")
            .to_string(),
        id: id.clone(),
        code: output_path,
    };

    // Set up the image size
    let width = 800;
    let height = 400;

    // Create an empty RGBA image with a white background
    let mut image = RgbaImage::new(width, height);
    let white = Rgba([255, 255, 255, 255]);
    for pixel in image.pixels_mut() {
        *pixel = white;
    }

    // Load and render the PNG image on the left side
    // render_png(&label.code, &mut image)?;
    render_svg(&label.code, &mut image)?;
    debug!("Label QR rendered successfully");

    // Load a default font
    let font_data = include_bytes!("../../calibri.ttf");
    let font = FontArc::try_from_slice(font_data)?;

    // Define text scale
    let scale = PxScale::from(20.0);

    // Draw the text onto the image (right side)
    let text_color = imageproc::image::Rgba([0, 0, 0, 255]); // Black

    let text_position_x = 300; // Leave space on the left for PNG
    let mut y = 60; // Starting Y position for text

    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("Volume: {} ml", label.volume),
    );
    y += 50;
    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("Additives: {}", label.additives),
    );
    y += 50;
    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("Mother: {}", label.mother),
    );
    y += 50;
    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("Baby: {}", label.baby),
    );
    y += 50;
    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("Expiry: {}", label.expiry),
    );
    y += 50;
    draw_text_mut(
        &mut image,
        text_color,
        text_position_x,
        y,
        scale,
        &font,
        &format!("ID: {}", label.id),
    );

    // Save the image
    image.save(&label.code)?;
    info!("Label saved: {:?}", label);

    Ok(label)
}

fn render_svg(svg_path: &str, image: &mut RgbaImage) -> Result<()> {
    // Load the SVG file
    let svg_data = fs::read(svg_path)?;

    // Parse the SVG data
    let opt = usvg::Options::default();
    let rtree = usvg::Tree::from_data(&svg_data, &opt)?;

    // Get the size of the image
    let (_img_width, img_height) = image.dimensions();

    // Create a Pixmap for rendering the SVG
    let mut pixmap = Pixmap::new(300, img_height).expect("Failed to create pixmap");

    // Render the SVG into the pixmap
    resvg::render(
        &rtree,
        resvg::tiny_skia::Transform::from_scale(8.0, 8.0),
        &mut pixmap.as_mut(),
    );

    // Copy the pixmap into the image buffer
    let pixmap_pixels = pixmap.pixels_mut();
    for (i, pixel) in pixmap_pixels.iter().enumerate() {
        let x = (i % 300) as u32;
        let y = (i / 300) as u32; // Leave space on the top for text
        let rgba = de_premultiply(*pixel);
        let img_pixel = image.get_pixel_mut(x, y);
        *img_pixel = Rgba([rgba[0], rgba[1], rgba[2], rgba[3]]);
    }

    Ok(())
}

// Helper function to de-premultiply the PremultipliedColorU8
fn de_premultiply(color: PremultipliedColorU8) -> [u8; 4] {
    if color.alpha() == 0 {
        return [255, 255, 255, 255]; // Fully transparent pixel
    }

    let alpha = color.alpha() as f32 / 255.0;
    [
        (color.red() as f32 / alpha) as u8,
        (color.green() as f32 / alpha) as u8,
        (color.blue() as f32 / alpha) as u8,
        color.alpha(),
    ]
}
