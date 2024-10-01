use anyhow::Result;
use image::imageops::colorops::invert;
use image::imageops::contrast;
use image::DynamicImage;
use log::{debug, info, warn};
use nokhwa::*;
use pixel_format::RgbAFormat;
use std::sync::Mutex;
use std::sync::{atomic::AtomicBool, Arc};
use utils::{CameraIndex, RequestedFormat, RequestedFormatType};

/// Maximum number of frames to read before giving up.
/// Default is 150, with an fps of 30, this is 5 seconds.
const MAX_FRAME_READS: usize = 150;

/// Camera index to use. Call `find_cameras()` to find available cameras.
const CAMERA_INDEX: CameraIndex = CameraIndex::Index(0);

/// Detects a barcode from the camera feed.
/// Camera feed is read in a separate thread, and the first QR code found is returned.
/// Might be faster than the single-threaded version, maybe, idk.
#[allow(dead_code)]
pub fn detect_threaded() -> Result<String> {
    nokhwa_initialize(|s| info!("Initialised Nokhwa: {s}"));
    let format = RequestedFormat::new::<RgbAFormat>(RequestedFormatType::AbsoluteHighestResolution);
    let (tx, rx) = std::sync::mpsc::channel();
    let frame_count = Arc::new(Mutex::new(0));
    let found = Arc::new(AtomicBool::new(false));
    let callback_closure = {
        let found = found.clone();
        let tx = tx.clone();
        let frame_count = frame_count.clone();
        move |frame: Buffer| {
            if found.load(std::sync::atomic::Ordering::Relaxed) {
                return;
            }

            let mut count = frame_count.lock().unwrap();
            let frame_count = *count;
            *count += 1;
            drop(count);

            debug!("Decoder thread for frame {frame_count} started");
            let decoder = bardecoder::default_decoder();

            let image = frame
                .decode_image::<RgbAFormat>()
                .expect("failed to decode image");
            let image = image::imageops::grayscale(&image);
            let image = contrast(&image, 300.0);
            let mut image = DynamicImage::ImageLuma8(image);
            invert(&mut image);

            let result = decoder.decode(&image);
            for code in &result {
                match code {
                    Ok(code) => {
                        info!("Decoder thread for frame {frame_count} found: {}", code);
                        found.store(true, std::sync::atomic::Ordering::Relaxed);
                        tx.send(Some(code.clone())).unwrap();
                        break;
                    }
                    Err(e) => {
                        info!(
                            "Decoder thread for frame {frame_count} had an extraction error: {e}"
                        );
                    }
                }
            }

            debug!(
                "Decoder thread for frame {frame_count} finished, found {} results",
                result.len()
            );
            if !found.load(std::sync::atomic::Ordering::Relaxed) {
                tx.send(None).unwrap();
            }
        }
    };

    let mut camera = CallbackCamera::new(CAMERA_INDEX, format, callback_closure)?;
    camera.open_stream()?;
    info!("Started camera");

    while let Ok(code) = rx.recv() {
        if found.load(std::sync::atomic::Ordering::Relaxed) {
            camera.stop_stream()?;
            info!(
                "Code found after {} frames, stopping camera",
                *frame_count.lock().unwrap()
            );
            return Ok(code.unwrap());
        } else {
            if *frame_count.lock().unwrap() >= MAX_FRAME_READS {
                camera.stop_stream()?;
                warn!("Exceeded maximum frame reads");
                return Err(anyhow::anyhow!("Exceeded maximum frame reads"));
            }
        }
    }

    warn!("Failed to recieve frame from camera");
    Err(anyhow::anyhow!("Failed to recieve frame from camera"))
}

#[allow(dead_code)]
/// Detects a barcode from the camera feed.
/// Everything is done in a single thread, processed frame by frame.
pub fn detect() -> Result<String> {
    nokhwa_initialize(|s| info!("Initialised Nokhwa: {s}"));
    let format = RequestedFormat::new::<RgbAFormat>(RequestedFormatType::AbsoluteHighestResolution);
    let mut frame_count = 0;
    let mut camera = Camera::new(CAMERA_INDEX, format).unwrap();
    let polling_delay = std::time::Duration::from_secs_f32(1.0 / camera.frame_rate() as f32);
    camera.open_stream()?;
    info!("Started camera");

    while let Ok(frame) = camera.frame() {
        debug!("Decoder thread for frame {frame_count} started");
        let decoder = bardecoder::default_decoder();

        let image = frame
            .decode_image::<RgbAFormat>()
            .expect("failed to decode image");
        let image = image::imageops::grayscale(&image);
        let image = contrast(&image, 300.0);
        let mut image = DynamicImage::ImageLuma8(image);
        invert(&mut image);

        let result = decoder.decode(&image);
        let mut found = None;
        for code in result {
            match code {
                Ok(code) => {
                    info!("Decoder thread for frame {frame_count} found: {}", code);
                    found = Some(code);
                }
                Err(e) => {
                    info!("Decoder thread for frame {frame_count} had an extraction error: {e}");
                }
            }
        }

        if let Some(code) = found {
            info!("Code found after {} frames", frame_count);
            camera.stop_stream()?;
            return Ok(code);
        } else if frame_count >= MAX_FRAME_READS {
            camera.stop_stream()?;
            warn!("Exceeded maximum frame reads ({frame_count})");
            return Err(anyhow::anyhow!("Exceeded maximum frame reads"));
        } else {
            debug!("Nothing found on frame {}", frame_count);
            frame_count += 1;
            std::thread::sleep(polling_delay);
        }
    }

    camera.stop_stream()?;
    warn!("Failed to recieve frame fron camera");
    Err(anyhow::anyhow!("Failed to recieve frame from camera"))
}

#[allow(dead_code)]
fn find_cameras() {
    let cameras = query(utils::ApiBackend::Auto).unwrap();
    cameras
        .iter()
        .for_each(|c| println!("Camera Found: {:?}", c));
}
