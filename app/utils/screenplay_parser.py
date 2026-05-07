import re

from markupsafe import Markup, escape


def screenplay_to_html(text: str) -> str:
    """Convert raw screenplay text to HTML with CSS classes."""
    if not text:
        return Markup("")

    lines = text.split("\n")
    out = []
    state = "action"  # tracks current context: action | character | dialogue | parenthetical

    for raw in lines:
        s = raw.strip()

        if not s:
            if state in ("character",):
                state = "action"
            elif state == "dialogue":
                state = "action"
            out.append('<span class="sp-blank"></span>')
            continue

        # Transitions (FADE IN:, CUT TO:, etc.) — must end with : or .
        if re.match(
            r"^(FADE IN|FADE OUT|FADE TO|CUT TO|SMASH CUT|MATCH CUT|DISSOLVE TO|IRIS IN|IRIS OUT)",
            s,
        ) and (s.endswith(":") or s.endswith(".")):
            out.append(f'<p class="transition">{escape(s)}</p>')
            state = "action"
            continue

        # Scene headings
        if re.match(r"^(INT\.|EXT\.|INT/EXT\.|I/E\.)\s", s, re.IGNORECASE):
            out.append(f'<p class="scene-heading">{escape(s.upper())}</p>')
            state = "action"
            continue

        # Parenthetical (only inside character/dialogue context)
        if (
            s.startswith("(")
            and s.endswith(")")
            and state in ("character", "dialogue", "parenthetical")
        ):
            out.append(f'<p class="parenthetical">{escape(s)}</p>')
            state = "parenthetical"
            continue

        # Character name: all caps, short, no trailing period (not a sentence), not a scene heading
        if (
            state == "action"
            and s == s.upper()
            and len(s) <= 38
            and re.match(r"^[A-Z][A-Z0-9 '\-\(\)\.]*$", s)
            and not re.match(r"^(INT\.|EXT\.)", s)
        ):
            out.append(f'<p class="character">{escape(s)}</p>')
            state = "character"
            continue

        # Dialogue (follows character, parenthetical, or continuing dialogue)
        if state in ("character", "parenthetical", "dialogue"):
            out.append(f'<p class="dialogue">{escape(s)}</p>')
            state = "dialogue"
            continue

        # Default: action
        out.append(f'<p class="action">{escape(s)}</p>')
        state = "action"

    return Markup("\n".join(out))
