# Phase 2 — UX Design: Mosaic

## 1. User Journey Map

### First-Time Visitor
```
Land on homepage → See today's prompt → Tap "Create Your Piece"
    → Choose mode (Simple/Advanced) → Create contribution
    → Preview piece → Submit → See confirmation + share card
    → Share to social OR "See Today's Mosaic" → View composite
    → Bookmark / Return tomorrow
```

### Returning User
```
Return to homepage → See today's new prompt → Notice streak counter (v1.1)
    → Create today's piece → Share → Check yesterday's mosaic
    → Find their piece in the mosaic → Share mosaic link
```

---

## 2. Information Architecture

```
/ (Homepage)
├── Daily prompt display
├── "Create Your Piece" CTA
├── Live contribution counter ("142 people have contributed today")
├── Yesterday's mosaic preview
│
/create
├── Mode toggle: Simple | Advanced
├── Simple mode: emoji/color grid picker
├── Advanced mode: drawing canvas
├── Preview & submit
│
/piece/:id (Share Page)
├── Individual contribution display
├── Prompt text + date
├── Social share buttons (Twitter, Facebook, Copy Link)
├── "See the Full Mosaic" link
│
/mosaic/:date (Composite View)
├── Full mosaic image (zoomable)
├── Contribution count
├── Prompt text
├── Share buttons
├── "Create Your Piece for Today" CTA
│
/about
├── How it works
├── FAQ
```

---

## 3. Wireframe Descriptions (Mobile-First)

### 3.1 Homepage (`/`)

```
┌─────────────────────────┐
│         MOSAIC           │  ← Logo, centered
│                          │
│  ┌───────────────────┐   │
│  │  Today's Prompt:  │   │
│  │                   │   │
│  │  "Draw your       │   │  ← Prompt card, large text
│  │   morning mood    │   │
│  │   using only      │   │
│  │   shapes"         │   │
│  └───────────────────┘   │
│                          │
│  ● 142 pieces so far     │  ← Live counter, subtle pulse
│                          │
│  ┌───────────────────┐   │
│  │                   │   │
│  │  CREATE YOUR      │   │  ← Primary CTA button
│  │     PIECE         │   │     Full-width, bold color
│  │                   │   │
│  └───────────────────┘   │
│                          │
│  ── Yesterday's Mosaic ──│
│  ┌───────────────────┐   │
│  │  [Composite thumb] │   │  ← Tappable thumbnail
│  │  287 contributors  │   │
│  └───────────────────┘   │
│                          │
│  How it works →          │  ← Expandable section
└─────────────────────────┘
```

### 3.2 Creation Tool — Simple Mode (`/create`)

```
┌─────────────────────────┐
│  ← Back    Simple | Adv  │  ← Mode toggle tabs
│                          │
│  "Draw your morning mood │
│   using only shapes"     │  ← Prompt reminder
│                          │
│  ┌───────────────────┐   │
│  │                   │   │
│  │   [Live Preview]  │   │  ← 200x200 preview of piece
│  │                   │   │
│  └───────────────────┘   │
│                          │
│  Choose an emoji:        │
│  😊 😢 🔥 🌅 💡 🎨 ⭐ 🌙 │  ← Scrollable emoji grid
│  🌊 🌸 🍃 ❤️ 🎵 🦋 ✨ 🌈 │
│                          │
│  Pick a background:      │
│  [🟥][🟧][🟨][🟩][🟦][🟪]│  ← Color swatches
│  [⬛][⬜][🟫][custom]    │
│                          │
│  ┌───────────────────┐   │
│  │   PREVIEW PIECE   │   │  ← Secondary CTA
│  └───────────────────┘   │
└─────────────────────────┘
```

### 3.3 Creation Tool — Advanced Mode (`/create`)

```
┌─────────────────────────┐
│  ← Back    Simple | Adv  │
│                          │
│  ┌───────────────────┐   │
│  │                   │   │
│  │                   │   │
│  │   [Drawing        │   │  ← Touch canvas (300x300)
│  │    Canvas]        │   │     Pinch-to-zoom disabled
│  │                   │   │
│  │                   │   │
│  └───────────────────┘   │
│                          │
│  🖊️  ○ ◉ ●    🎨 🗑️  ↩️  │  ← Tools: pen, brush sizes,
│                          │     color, clear, undo
│  Colors:                 │
│  [●][●][●][●][●][●][+]  │  ← Preset + custom color
│                          │
│  ┌───────────────────┐   │
│  │   PREVIEW PIECE   │   │
│  └───────────────────┘   │
└─────────────────────────┘
```

### 3.4 Preview + Share Screen

```
┌─────────────────────────┐
│                          │
│       Your piece! 🎉     │  ← Celebration moment
│                          │
│  ┌───────────────────┐   │
│  │                   │   │
│  │  [Contribution    │   │  ← Rendered contribution
│  │   Image]          │   │     with subtle border
│  │                   │   │
│  └───────────────────┘   │
│                          │
│  "Draw your morning mood │
│   using only shapes"     │
│  March 21, 2026          │
│                          │
│  ┌───────────────────┐   │
│  │   SUBMIT PIECE    │   │  ← Primary CTA (if not yet submitted)
│  └───────────────────┘   │
│                          │
│  Share your piece:       │
│  [Twitter] [Facebook]    │  ← Social share buttons
│  [Copy Link] [Download]  │
│                          │
│  ┌───────────────────┐   │
│  │ SEE TODAY'S MOSAIC│   │  ← Secondary CTA
│  └───────────────────┘   │
└─────────────────────────┘
```

### 3.5 Composite View (`/mosaic/:date`)

```
┌─────────────────────────┐
│  ← Home    MOSAIC        │
│                          │
│  March 20, 2026          │
│  "Yesterday's prompt"    │
│  287 contributors        │
│                          │
│  ┌───────────────────┐   │
│  │                   │   │
│  │  [Full Mosaic     │   │  ← Pinch-to-zoom enabled
│  │   Composite       │   │     Tap piece to highlight
│  │   Image]          │   │
│  │                   │   │
│  │                   │   │
│  └───────────────────┘   │
│                          │
│  🔍 Zoom in to find      │
│     your piece           │
│                          │
│  Share this mosaic:      │
│  [Twitter] [Copy Link]   │
│                          │
│  ┌───────────────────┐   │
│  │ CREATE TODAY'S    │   │  ← CTA back to creation
│  │      PIECE        │   │
│  └───────────────────┘   │
└─────────────────────────┘
```

---

## 4. Design System Foundations

### Typography
- **Heading**: Inter, 700 weight — clean, modern, legible
- **Body**: Inter, 400 weight
- **Prompt text**: Playfair Display, 600 — adds warmth and creativity
- **Scale**: 14/16/20/24/32/40px (mobile); 16/18/24/28/36/48px (desktop)

### Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#6C5CE7` | CTA buttons, active states |
| `--primary-hover` | `#5A4BD4` | Button hover |
| `--secondary` | `#FF6B35` | Accents, counters, badges |
| `--background` | `#FEFEFE` | Page background |
| `--surface` | `#F8F7FF` | Card backgrounds |
| `--text-primary` | `#2D2D3F` | Headings, body text |
| `--text-secondary` | `#6B6B80` | Captions, metadata |
| `--success` | `#00C48C` | Submission success |
| `--error` | `#FF4757` | Errors, rejections |
| `--border` | `#E8E8EF` | Card borders, dividers |

### Spacing
- **Base unit**: 8px grid
- **Component padding**: 16px (mobile), 24px (desktop)
- **Section spacing**: 32px (mobile), 48px (desktop)
- **Border radius**: 12px (cards), 8px (buttons), 50% (avatars)

### Shadows
```css
--shadow-sm: 0 1px 3px rgba(45, 45, 63, 0.08);
--shadow-md: 0 4px 12px rgba(45, 45, 63, 0.12);
--shadow-lg: 0 8px 24px rgba(45, 45, 63, 0.16);
```

---

## 5. Micro-Interactions & Delight

| Moment | Animation |
|--------|-----------|
| **Submit piece** | Piece "stamps" down with a satisfying bounce + confetti particles |
| **Live counter** | Number ticks up with a subtle scale pulse when new contributions arrive |
| **Share card** | Card slides up from bottom with spring physics |
| **View mosaic** | Smooth zoom from overview → individual piece with haptic feedback |
| **Mode toggle** | Tabs slide with a pill indicator following the active tab |
| **Drawing** | Subtle pen pressure simulation — faster = thinner line |
| **Color pick** | Selected swatch scales up with a ring indicator |

---

## 6. Responsive Breakpoints

| Breakpoint | Width | Layout |
|-----------|-------|--------|
| Mobile (default) | < 640px | Single column, full-width cards |
| Tablet | 640–1024px | Wider cards, 2-col mosaic grid |
| Desktop | > 1024px | Centered max-width (720px), larger canvas |

**Mobile-first**: All CSS written for mobile, then enhanced with `min-width` media queries.

---

## 7. Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|------------|----------------|
| **Color contrast** | All text meets 4.5:1 ratio (verified against palette above) |
| **Keyboard navigation** | Full tab order for all interactive elements; visible focus rings |
| **Screen readers** | ARIA labels on canvas tools; alt text on all images; live regions for counter |
| **Motion** | Respect `prefers-reduced-motion`; disable confetti + bounce animations |
| **Touch targets** | Minimum 44x44px for all tappable elements |
| **Simple mode** | Fully accessible — grid of buttons with labels |
| **Advanced mode** | Canvas has limited accessibility; simple mode is the accessible alternative |
| **Skip links** | "Skip to main content" link for keyboard users |
