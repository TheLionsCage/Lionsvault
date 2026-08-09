# LiONsVAULT Tagging System

## Principles

LiONsVAULT keeps Apple Photos and automatically created application albums intact. Albums are treated as useful metadata rather than folders to reorganize.

## Tag layers

### `topic:`
Semantic meaning derived primarily from recognized text.

Examples:
- `topic:success`
- `topic:motivation`
- `topic:heartbreak`
- `topic:leadership`
- `topic:marketing`
- `topic:ai`
- `topic:techno`

### `content:`
Visible image/video-preview motifs derived from Apple Vision labels or safe album signals.

Examples:
- `content:car`
- `content:night_drive`
- `content:rain`
- `content:streetlights`
- `content:warehouse`
- `content:stage`
- `content:hotel`

### `source:`
Known origin or Apple media subtype.

Examples:
- `source:capcut`
- `source:tiktok`
- `source:instagram`
- `source:whatsapp`
- `source:screenshot`
- `source:livephoto`
- `source:animated`

### `project:`
Known project context from reliable metadata such as album membership.

Examples:
- `project:lionscage`
- `project:lionstech`
- `project:mc5`

### `quality:`
Usability/status hints.

Examples:
- `quality:no_watermark`
- `quality:watermark`
- `quality:clean`
- `quality:ui`

## Identity rule

LiONsVAULT must not infer named identities such as David, Vanessa or a specific artist/project from generic visual labels like `man`, `woman` or `portrait`. Named identities require a reliable explicit source before being tagged.

## Quote handling

OCR text can create `content:text`. A text image becomes `content:quote_candidate` only when sufficient text and a relevant semantic topic are present. This deliberately avoids treating every screenshot or UI screen as a quote.

## Privacy

Recognized text and Apple Photos asset identifiers remain in the local JSON/CSV index. Generated index files are excluded from the public repository.
