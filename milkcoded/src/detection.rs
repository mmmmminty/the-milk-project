use image::{GenericImageView, Rgba};
use nokhwa::*;
use anyhow::Result;
use log::info;
use pixel_format::RgbAFormat;
use utils::{CameraFormat, CameraIndex, FrameFormat, RequestedFormat, RequestedFormatType, Resolution};

/// Detects a barcode from the camera feed.
pub fn detect() -> Result<String> {
    /// Maximum number of frames to read before giving up.
    /// Default is 25, with an fps of 5.0, this is 5 seconds.
    const MAX_FRAME_READS: usize = 2005;

    let mut decoder = quircs::Quirc::default();
    let index = CameraIndex::Index(0);
    let requested = RequestedFormat::new::<RgbAFormat>(RequestedFormatType::AbsoluteHighestResolution);
    let mut camera = Camera::new(index, requested).unwrap();
    camera.open_stream()?;
    info!("Found camera");

    while let Ok(frame) = camera.frame() {
        let image = frame.decode_image::<RgbAFormat>().unwrap(); 
        let img_gray = image::imageops::grayscale(&image);
        let codes = decoder.identify(image.width() as usize, image.height() as usize, &img_gray);

        for code in codes {
            match code {
                Ok(code) => {
                    let decoded = code.decode().expect("failed to decode qr code");
                    println!("qrcode: {}", std::str::from_utf8(&decoded.payload).unwrap());
                    return Ok(std::str::from_utf8(&decoded.payload).unwrap().to_string());
                },
                Err(e) => {
                    println!("Error in barcode: {}", e);
                }
            }
        }

        // println!("Frame: {}", frame_count);
        // img_gray.save("frame.bmp").unwrap();
        // if frame_count >= MAX_FRAME_READS {
        //     return Err(anyhow::anyhow!("Exceeded maximum frame reads"));
        // }
    }

    Err(anyhow::anyhow!("Failed to detect barcode"))
}