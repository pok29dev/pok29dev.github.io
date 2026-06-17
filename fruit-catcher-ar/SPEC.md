# Fruit Catcher AR Game Specification

## Core Mechanic
- **Gameplay**: Fruits, balloons, or stars fall from the top of the screen.
- **Interaction**: Player moves their hand (left-right) to control a basket at the bottom of the screen to catch the falling items.
- **Target Audience**: Children (kid-safe, no external links, no ads, synthesized audio only).
- **Device**: Mobile-first, touch screen compatible.

## AR Interaction
- **Primary Input**: Hand tracking (MediaPipe Hands).
- **Tracking Point**: Index finger tip (landmark 8) or wrist (landmark 0) mapped to the horizontal (X) axis of the basket.
- **Fallback**: Mouse/Touch movement for desktop testing or if camera is denied.

## Screen Flow
1. **Permission Screen**: Ask for camera access (cached in `localStorage`).
2. **Game Screen**: 
   - Challenge: Items fall at increasing speed.
   - AR Action: Hand moves basket.
   - Feedback: Visual (catch animation) + Audio (synthesized SFX via Tone.js).
   - Score: +10 per catch, -1 life per miss.
3. **Result Screen**: Final score, high score, "Play Again" button (returns to Game Screen without re-asking camera).

## Tech Stack
- **AR Library**: MediaPipe Hands (via CDN).
- **UI/Styling**: Tailwind CSS (via CDN) + custom playful CSS for kids.
- **Audio**: Tone.js (synthesized sounds, no external audio files for kid-safety).
- **Output Format**: Single-file HTML (self-contained, easy to run).

## Constraints
- No external links, ads, or data collection.
- Responsive design, no vertical scroll on mobile.
- Mirror/flip handling for AR video feed.