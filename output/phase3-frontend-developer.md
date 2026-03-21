# Phase 3 — Frontend Developer: Component Architecture

## 1. Component Hierarchy

```
RootLayout
├── Header (logo, minimal nav)
├── [Pages]
│   ├── HomePage
│   │   ├── PromptCard (server component)
│   │   ├── LiveCounter (client — polls/WebSocket)
│   │   ├── CTAButton → /create
│   │   └── YesterdayMosaic (server — async image)
│   │
│   ├── CreatePage
│   │   ├── PromptReminder
│   │   ├── ModeToggle (Simple | Advanced)
│   │   ├── SimpleMode
│   │   │   ├── EmojiGrid
│   │   │   ├── ColorPalette
│   │   │   └── LivePreview
│   │   ├── AdvancedMode
│   │   │   ├── DrawingCanvas (Fabric.js)
│   │   │   ├── ToolBar (pen, size, color, undo, clear)
│   │   │   └── LivePreview
│   │   └── PreviewSubmitSheet
│   │       ├── PiecePreview
│   │       ├── SubmitButton
│   │       └── ShareButtons
│   │
│   ├── PiecePage (share page)
│   │   ├── PieceImage
│   │   ├── PromptInfo
│   │   ├── ShareButtons
│   │   └── CTAButton → /mosaic/:date
│   │
│   └── MosaicPage
│       ├── MosaicViewer (pinch-zoom, pan)
│       ├── MosaicInfo (date, count, prompt)
│       ├── ShareButtons
│       └── CTAButton → /create
│
└── Footer (about link, minimal)
```

---

## 2. State Management

**No global state library needed for MVP.** Use:

| State | Solution | Scope |
|-------|----------|-------|
| Creation flow (selected emoji, color, mode) | React `useState` in CreatePage | Page-level |
| Drawing canvas state | Fabric.js internal + ref | Component-level |
| Contribution submission status | React `useState` + fetch | Page-level |
| Server data (prompt, composite) | Server Components + `fetch` | Request-level |
| Live counter | `useSWR` with polling (30s interval) | Component-level |

### Data Fetching Pattern
```typescript
// Server Component (default) — no client JS shipped
async function HomePage() {
  const prompt = await getPrompt(); // Direct DB/cache call
  return <PromptCard prompt={prompt} />;
}

// Client Component — for interactive features
'use client';
function LiveCounter({ initialCount }: { initialCount: number }) {
  const { data } = useSWR('/api/contributions/count', fetcher, {
    refreshInterval: 30000,
    fallbackData: initialCount,
  });
  return <span>{data?.count}</span>;
}
```

---

## 3. Key Component Specifications

### 3.1 SimpleMode

```typescript
// State
const [selectedEmoji, setSelectedEmoji] = useState<string | null>(null);
const [backgroundColor, setBackgroundColor] = useState('#FF6B35');

// Emoji grid: 16 curated emojis relevant to daily themes
const EMOJI_OPTIONS = ['😊','😢','🔥','🌅','💡','🎨','⭐','🌙','🌊','🌸','🍃','❤️','🎵','🦋','✨','🌈'];

// Color palette: 12 preset + 1 custom
const COLOR_OPTIONS = ['#FF6B35','#E84855','#6C5CE7','#00C48C','#FDCB58','#26C6DA','#AB47BC','#F06292','#2D2D3F','#FEFEFE','#8D6E63','#78909C'];

// Preview: 200x200 canvas rendering emoji on background
// Submit: POST to API with { contentType: 'emoji', contentData: { emoji, backgroundColor } }
```

### 3.2 AdvancedMode (Drawing Canvas)

```typescript
// Using Fabric.js for touch-friendly drawing
// Canvas size: 300x300 (scaled to container width on mobile)
// Tools: freehand brush, color picker, brush size (3 sizes), undo, clear
// Export: canvas.toDataURL('image/png') → base64

const canvasRef = useRef<fabric.Canvas | null>(null);

useEffect(() => {
  const canvas = new fabric.Canvas('drawing-canvas', {
    isDrawingMode: true,
    width: 300,
    height: 300,
    backgroundColor: '#FFFFFF',
  });
  canvas.freeDrawingBrush.width = 5;
  canvas.freeDrawingBrush.color = '#2D2D3F';
  canvasRef.current = canvas;

  return () => canvas.dispose();
}, []);
```

**Mobile touch handling**:
- Disable page scroll when touching canvas
- `touch-action: none` on canvas element
- Prevent pinch-zoom on canvas (allow on mosaic viewer)

### 3.3 MosaicViewer

```typescript
// Pinch-to-zoom + pan for composite image
// Using CSS transform + touch events (no heavy library)
// Constraints: min zoom 1x, max zoom 5x, bounded pan

const [transform, setTransform] = useState({ scale: 1, x: 0, y: 0 });

// Render: <img> wrapped in transform container
// On tap: smooth zoom to 2x centered on tap point
// On pinch: live scale adjustment
// Reset button: return to 1x overview
```

### 3.4 ShareButtons

```typescript
// Social sharing with pre-populated text
const shareData = {
  twitter: `I contributed to today's Mosaic! 🎨 Check out my piece: ${shareUrl}`,
  facebook: shareUrl,
  copyLink: shareUrl,
};

// OG tags (set in page metadata):
// og:title = "My piece in today's Mosaic"
// og:image = contribution image URL (or composite for mosaic page)
// og:description = prompt text
```

---

## 4. Performance Strategy

| Technique | Where | Impact |
|-----------|-------|--------|
| Server Components | Homepage, share page, mosaic page | Zero client JS for static content |
| Dynamic imports | `AdvancedMode` (Fabric.js is ~300KB) | Only loaded when user selects advanced mode |
| Image optimization | `next/image` for all images | WebP, responsive sizes, lazy loading |
| SWR | Live counter | Stale-while-revalidate, 30s polling |
| Route prefetching | Next.js default link prefetch | Instant page transitions |
| Tailwind CSS | All styling | Purged CSS, ~10KB production bundle |

**Target Core Web Vitals**:
- LCP: < 2.0s (hero prompt card)
- FID: < 100ms
- CLS: < 0.1
- INP: < 200ms

### Bundle Strategy
```
Entry chunks:
  - layout.js: ~15KB (React, minimal layout)
  - page.js (home): ~5KB (mostly server-rendered)
  - create/page.js: ~20KB (SimpleMode + ModeToggle)

Lazy chunks:
  - AdvancedMode.js: ~350KB (Fabric.js + canvas tools) — loaded on demand
  - MosaicViewer.js: ~8KB (zoom/pan logic) — loaded on mosaic page
```

---

## 5. CSS Architecture

Tailwind CSS with custom design tokens:

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#6C5CE7', hover: '#5A4BD4' },
        secondary: '#FF6B35',
        surface: '#F8F7FF',
        'text-primary': '#2D2D3F',
        'text-secondary': '#6B6B80',
        success: '#00C48C',
        error: '#FF4757',
      },
      fontFamily: {
        heading: ['Inter', 'sans-serif'],
        prompt: ['Playfair Display', 'serif'],
      },
      borderRadius: {
        card: '12px',
        button: '8px',
      },
    },
  },
};
```

---

## 6. Accessibility Implementation

| Element | Implementation |
|---------|---------------|
| Emoji grid | `role="radiogroup"` with `role="radio"` buttons; `aria-checked` |
| Color palette | Same as emoji grid; `aria-label` with color name |
| Drawing canvas | `aria-label="Drawing canvas"` + instructions text; simple mode as accessible alternative |
| Live counter | `aria-live="polite"` region |
| Share buttons | Descriptive `aria-label` ("Share on Twitter") |
| Mode toggle | `role="tablist"` with `role="tab"` + `aria-selected` |
| Images | `alt` text: contribution → "Creative piece: [prompt]"; mosaic → "Community mosaic for [date]" |
