use image::{DynamicImage, ImageBuffer, Rgba, RgbaImage};
use anyhow::Result;
use log::info;

/// Detects a barcode from the camera feed.
pub fn detect() -> Result<String> {
    /// Maximum number of frames to read before giving up.
    /// Default is 25, with an fps of 5.0, this is 5 seconds.
    const MAX_FRAME_READS: usize = 2005;

    let decoder = bardecoder::default_decoder();
    let cam = camera_capture::create(0)
        .unwrap()
        .fps(5.0)
        .unwrap()
        .start()?;

    for (frame_count, frame) in cam.enumerate() {
        let (width, height) = frame.dimensions();
        let mut converted_img: RgbaImage = ImageBuffer::new(width, height);

        for (x, y, pixel) in frame.enumerate_pixels() {
            let rgba = Rgba([pixel[0], pixel[1], pixel[2], 255]);
            converted_img.put_pixel(x, y, rgba);
        }

        let converted = DynamicImage::ImageRgba8(converted_img);    
        let result = decoder.decode(&converted);
        
        for code in result {
            println!("Attempting to decode: {:?}", code);
            match code {
                Ok(data) => {
                    info!("Detected: {}", data);
                    return Ok(data);
                },
                Err(e) => {
                    info!("Error: {}", e);
                }
            }
        }

        println!("Frame: {}", frame_count);
        if frame_count >= MAX_FRAME_READS {
            return Err(anyhow::anyhow!("Exceeded maximum frame reads"));
        }
    }

    Err(anyhow::anyhow!("Failed to detect barcode"))
}