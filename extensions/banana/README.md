# Banana Extension for Claude Repurpose

Integrates [Claude Banana](https://github.com/AgriciDaniel/claude-banana) AI image generation with the Content Repurposing Engine.

## What It Enables

When `/banana` is installed and `--images` flag is used:

- **Quote cards** (5): Visually designed quote graphics from content's best moments
- **Carousel covers**: Bold title slides for Instagram and LinkedIn carousels
- **Social hero images**: Topic-relevant images for Twitter, LinkedIn, Facebook posts

## Image Specs

| Platform | Aspect Ratio | Dimensions |
|----------|-------------|------------|
| Twitter/X | 16:9 | 1600x900 |
| LinkedIn | 1:1 or 4:5 | 1080x1080 or 1080x1350 |
| Instagram | 4:5 | 1080x1350 |
| Facebook | 4:5 | 1080x1350 |
| YouTube Community | 1:1 | 1080x1080 |

## Install

```bash
bash extensions/banana/install.sh
```

## Without /banana

The repurpose skill works fully without this extension. Image generation prompts are saved to `banana-prompts.md` in the output directory for manual use with any image generation tool.
