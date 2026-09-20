"""Design tokens. One place to change the look."""

INK = "#0B0E14"      # panel background
PAPER = "#E8E6E1"    # primary text, data marks
AMBER = "#F5A623"    # values and the single accent
CYAN = "#3FA9F5"     # names of people, nothing else
SLATE = "#5C6470"    # hairlines
MUTED = "#8B93A0"    # secondary text (slate lightened so it passes contrast on INK)

W = 840              # every panel is 840 wide; GitHub scales it down
PAD = 24
RADIUS = 10

MONO = "'JBM', ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

# type scale (px at 840 wide)
T_XS, T_S, T_M, T_L, T_XL = 11, 12, 14, 16, 20
T_NAME = 56
