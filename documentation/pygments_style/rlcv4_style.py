from pygments.style import Style
from pygments.token import (
    Token, Comment, Keyword, Name,
    Number, Operator, Punctuation, String, Generic, Error,
)


class RefinedStyle(Style):
    """
    Frost variant — cool blue-white background, #ff5500 accent.
    Keywords dark burnt-orange; types/functions blue; numbers accent; comments muted blue-gray.
    """
    background_color = "#f2f6fb"
    default_style    = "#1a2030"

    styles = {
        Token:                  "#1a2030",

        Comment:                "italic #3a5a6a",
        Comment.Preproc:        "#6a8898",

        Keyword:                "bold #d94400",
        Keyword.Type:           "#2255aa",       # uint8_t, int, void …
        Keyword.Constant:       "#ff5500",        # true, false, nullptr

        Name:                   "#1a2030",
        Name.Function:          "#2255aa",
        Name.Class:             "bold #2255aa",
        Name.Builtin:           "#2255aa",
        Name.Constant:          "#8833aa",        # EVT_* ALL_CAPS macros
        Name.Decorator:         "#d94400",
        Name.Namespace:         "#8898a8",        # std:: — muted
        Name.Variable:          "#1a2030",
        Name.Attribute:         "#2255aa",

        String:                 "#1e6b35",
        String.Escape:          "bold #ff5500",

        Number:                 "#ff5500",        # accent — reserved for literals
        Number.Integer:         "#ff5500",
        Number.Hex:             "#ff5500",
        Number.Float:           "#ff5500",
        Number.Oct:             "#ff5500",

        Operator:               "#4a5a6a",
        Operator.Word:          "bold #d94400",

        Punctuation:           "#4a5a6a",

        Generic.Heading:        "bold #1a2030",
        Generic.Subheading:     "#d94400",
        Generic.Deleted:        "#cc0000",
        Generic.Inserted:       "#336644",
        Generic.Error:          "#cc0000",
        Generic.Traceback:      "#cc0000",

        Error:                  "bg:#dde8f8 #cc0000",
    }