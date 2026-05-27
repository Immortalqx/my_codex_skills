# auto_drawio bridge reference

Use this reference when a workspace contains `auto_presentation/auto_drawio`.

## Locate bridge

Prefer a user-provided path. Otherwise look in:

- `<workspace>/output/auto_presentation/auto_drawio`
- `<workspace>/auto_presentation/auto_drawio`
- any nearby `auto_drawio` directory

Do not hard-code private paths into generated artifacts.

## Connect a target `.drawio`

From the `auto_drawio` directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\connect-bridge.ps1 -Port 4318 -DiagramPath "<absolute-path-to-file.drawio>"
```

The bridge URL is usually:

```text
http://127.0.0.1:4318/
```

Use `connect-bridge.ps1` instead of manually editing config files, especially on Windows paths with non-ASCII characters.

## Inspect target

```powershell
node .\scripts\inspect-target.mjs --port 4318
```

## Layout preferences

- Compact layout without large blank areas.
- Align same-level modules.
- Prefer orthogonal connectors and minimize crossings.
- Preserve human-edited layout unless the user asks for a full redesign.
- Use draw.io for semantic structure; use GPT-Image-2 for visual style.
