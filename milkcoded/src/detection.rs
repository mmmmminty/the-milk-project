use image::Rgba;
use nokhwa::*;
use anyhow::Result;
use log::info;
use pixel_format::RgbAFormat;
use utils::{CameraIndex, RequestedFormat, RequestedFormatType};

/// Detects a barcode from the camera feed.
pub fn detect() -> Result<String> {
    /// Maximum number of frames to read before giving up.
    /// Default is 25, with an fps of 5.0, this is 5 seconds.
    const MAX_FRAME_READS: usize = 2005;

    let decoder = bardecoder::default_decoder();
    let index = CameraIndex::Index(0); 
    let requested = RequestedFormat::new::<RgbAFormat>(RequestedFormatType::AbsoluteHighestResolution);
    let mut camera = Camera::new(index, requested).unwrap();
    camera.open_stream().unwrap();
    info!("Found camera");

    for frame_count in 0..MAX_FRAME_READS {
        let frame = camera.frame().unwrap();
        let image: image::ImageBuffer<Rgba<u8>, Vec<u8>> = frame.decode_image::<RgbAFormat>().unwrap(); 

        fn convert_to_black_and_white(image: &image::ImageBuffer<Rgba<u8>, Vec<u8>>) -> image::ImageBuffer<Rgba<u8>, Vec<u8>> {
            let mut new_image = image.clone();
            for (_x, _y, pixel) in new_image.enumerate_pixels_mut() {
                let Rgba(data) = *pixel;
                let gray_value = (0.299 * data[0] as f32 + 0.587 * data[1] as f32 + 0.114 * data[2] as f32) as u8;
                *pixel = Rgba([gray_value, gray_value, gray_value, data[3]]);
            }
            new_image
        }

        let new_image = convert_to_black_and_white(&image);

        let result = decoder.decode(&new_image);
        info!("Got & decoded frame... checking for barcode");
        println!("Got & decoded frame... checking for barcode");
        println!("Results: {}", result.len());

        for code in result {
            match code {
                Ok(data) => {
                    info!("Detected: {}", data);
                    return Ok(data);
                },
                Err(e) => {
                    info!("Error in barcode: {}", e);
                    println!("Error in barcode: {}", e);
                }
            }
        }

        println!("Frame: {}", frame_count);
        // new_image.save("frame.bmp").unwrap();
        if frame_count >= MAX_FRAME_READS {
            return Err(anyhow::anyhow!("Exceeded maximum frame reads"));
        }
    }

    Err(anyhow::anyhow!("Failed to detect barcode"))
}