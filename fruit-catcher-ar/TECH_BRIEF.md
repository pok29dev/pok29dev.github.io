# Tech Brief: Fruit Catcher AR

## Technology Choices

- **MediaPipe Hands**: Chosen for robust, real-time hand tracking directly in the browser. Landmark 8 (index finger tip) is mapped to the basket's X position, providing intuitive left-right control.
- **Tone.js**: Used for synthesized audio (catch/miss sounds). This ensures the game is 100% self-contained with no external audio file dependencies, adhering to kid-safe defaults.
- **Tailwind CSS (CDN)**: Provides rapid, responsive styling for UI overlays (permission and result screens) without needing a build step.
- **Single-File HTML**: The entire game (HTML, CSS, JS) is bundled into one file. This makes it trivial to test, share, and deploy without any Node.js or build tooling overhead.
- **Canvas API**: Used for rendering the game loop (falling items, basket) at 60fps, overlaid on top of the mirrored webcam feed.

## AR Interaction Design
- The webcam feed is mirrored (`transform: scaleX(-1)`) so moving the hand right moves the basket right on screen, matching natural intuition.
- MediaPipe returns normalized coordinates (0.0 to 1.0). We invert the X coordinate to account for the mirrored video, then clamp it between 0.1 and 0.9 to keep the basket on screen.
- A fallback mouse/touch listener is included for desktop testing or if the user denies camera access (though the game requires camera to start, the input fallback ensures the basket can still be moved if tracking drops).