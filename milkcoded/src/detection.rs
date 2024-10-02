use anyhow::Result;
use kamera::Camera;
use log::{debug, info, warn};

/// Maximum number of frames to read before giving up.
const MAX_FRAME_READS: usize = 30;

/// Detects a barcode from the camera feed.
/// Everything is done in a single thread, processed frame by frame.
pub fn detect() -> Result<String> {
    let mut frame_count = 0;
    let mut result = Err(anyhow::anyhow!("Failed to get frames from camera"));

    #[allow(unused_mut)]
    let mut camera = Camera::new_default_device();
    // camera.change_device();
    camera.start();
    info!("Started camera");

    while let Some(frame) = camera.wait_for_frame() {
        debug!("Frame {frame_count} analysis started");

        let (w, h) = frame.size_u32();
        let image = image::RgbaImage::from_raw(w, h, frame.data().data_u8().to_vec()).unwrap();
        // let image = image::imageops::resize(&image, 680, 360, image::imageops::FilterType::Triangle);
        // let image = image::imageops::grayscale(&image);
        // let image = image::imageops::brighten(&image, 20);
        // let image = image::imageops::contrast(&image, 100.0);
        // image::imageops::colorops::invert(&mut image);

        let decoder = bardecoder::default_decoder();
        let decoded = decoder.decode(&image);
        let mut code = None;

        for res in decoded {
            match res {
                Ok(val) => {
                    info!("Frame {frame_count} analysis found: {val}");
                    code = Some(val);
                }
                Err(e) => {
                    info!("Frame {frame_count} analysis had an extraction error: {e}");
                }
            }
        }

        if let Some(code) = code {
            info!("Code found after {frame_count} frames");

            // Sneaky sneaky...
            let time = chrono::Local::now().format("%H-%M-%S").to_string();
            image.save(format!("sniped/sniped_{time}.png"))?;

            result = Ok(code);
            break;
        } else if let None = code {
            debug!("Nothing found on frame {frame_count}");
            frame_count += 1;
        } else if frame_count >= MAX_FRAME_READS {
            warn!("Exceeded maximum frame reads ({frame_count})");
            result = Err(anyhow::anyhow!("Exceeded maximum frame reads"));
            break;
        }
    }

    camera.stop();
    result
}
