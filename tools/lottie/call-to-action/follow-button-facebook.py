from _platforms import Platform, build_platform

# Simple Icons "facebook" (CC0; the logo is a trademark of its owner), 24x24 box.
GLYPH = ("M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.10"
         "3a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-"
         "1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-"
         ".287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5"
         ".628 3.874 10.35 9.101 11.647Z")

build_platform(Platform(
    "follow-button-facebook", "Facebook", GLYPH,
    kind="knockout", shape="circle", path_fill="#0866FF", backing=[("ellipse", 12, 12, 23, 23)],
    primary="#0866FF", secondary="#3A3B3C", glass_bg="1d2b4a", tags=["meta"]))
