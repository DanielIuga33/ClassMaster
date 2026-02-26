import tkinter as tk


def validate_roman_entry(char):
    """Permite doar caracterele romane valide."""
    allowed_chars = "IVXivx"
    return char in allowed_chars


def to_uppercase(widget):
    """Transformă textul în majuscule în timp real."""
    pos = widget.index(tk.INSERT)
    current_text = widget.get().upper()
    widget.delete(0, tk.END)
    widget.insert(0, current_text)
    widget.icursor(pos)


def get_colors_by_name(name):
    if name == "classic_dark":
        return {
            "bg": "#121212", "sidebar_bg": "#1E1E1E", "fg": "#FFFFFF",
            "card_bg": "#1E1E1E", "input_bg": "#2C2C2C", "hover": "#333333",
            "grid_line": "#333333", "accent": "#4A90E2", "success": "#2ECC71", "danger": "#E74C3C",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1B3D2F", "schedule_past_fg": "#A5D6A7",
            "schedule_today_bg": "#1A237E", "schedule_today_fg": "#E8EAF6",
            "schedule_future_bg": "#3D3A1B", "schedule_future_fg": "#FFF59D",
            "header_today_bg": "#0984E3"
        }
    elif name in ["dark_start", "dark"]:
        return {
            "bg": "#18191A", "sidebar_bg": "#242526", "fg": "#E4E6EB",
            "card_bg": "#242526", "input_bg": "#3A3B3C", "hover": "#3E4042",
            "grid_line": "#3E4042", "accent": "#007BFF", "success": "#059669", "danger": "#E74C3C",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#143026", "schedule_past_fg": "#A7F3D0",
            "schedule_today_bg": "#1E3A8A", "schedule_today_fg": "#DBEAFE",
            "schedule_future_bg": "#422006", "schedule_future_fg": "#FEF3C7",
            "header_today_bg": "#1D4ED8"
        }
    elif name == "midnight_blue":
        return {
            "bg": "#0B0E14", "sidebar_bg": "#151921", "fg": "#D1D5DB",
            "card_bg": "#151921", "input_bg": "#1F2937", "hover": "#2D3748",
            "grid_line": "#2D3748", "accent": "#6366F1", "success": "#10B981", "danger": "#EF4444",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#064E3B", "schedule_past_fg": "#D1FAE5",
            "schedule_today_bg": "#312E81", "schedule_today_fg": "#E0E7FF",
            "schedule_future_bg": "#78350F", "schedule_future_fg": "#FEF3C7",
            "header_today_bg": "#4338CA"
            }
    elif name == "dracula":
        return {
            "bg": "#282A36", "sidebar_bg": "#21222C", "fg": "#F8F8F2",
            "card_bg": "#21222C", "input_bg": "#44475A", "hover": "#6272A4",
            "grid_line": "#44475A", "accent": "#BD93F9", "success": "#50FA7B", "danger": "#FF5555",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#234135", "schedule_past_fg": "#50FA7B",
            "schedule_today_bg": "#3A3052", "schedule_today_fg": "#F8F8F2",
            "schedule_future_bg": "#4D462E", "schedule_future_fg": "#F1FA8C",
            "header_today_bg": "#6272A4"
        }
    elif name == "tokyo_night":
        return {
            "bg": "#1A1B26", "sidebar_bg": "#16161E", "fg": "#A9B1D6",
            "card_bg": "#16161E", "input_bg": "#24283B", "hover": "#292E42",
            "grid_line": "#292E42", "accent": "#7AA2F7", "success": "#9ECE6A", "danger": "#F7768E",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#23332B", "schedule_past_fg": "#9ECE6A",
            "schedule_today_bg": "#1E223A", "schedule_today_fg": "#7AA2F7",
            "schedule_future_bg": "#332F2A", "schedule_future_fg": "#E0AF68",
            "header_today_bg": "#3D59A1"
        }
    elif name == "cyberpunk":
        return {
            "bg": "#000505", "sidebar_bg": "#000000", "fg": "#00FF9F",
            "card_bg": "#0D0D0D", "input_bg": "#1A1A1A", "hover": "#333333",
            "grid_line": "#00FF9F", "accent": "#FF0055", "success": "#00FF9F", "danger": "#FFFF00",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#002B1A", "schedule_past_fg": "#00FF9F",
            "schedule_today_bg": "#2B001A", "schedule_today_fg": "#FF0055",
            "schedule_future_bg": "#2B2B00", "schedule_future_fg": "#FFFF00",
            "header_today_bg": "#FF0055"
        }
    elif name == "dark_oled":
        return {
            "bg": "#000000", "sidebar_bg": "#000000", "fg": "#FFFFFF",
            "card_bg": "#121212", "input_bg": "#1A1A1A", "hover": "#222222",
            "grid_line": "#333333", "accent": "#BB86FC", "success": "#03DAC6", "danger": "#CF6679",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#03302C", "schedule_past_fg": "#03DAC6",
            "schedule_today_bg": "#251B33", "schedule_today_fg": "#BB86FC",
            "schedule_future_bg": "#332E1B", "schedule_future_fg": "#F1C40F",
            "header_today_bg": "#3700B3"
        }
    elif name in ["classic_light", "light"]:
        return {
            "bg": "#F8F9FA", "sidebar_bg": "#FFFFFF", "fg": "#2D3436",
            "card_bg": "#FFFFFF", "input_bg": "#F0F2F5", "hover": "#EEEEEE",
            "grid_line": "#D1D8E0", "accent": "#4A90E2", "success": "#2ECC71", "danger": "#E74C3C",
            "schedule_text": "#000000",
            "schedule_past_bg": "#E8F5E9", "schedule_past_fg": "#2E7D32",
            "schedule_today_bg": "#D1E3FF", "schedule_today_fg": "#0D47A1",
            "schedule_future_bg": "#FFFDE7", "schedule_future_fg": "#F9A825",
            "header_today_bg": "#00CEC9"
        }
    elif name == "nordic_frost":
        return {
            "bg": "#F3F9FB", "sidebar_bg": "#E1EBF2", "fg": "#2C3E50",
            "card_bg": "#FFFFFF", "input_bg": "#E1EBF2", "hover": "#D1DEE8",
            "grid_line": "#CAD6E0", "accent": "#3498DB", "success": "#27AE60", "danger": "#E74C3C",
            "schedule_text": "#000000",
            "schedule_past_bg": "#D4EFDF", "schedule_past_fg": "#1E8449",
            "schedule_today_bg": "#D6EAF8", "schedule_today_fg": "#21618C",
            "schedule_future_bg": "#FCF3CF", "schedule_future_fg": "#9A7D0A",
            "header_today_bg": "#2E86C1"
        }
    elif name == "github_light":
        return {
            "bg": "#FFFFFF", "sidebar_bg": "#F6F8FA", "fg": "#24292F",
            "card_bg": "#FFFFFF", "input_bg": "#F6F8FA", "hover": "#F3F4F6",
            "grid_line": "#D0D7DE", "accent": "#0969DA", "success": "#1A7F37", "danger": "#CF222E",
            "schedule_text": "#000000",
            "schedule_past_bg": "#DAFBE1", "schedule_past_fg": "#1A7F37",
            "schedule_today_bg": "#DDF4FF", "schedule_today_fg": "#0969DA",
            "schedule_future_bg": "#FFF8C5", "schedule_future_fg": "#9A6700",
            "header_today_bg": "#54AEFF"
        }
    elif name == "sakura_blossom":
        return {
            "bg": "#FFF5F7", "sidebar_bg": "#FFE4E8", "fg": "#5D2E36",
            "card_bg": "#FFFFFF", "input_bg": "#FFE4E8", "hover": "#FFD1D9",
            "grid_line": "#FAD0D8", "accent": "#FF8A9D", "success": "#77DD77", "danger": "#FF6961",
            "schedule_text": "#000000",
            "schedule_past_bg": "#E2F3E2", "schedule_past_fg": "#4CAF50",
            "schedule_today_bg": "#FCE4EC", "schedule_today_fg": "#C2185B",
            "schedule_future_bg": "#FFF9C4", "schedule_future_fg": "#FBC02D",
            "header_today_bg": "#FF8A9D"
        }
    elif name == "rosea_dark":
        return {
            "bg": "#1A1617", "sidebar_bg": "#2D2426", "fg": "#F8E1E5",
            "card_bg": "#2D2426", "input_bg": "#3D3133", "hover": "#4D3F41",
            "grid_line": "#4D3F41", "accent": "#FF79C6", "success": "#50FA7B", "danger": "#FF5555",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#253128", "schedule_past_fg": "#50FA7B",
            "schedule_today_bg": "#3D2431", "schedule_today_fg": "#FF79C6",
            "schedule_future_bg": "#3D3A24", "schedule_future_fg": "#F1FA8C",
            "header_today_bg": "#BD93F9"
        }
    elif name == "lavender_mist":
        return {
            "bg": "#F3F0F9", "sidebar_bg": "#E6E1F3", "fg": "#4A4458",
            "card_bg": "#FFFFFF", "input_bg": "#E6E1F3", "hover": "#DCD4ED",
            "grid_line": "#D1C9E7", "accent": "#9B89B3", "success": "#8FCB9B", "danger": "#E57373",
            "schedule_text": "#000000",
            "schedule_past_bg": "#E8F5E9", "schedule_past_fg": "#2E7D32",
            "schedule_today_bg": "#F3E5F5", "schedule_today_fg": "#6A1B9A",
            "schedule_future_bg": "#FFFDE7", "schedule_future_fg": "#F9A825",
            "header_today_bg": "#9B89B3"
        }
    elif name == "cotton_candy":
        return {
            "bg": "#F0F4FF", "sidebar_bg": "#E0E9FF", "fg": "#5B6A8E",
            "card_bg": "#FFFFFF", "input_bg": "#FDE7F3", "hover": "#FAD4E9",
            "grid_line": "#E0E9FF", "accent": "#F49AC2", "success": "#A0E7E5", "danger": "#FFABAB",
            "schedule_text": "#000000",
            "schedule_past_bg": "#E0F2F1", "schedule_past_fg": "#00796B",
            "schedule_today_bg": "#FCE4EC", "schedule_today_fg": "#C2185B",
            "schedule_future_bg": "#E1F5FE", "schedule_future_fg": "#0277BD",
            "header_today_bg": "#F49AC2"
        }
    elif name == "coffee_shop":
        return {
            "bg": "#F5F5DC", "sidebar_bg": "#EBDCB2", "fg": "#4B3621",
            "card_bg": "#FAF9F6", "input_bg": "#EBDCB2", "hover": "#D9C5A3",
            "grid_line": "#C1A173", "accent": "#6F4E37", "success": "#606C38", "danger": "#BC6C25",
            "schedule_text": "#000000",
            "schedule_past_bg": "#DED9C4", "schedule_past_fg": "#606C38",
            "schedule_today_bg": "#D7CCC8", "schedule_today_fg": "#5D4037",
            "schedule_future_bg": "#F5F5F5", "schedule_future_fg": "#795548",
            "header_today_bg": "#8D6E63"
        }
    elif name == "dark_emerald":
        return {
            "bg": "#18191A", "sidebar_bg": "#242526", "fg": "#E4E6EB",
            "card_bg": "#242526", "input_bg": "#3A3B3C", "hover": "#3E4042",
            "grid_line": "#3E4042", "accent": "#374151", "success": "#059669", "danger": "#E74C3C",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#064E3B", "schedule_past_fg": "#A7F3D0",
            "schedule_today_bg": "#312E81", "schedule_today_fg": "#E0E7FF",
            "schedule_future_bg": "#3D2B1F", "schedule_future_fg": "#FDE68A",
            "header_today_bg": "#059669"
        }
    elif name == "forest_dark":
        return {
            "bg": "#0D1111", "sidebar_bg": "#161B1B", "fg": "#ECF1F1",
            "card_bg": "#161B1B", "input_bg": "#232A2A", "hover": "#2D3737",
            "grid_line": "#2D3737", "accent": "#00B894", "success": "#55E6C1", "danger": "#FC427B",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#0A2F28", "schedule_past_fg": "#55E6C1",
            "schedule_today_bg": "#102533", "schedule_today_fg": "#81ECEC",
            "schedule_future_bg": "#2D2616", "schedule_future_fg": "#FFEAA7",
            "header_today_bg": "#00B894"
        }
    elif name == "material_ocean":
        return {
            "bg": "#0F111A", "sidebar_bg": "#090B10", "fg": "#8F93A2",
            "card_bg": "#090B10", "input_bg": "#1A1C25", "hover": "#24262E",
            "grid_line": "#1A1C25", "accent": "#82AAFF", "success": "#C3E88D", "danger": "#FF5370",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1E2D24", "schedule_past_fg": "#C3E88D",
            "schedule_today_bg": "#1A1C32", "schedule_today_fg": "#82AAFF",
            "schedule_future_bg": "#2D2A1E", "schedule_future_fg": "#FFCB6B",
            "header_today_bg": "#3F51B5"
        }
    elif name == "nordic_frost":
        return {
            "bg": "#F3F9FB", "sidebar_bg": "#E1EBF2", "fg": "#2C3E50",
            "card_bg": "#FFFFFF", "input_bg": "#E1EBF2", "hover": "#D1DEE8",
            "grid_line": "#CAD6E0", "accent": "#3498DB", "success": "#27AE60", "danger": "#E74C3C",
            "schedule_text": "#000000",
            "schedule_past_bg": "#D4EFDF", "schedule_past_fg": "#1E8449",
            "schedule_today_bg": "#D6EAF8", "schedule_today_fg": "#21618C",
            "schedule_future_bg": "#FCF3CF", "schedule_future_fg": "#9A7D0A",
            "header_today_bg": "#2E86C1"
        }
    elif name == "light_soft":
        return {
            "bg": "#FDF6E3", "sidebar_bg": "#EEE8D5", "fg": "#586E75",
            "card_bg": "#FDF6E3", "input_bg": "#EEE8D5", "hover": "#E0D9C1",
            "grid_line": "#D5D0BA", "accent": "#B58900", "success": "#859900", "danger": "#DC322F",
            "schedule_text": "#000000",
            "schedule_past_bg": "#F0F4E1", "schedule_past_fg": "#859900",
            "schedule_today_bg": "#E2EAF1", "schedule_today_fg": "#268BD2",
            "schedule_future_bg": "#F9EBD3", "schedule_future_fg": "#B58900",
            "header_today_bg": "#B58900"
        }
    elif name == "solarized_light":
        return {
            "bg": "#FDF6E3", "sidebar_bg": "#EEE8D5", "fg": "#657B83",
            "card_bg": "#FCF9ED", "input_bg": "#EEE8D5", "hover": "#E5DFCC",
            "grid_line": "#D5D0BA", "accent": "#268BD2", "success": "#859900", "danger": "#DC322F",
            "schedule_text": "#000000",
            "schedule_past_bg": "#E9EFD1", "schedule_past_fg": "#859900",
            "schedule_today_bg": "#D1E4F2", "schedule_today_fg": "#268BD2",
            "schedule_future_bg": "#F7E6D2", "schedule_future_fg": "#CB4B16",
            "header_today_bg": "#268BD2"
        }
    elif name == "retro_terminal":
        return {
            "bg": "#0C0C0C", "sidebar_bg": "#161616", "fg": "#10FF00",
            "card_bg": "#161616", "input_bg": "#212121", "hover": "#2A2A2A",
            "grid_line": "#10FF00", "accent": "#33FF33", "success": "#00FF00", "danger": "#FF0000",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#062106", "schedule_past_fg": "#10FF00",
            "schedule_today_bg": "#1B1B1B", "schedule_today_fg": "#FFFFFF",
            "schedule_future_bg": "#212100", "schedule_future_fg": "#FFFF00",
            "header_today_bg": "#10FF00"
        }
    elif name == "ocean_sunset":
        return {
            "bg": "#1A1A2E", "sidebar_bg": "#16213E", "fg": "#E94560",
            "card_bg": "#0F3460", "input_bg": "#16213E", "hover": "#533483",
            "grid_line": "#533483", "accent": "#E94560", "success": "#00D2D3", "danger": "#FF4757",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#0F4C5C", "schedule_past_fg": "#00D2D3",
            "schedule_today_bg": "#1A1A40", "schedule_today_fg": "#FFFFFF",
            "schedule_future_bg": "#5F3741", "schedule_future_fg": "#E94560",
            "header_today_bg": "#E94560"
            }
    elif name == "nord_deep":
        return {
            "bg": "#2E3440", "sidebar_bg": "#242933", "fg": "#D8DEE9",
            "card_bg": "#3B4252", "input_bg": "#434C5E", "hover": "#4C566A",
            "grid_line": "#4C566A", "accent": "#88C0D0", "success": "#A3BE8C", "danger": "#BF616A",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#3B4252", "schedule_past_fg": "#A3BE8C",
            "schedule_today_bg": "#2E3440", "schedule_today_fg": "#88C0D0",
            "schedule_future_bg": "#434C5E", "schedule_future_fg": "#EBCB8B",
            "header_today_bg": "#81A1C1"
        }
    elif name == "monokai_pro":
        return {
            "bg": "#2D2A2E", "sidebar_bg": "#221F22", "fg": "#FCFCFA",
            "card_bg": "#221F22", "input_bg": "#403E41", "hover": "#5B595C",
            "grid_line": "#403E41", "accent": "#FFD866", "success": "#A9DC76", "danger": "#FF6188",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#373B30", "schedule_past_fg": "#A9DC76",
            "schedule_today_bg": "#303541", "schedule_today_fg": "#78DCE8",
            "schedule_future_bg": "#41363A", "schedule_future_fg": "#FC9867",
            "header_today_bg": "#AB9DF2"
        }
    elif name == "everforest_dark":
        return {
            "bg": "#2D353B", "sidebar_bg": "#232A2E", "fg": "#D3C6AA",
            "card_bg": "#232A2E", "input_bg": "#343F44", "hover": "#3D484D",
            "grid_line": "#3D484D", "accent": "#A7C080", "success": "#A7C080", "danger": "#E67E80",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#323C41", "schedule_past_fg": "#A7C080",
            "schedule_today_bg": "#3A4B59", "schedule_today_fg": "#7FBBB3",
            "schedule_future_bg": "#4A463B", "schedule_future_fg": "#DBBC7F",
            "header_today_bg": "#D699B6"
        }
    elif name == "deep_sea":
        return {
            "bg": "#011627", "sidebar_bg": "#010E1A", "fg": "#D6DEEB",
            "card_bg": "#010E1A", "input_bg": "#0B2942", "hover": "#123E5A",
            "grid_line": "#123E5A", "accent": "#82AAFF", "success": "#22DA6E", "danger": "#EF5350",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#122D30", "schedule_past_fg": "#22DA6E",
            "schedule_today_bg": "#1A254D", "schedule_today_fg": "#82AAFF",
            "schedule_future_bg": "#3D3728", "schedule_future_fg": "#ADDB67",
            "header_today_bg": "#7F7AF3"
        }
    elif name == "nord_light":
        return {
            "bg": "#ECEFF4", "sidebar_bg": "#E5E9F0", "fg": "#2E3440",
            "card_bg": "#FFFFFF", "input_bg": "#E5E9F0", "hover": "#D8DEE9",
            "grid_line": "#D8DEE9", "accent": "#5E81AC", "success": "#A3BE8C", "danger": "#BF616A",
            "schedule_text": "#000000",
            "schedule_past_bg": "#EDF4E9", "schedule_past_fg": "#4F7336",
            "schedule_today_bg": "#E1E9F0", "schedule_today_fg": "#5E81AC",
            "schedule_future_bg": "#F5EFE0", "schedule_future_fg": "#8F6E2B",
            "header_today_bg": "#81A1C1"
        }
    elif name == "vibrant_purple":
        return {
            "bg": "#120B1A", "sidebar_bg": "#1A1125", "fg": "#E9D5FF",
            "card_bg": "#1A1125", "input_bg": "#2A1B3D", "hover": "#3B2654",
            "grid_line": "#3B2654", "accent": "#A855F7", "success": "#22C55E", "danger": "#EF4444",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#142E1F", "schedule_past_fg": "#4ADE80",
            "schedule_today_bg": "#2E1065", "schedule_today_fg": "#D8B4FE",
            "schedule_future_bg": "#422006", "schedule_future_fg": "#FDE68A",
            "header_today_bg": "#9333EA"
        }
    elif name == "sepia_paper":
        return {
            "bg": "#F4ECD8", "sidebar_bg": "#EADFCA", "fg": "#433422",
            "card_bg": "#F9F4E8", "input_bg": "#EADFCA", "hover": "#DBCFB6",
            "grid_line": "#D3C2A3", "accent": "#8B4513", "success": "#4F6F52", "danger": "#A04747",
            "schedule_text": "#433422",
            "schedule_past_bg": "#E3EDD3", "schedule_past_fg": "#3A5A40",
            "schedule_today_bg": "#D6E4F0", "schedule_today_fg": "#2D4B73",
            "schedule_future_bg": "#F0EAD6", "schedule_future_fg": "#A67B5B",
            "header_today_bg": "#A67B5B"
        }
    elif name == "catppuccin":
        return {
            "bg": "#24273A", "sidebar_bg": "#1E2030", "fg": "#CAD3F5",
            "card_bg": "#1E2030", "input_bg": "#363A4F", "hover": "#494D64",
            "grid_line": "#494D64", "accent": "#8AADF4", "success": "#A6DA95", "danger": "#ED8796",
            "schedule_text": "#CAD3F5",
            "schedule_past_bg": "#2D3F36", "schedule_past_fg": "#A6DA95",
            "schedule_today_bg": "#313958", "schedule_today_fg": "#8AADF4",
            "schedule_future_bg": "#463E33", "schedule_future_fg": "#EED49F",
            "header_today_bg": "#C6A0F6"
        }
    elif name == "space_gray":
        return {
            "bg": "#2B303B", "sidebar_bg": "#232830", "fg": "#C0C5CE",
            "card_bg": "#232830", "input_bg": "#343D46", "hover": "#4F5B66",
            "grid_line": "#4F5B66", "accent": "#65737E", "success": "#99C794", "danger": "#EC5F67",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#2E3D35", "schedule_past_fg": "#99C794",
            "schedule_today_bg": "#2D3E4F", "schedule_today_fg": "#6699CC",
            "schedule_future_bg": "#433D2D", "schedule_future_fg": "#FAC863",
            "header_today_bg": "#AB7967"
        }
    elif name == "night_owl":
        return {
            "bg": "#011627", "sidebar_bg": "#01111D", "fg": "#D6DEEB",
            "card_bg": "#01111D", "input_bg": "#0B2942", "hover": "#123E5A",
            "grid_line": "#123E5A", "accent": "#7FDBCA", "success": "#ADDB67", "danger": "#EF5350",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#122D30", "schedule_past_fg": "#ADDB67",
            "schedule_today_bg": "#1A254D", "schedule_today_fg": "#82AAFF",
            "schedule_future_bg": "#3D3728", "schedule_future_fg": "#ECC48D",
            "header_today_bg": "#C792EA"
        }
    elif name == "synthwave":
        return {
            "bg": "#262335", "sidebar_bg": "#241B2F", "fg": "#FFFFFF",
            "card_bg": "#241B2F", "input_bg": "#34294F", "hover": "#443566",
            "grid_line": "#FF7EDB", "accent": "#F97E72", "success": "#72F1B8", "danger": "#FE4450",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1E3A3A", "schedule_past_fg": "#72F1B8",
            "schedule_today_bg": "#2A1E3D", "schedule_today_fg": "#FF7EDB",
            "schedule_future_bg": "#3D352A", "schedule_future_fg": "#FEDE5D",
            "header_today_bg": "#03E8F3"
        }
    elif name == "aura_dark":
        return {
            "bg": "#15141B", "sidebar_bg": "#111016", "fg": "#EDECEE",
            "card_bg": "#111016", "input_bg": "#1C1B22", "hover": "#292631",
            "grid_line": "#292631", "accent": "#A277FF", "success": "#61FFCA", "danger": "#FF6767",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1E2D28", "schedule_past_fg": "#61FFCA",
            "schedule_today_bg": "#221E3D", "schedule_today_fg": "#A277FF",
            "schedule_future_bg": "#302B1E", "schedule_future_fg": "#FFCA85",
            "header_today_bg": "#61FFCA"
        }
    elif name == "gruvbox_dark":
        return {
            "bg": "#282828", "sidebar_bg": "#1D2021", "fg": "#D4BE98",
            "card_bg": "#1D2021", "input_bg": "#32302F", "hover": "#3C3836",
            "grid_line": "#3C3836", "accent": "#7DAEA3", "success": "#A9B665", "danger": "#EA6962",
            "schedule_text": "#D4BE98",
            "schedule_past_bg": "#32361A", "schedule_past_fg": "#A9B665",
            "schedule_today_bg": "#263035", "schedule_today_fg": "#7DAEA3",
            "schedule_future_bg": "#413020", "schedule_future_fg": "#D8A657",
            "header_today_bg": "#D3869B"
        }
    elif name == "nordic_night":
        return {
            "bg": "#1A1C23", "sidebar_bg": "#16161E", "fg": "#D8DEE9",
            "card_bg": "#16161E", "input_bg": "#24283B", "hover": "#2F334D",
            "grid_line": "#2F334D", "accent": "#81A1C1", "success": "#A3BE8C", "danger": "#BF616A",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#23332B", "schedule_past_fg": "#A3BE8C",
            "schedule_today_bg": "#1E223A", "schedule_today_fg": "#88C0D0",
            "schedule_future_bg": "#332F2A", "schedule_future_fg": "#EBCB8B",
            "header_today_bg": "#5E81AC"
        }
    elif name == "rose_pine_moon":
        return {
            "bg": "#232136", "sidebar_bg": "#1F1D2E", "fg": "#E0DEF4",
            "card_bg": "#1F1D2E", "input_bg": "#2A273F", "hover": "#393552",
            "grid_line": "#393552", "accent": "#C4A7E7", "success": "#9CCFD8", "danger": "#EB6F92",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#243337", "schedule_past_fg": "#9CCFD8",
            "schedule_today_bg": "#2D2845", "schedule_today_fg": "#C4A7E7",
            "schedule_future_bg": "#3E3639", "schedule_future_fg": "#F6C177",
            "header_today_bg": "#EBBCBA"
        }
    elif name == "oxocarbon":
        return {
            "bg": "#161616", "sidebar_bg": "#0D0D0D", "fg": "#DDE1E6",
            "card_bg": "#0D0D0D", "input_bg": "#262626", "hover": "#393939",
            "grid_line": "#393939", "accent": "#BE95FF", "success": "#42BE65", "danger": "#FF7EB6",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#122D1B", "schedule_past_fg": "#42BE65",
            "schedule_today_bg": "#231B33", "schedule_today_fg": "#BE95FF",
            "schedule_future_bg": "#332616", "schedule_future_fg": "#82CFFF",
            "header_today_bg": "#EE5396"
        }
    elif name == "erebus":
        return {
            "bg": "#0A0A0A", "sidebar_bg": "#050505", "fg": "#E0E0E0",
            "card_bg": "#050505", "input_bg": "#1A1A1A", "hover": "#252525",
            "grid_line": "#252525", "accent": "#D4AF37", "success": "#85BB65", "danger": "#B22222",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1A241A", "schedule_past_fg": "#85BB65",
            "schedule_today_bg": "#1A1A24", "schedule_today_fg": "#D4AF37",
            "schedule_future_bg": "#241A1A", "schedule_future_fg": "#CD7F32",
            "header_today_bg": "#C0C0C0"
        }
    elif name == "forest_stream":
        return {
            "bg": "#0B1212", "sidebar_bg": "#080D0D", "fg": "#9DB7B7",
            "card_bg": "#080D0D", "input_bg": "#141F1F", "hover": "#1D2E2E",
            "grid_line": "#1D2E2E", "accent": "#4DB6AC", "success": "#81C784", "danger": "#E57373",
            "schedule_text": "#FFFFFF",
            "schedule_past_bg": "#1A2D23", "schedule_past_fg": "#81C784",
            "schedule_today_bg": "#152633", "schedule_today_fg": "#4DB6AC",
            "schedule_future_bg": "#2D261A", "schedule_future_fg": "#D4E157",
            "header_today_bg": "#26A69A"
        }
    return None
