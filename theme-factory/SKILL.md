---
name: theme-factory
description: Theme-selection and theme-application workflow for slides, documents, reports, and lightweight HTML artifacts. Use when Codex should apply one of the bundled curated themes from `themes/`, show the theme showcase, or derive a new theme with coherent colors, fonts, contrast, and repeated visual motifs.
---


# Theme Factory

This skill provides a small library of reusable visual themes. Each bundled theme defines a palette, font pairing, and overall visual direction that can be applied consistently across an artifact.

## Purpose

Use this skill to avoid generic styling. Each theme should provide:

- a cohesive color palette with hex codes,
- a header and body font pairing,
- a distinct visual identity,
- enough consistency that multiple pages or slides feel like one system.

## Usage Instructions

When styling an artifact:

1. Show `theme-showcase.pdf` if the user needs a visual overview of the bundled options.
2. Ask the user to choose a bundled theme or request a new one.
3. Read the chosen theme file from `themes/`.
4. Apply the palette, type choices, and motif consistently across the target artifact.
5. Verify contrast, readability, and consistency before handoff.

## Themes Available

The following 10 themes are available, each showcased in `theme-showcase.pdf`:

1. **Ocean Depths** - Professional and calming maritime theme
2. **Sunset Boulevard** - Warm and vibrant sunset colors
3. **Forest Canopy** - Natural and grounded earth tones
4. **Modern Minimalist** - Clean and contemporary grayscale
5. **Golden Hour** - Rich and warm autumnal palette
6. **Arctic Frost** - Cool and crisp winter-inspired theme
7. **Desert Rose** - Soft and sophisticated dusty tones
8. **Tech Innovation** - Bold and modern tech aesthetic
9. **Botanical Garden** - Fresh and organic garden colors
10. **Midnight Galaxy** - Dramatic and cosmic deep tones

## Theme Details

Each file in `themes/` should be treated as the source of truth for:

- palette,
- typography,
- tone,
- suggested usage patterns.

## Application Process

After a theme is selected:

1. Read the corresponding theme file from `themes/`.
2. Apply the specified colors and fonts consistently.
3. Reuse one or two repeated motifs rather than inventing a new style on every page.
4. Ensure contrast and readability still hold after applying the theme to real content.

## Create your Own Theme

If the user wants a new theme:

1. Pick a dominant mood and target context.
2. Choose one dominant color, one or two supporting colors, and one accent.
3. Choose a header font and a body font that can coexist across the full artifact.
4. Define the motif rules, for example card shapes, border treatment, icon treatment, or image framing.
5. Save the new theme as a Markdown file under `themes/` only if the user wants it preserved in the library.

## Boundaries

- If the artifact already belongs to an existing design system, preserve that system instead of imposing a new theme.
- Do not apply a theme mechanically without checking contrast, density, and typography against the actual content.
