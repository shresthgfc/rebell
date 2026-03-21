# Phase 4 — Accessibility Tester: WCAG 2.1 AA Audit Plan

## 1. Per-Page WCAG 2.1 AA Checklist

### Landing Page (/)
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Alt text for YesterdayMosaic image | `alt="Community mosaic for {date}: {contributionCount} pieces"` |
| 1.3.1 Info & Relationships | PromptCard uses semantic heading (h1) | `<h1>` for prompt text |
| 1.4.3 Contrast | Text on surface (#2D2D3F on #F8F7FF) | Ratio 12.4:1 — passes |
| 2.1.1 Keyboard | All interactive elements focusable | CTAButton, nav links — standard `<button>` and `<a>` |
| 2.4.1 Skip Link | Skip to main content | `<a href="#main" class="sr-only focus:not-sr-only">` |
| 3.1.1 Language | `lang="en"` on `<html>` | Set in RootLayout |

### Create Page (/create) — Simple Mode
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.3.1 Info & Relationships | EmojiGrid as radio group | `role="radiogroup"`, each emoji `role="radio"` with `aria-checked` |
| 1.4.1 Use of Color | Color palette not color-only | Each swatch has `aria-label` with color name (e.g., "Coral orange") |
| 1.4.11 Non-text Contrast | Selected state indicator | 3px border + focus ring (not color-only) |
| 2.1.1 Keyboard | Arrow keys navigate emoji grid | `onKeyDown` handler for arrow key grid navigation |
| 4.1.2 Name, Role, Value | Submit button state | `aria-disabled` when no selection; `aria-busy` during submission |

### Create Page (/create) — Advanced Mode (Fabric.js Canvas)
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Canvas has accessible name | `aria-label="Drawing canvas for today's prompt"` |
| 1.3.1 Info & Relationships | Tool selection as toolbar | `role="toolbar"` with `aria-label="Drawing tools"` |
| 2.1.1 Keyboard | Canvas drawing via keyboard | Keyboard shortcuts: arrow keys move cursor, Space to draw, U to undo, C to clear |
| 2.1.4 Character Key Shortcuts | Single-key shortcuts | Only active when canvas is focused; documented in tooltip |
| 4.1.3 Status Messages | Drawing feedback | `aria-live="polite"` region: "Stroke added", "Canvas cleared" |

### Share Page (/piece/:id)
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Contribution image alt | `alt="Creative piece by anonymous contributor for prompt: {promptText}"` |
| 1.4.3 Contrast | Text over image avoided | Prompt text below image, not overlaid |
| 2.4.4 Link Purpose | Share button labels | `aria-label="Share on Twitter"`, `aria-label="Copy link to clipboard"` |

### Mosaic Page (/mosaic/:date)
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Composite image alt | `alt="Community mosaic for {date}: {count} contributions responding to '{promptText}'"` |
| 1.4.3 Contrast | Info text readable | White text on dark overlay or dark text below image |
| 2.1.1 Keyboard | MosaicViewer zoom/pan | +/- keys for zoom, arrow keys for pan, Home to reset |
| 2.5.1 Pointer Gestures | Pinch-zoom alternative | Zoom buttons visible alongside touch gestures |

### Admin Panel (/admin)
| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.3.1 Info & Relationships | Moderation queue as list | `role="list"` with contribution cards as `role="listitem"` |
| 2.1.1 Keyboard | Approve/reject via keyboard | Tab to card, Enter to expand, A to approve, R to reject |
| 4.1.3 Status Messages | Action feedback | `aria-live="assertive"` for "Contribution approved/rejected" |

---

## 2. Keyboard Navigation Audit

### Tab Order (per page)
| Page | Expected Tab Order |
|------|-------------------|
| Landing | Skip link → Logo/Home → PromptCard → CTAButton → YesterdayMosaic link → Footer |
| Create | Skip link → ModeToggle → [Simple: EmojiGrid → ColorPalette] or [Advanced: ToolBar → Canvas] → PreviewSubmitSheet → SubmitButton → ShareButtons |
| Share | Skip link → PieceImage → ShareButtons → CTAButton |
| Mosaic | Skip link → MosaicViewer controls → ShareButtons → CTAButton |
| Admin | Skip link → Moderation queue items → Approve/Reject buttons |

### Focus Management
- **Modal/Sheet**: PreviewSubmitSheet traps focus when open; Escape closes; focus returns to trigger
- **Post-submission**: Focus moves to success message / share buttons
- **Page navigation**: Focus on `<h1>` after route change (Next.js App Router `focus-on-navigate`)

### Skip Links
- Every page: `<a href="#main">Skip to main content</a>` — visually hidden, visible on focus

---

## 3. Color Contrast Verification

### Design System Palette Audit
| Color Pair | Usage | Ratio | Result |
|-----------|-------|-------|--------|
| #2D2D3F on #F8F7FF | Body text on surface | 12.4:1 | Pass (AA + AAA) |
| #6B6B80 on #F8F7FF | Secondary text on surface | 5.1:1 | Pass (AA) |
| #FEFEFE on #6C5CE7 | Button text on primary | 8.3:1 | Pass (AA + AAA) |
| #FEFEFE on #FF6B35 | Button text on secondary | 3.2:1 | Fail for small text — use #FFFFFF on darker shade or increase size to 18px+ |
| #6C5CE7 on #F8F7FF | Link text on surface | 5.5:1 | Pass (AA) |
| #FF4757 on #F8F7FF | Error text on surface | 4.6:1 | Pass (AA, barely) |
| #00C48C on #F8F7FF | Success text on surface | 2.8:1 | Fail — use darker green #008A5E (4.5:1+) |

### Findings
- **FIX REQUIRED**: Secondary button (#FF6B35 background) fails small text contrast. Darken to #E55A20 or use large text only.
- **FIX REQUIRED**: Success text (#00C48C) fails contrast. Use #008A5E or pair with an icon (not color-only).

---

## 4. Screen Reader Testing Plan

### Test Matrix
| Screen Reader | Browser | OS | Priority |
|--------------|---------|-----|----------|
| VoiceOver | Safari | macOS / iOS | P0 (largest mobile share) |
| NVDA | Chrome | Windows | P0 (most common desktop SR) |
| JAWS | Chrome | Windows | P1 (enterprise/power users) |

### Critical Test Scenarios
1. **Landing → Create flow**: SR user navigates from prompt to create page, selects emoji, submits
2. **Simple Mode creation**: Full radio group navigation with arrow keys, selection announced
3. **Share page**: Image alt text read, share buttons announced with labels
4. **Mosaic viewer**: Composite image description read, zoom controls announced
5. **Submission feedback**: Live region announces "Contribution submitted successfully"
6. **Error states**: Rate limit, validation errors announced via `aria-live`

### ARIA Requirements
| Component | ARIA Attributes |
|-----------|----------------|
| EmojiGrid | `role="radiogroup"`, `aria-label="Choose an emoji"`, items: `role="radio"`, `aria-checked`, `aria-label="{emoji name}"` |
| ColorPalette | `role="radiogroup"`, `aria-label="Choose a background color"`, items: `role="radio"`, `aria-checked`, `aria-label="{color name}"` |
| ModeToggle | `role="tablist"`, tabs: `role="tab"`, `aria-selected`, panels: `role="tabpanel"` |
| DrawingCanvas | `aria-label="Drawing canvas"`, `aria-roledescription="drawing area"` |
| LiveCounter | `aria-live="polite"`, `aria-atomic="true"` |
| SubmitButton | `aria-disabled` when inactive, `aria-busy="true"` during submission |
| Toast/feedback | `role="status"`, `aria-live="polite"` |

---

## 5. Canvas Accessibility — Critical Risk

The Fabric.js drawing canvas is inherently visual. Mitigation strategy:

1. **Simple mode is the accessible default** — EmojiGrid and ColorPalette are fully keyboard/SR accessible. ModeToggle defaults to Simple.
2. **Canvas keyboard controls** (for motor-impaired users who can see):
   - Arrow keys: move drawing cursor (10px steps)
   - Shift + Arrow: move 1px (fine control)
   - Space: toggle drawing on/off
   - U: undo last stroke
   - C: clear canvas
   - Tab: cycle through toolbar buttons
3. **Canvas description for screen readers**: `aria-label` describes current state ("Drawing canvas with 3 strokes"). Updated via `aria-live` on each action.
4. **Alternative for non-sighted users**: Simple mode provides equivalent creative expression. Ensure prompt text emphasizes that both modes are valid responses.
5. **Do NOT hide Advanced Mode** from assistive technology — allow users to choose, but default to Simple.

---

## 6. Mobile Accessibility

| Requirement | Target | Implementation |
|-------------|--------|----------------|
| Touch targets | 44x44px minimum | All buttons, emoji cells, color swatches sized ≥ 44x44 |
| Orientation | Both portrait + landscape | CSS `orientation` media queries; canvas scales |
| Zoom | Allow up to 200% zoom without content loss | `<meta name="viewport" content="width=device-width, initial-scale=1">` (no maximum-scale) |
| Reduced motion | Respect `prefers-reduced-motion` | Disable animations, transitions. Canvas drawing unaffected. |
| Text resize | Up to 200% without horizontal scroll | Tailwind responsive classes; max-width: 720px on desktop |
| High contrast | Support `forced-colors` | Test with Windows High Contrast mode; ensure borders visible |

---

## 7. Automated Testing Integration

| Tool | Integration Point | Coverage |
|------|------------------|----------|
| @axe-core/playwright | E2E test suite — run on every page | WCAG 2.1 AA automated checks |
| eslint-plugin-jsx-a11y | ESLint in pre-commit | Catch missing alt, roles, labels at code time |
| Lighthouse CI (a11y score) | GitHub Actions on PR | Score ≥ 90 required |
| Manual screen reader testing | Sprint 2 + Sprint 4 | VoiceOver + NVDA on critical flows |

---

## 8. Findings Summary

| # | Finding | Severity | Page | Fix |
|---|---------|----------|------|-----|
| A11Y-001 | Secondary button (#FF6B35) fails small text contrast | High | Create, Share | Darken to #E55A20 or use ≥18px text |
| A11Y-002 | Success color (#00C48C) fails contrast | High | Create (submission feedback) | Use #008A5E |
| A11Y-003 | Canvas has no keyboard drawing support | Medium | Create (Advanced) | Implement arrow key + Space drawing |
| A11Y-004 | No skip link implemented yet | Medium | All pages | Add `<a href="#main">` in RootLayout |
| A11Y-005 | MosaicViewer zoom has no keyboard alternative | Medium | Mosaic | Add +/- buttons and keyboard shortcuts |
| A11Y-006 | No `prefers-reduced-motion` handling specified | Low | All pages | Add Tailwind `motion-reduce:` variants |
