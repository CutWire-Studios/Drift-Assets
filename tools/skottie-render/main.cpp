// Renders Lottie files with Skottie (the renderer Drift uses) to PNG thumbnails or contact sheets.
#include "include/core/SkCanvas.h"
#include "include/core/SkColor.h"
#include "include/core/SkData.h"
#include "include/core/SkImage.h"
#include "include/core/SkSurface.h"
#include "modules/skottie/include/Skottie.h"
#include "modules/skottie/include/SlotManager.h"

#include <png.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

namespace {

struct Logger : skottie::Logger {
    int warnings = 0;
    void log(Level level, const char message[], const char *json) override
    {
        ++warnings;
        std::fprintf(stderr, "%s: %s%s%s\n", level == Level::kError ? "error" : "warning", message,
                     json ? " @ " : "", json ? json : "");
    }
};

// Drift's prebuilt Skia omits SkPngEncoder, so write through libpng directly.
bool writePng(const char *path, SkImage *image)
{
    const int w = image->width(), h = image->height();
    std::vector<uint8_t> rgba(size_t(w) * h * 4);
    const SkImageInfo info = SkImageInfo::Make(w, h, kRGBA_8888_SkColorType, kUnpremul_SkAlphaType);
    if (!image->readPixels(info, rgba.data(), size_t(w) * 4, 0, 0))
        return false;
    FILE *fp = std::fopen(path, "wb");
    if (!fp)
        return false;
    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, nullptr, nullptr, nullptr);
    png_infop pinfo = png_create_info_struct(png);
    if (setjmp(png_jmpbuf(png))) {
        png_destroy_write_struct(&png, &pinfo);
        std::fclose(fp);
        return false;
    }
    png_init_io(png, fp);
    png_set_IHDR(png, pinfo, w, h, 8, PNG_COLOR_TYPE_RGBA, PNG_INTERLACE_NONE, PNG_COMPRESSION_TYPE_DEFAULT,
                 PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png, pinfo);
    for (int y = 0; y < h; ++y)
        png_write_row(png, rgba.data() + size_t(y) * w * 4);
    png_write_end(png, nullptr);
    png_destroy_write_struct(&png, &pinfo);
    std::fclose(fp);
    return true;
}

void usage()
{
    std::fprintf(stderr,
                 "usage: skottie-render IN.json OUT.png [--size N] [--t FRACTION] [--sheet N]\n"
                 "                      [--bg none|checker|RRGGBB] [--pad FRACTION] [--region X,Y,W,H]\n"
                 "                      [--strict]\n"
                 "  --t      normalized time of the frame to render (default 0.5)\n"
                 "  --sheet  render an N x N grid of evenly spaced frames instead of one frame\n"
                 "  --region fit this canvas rectangle instead of the whole canvas (close-up thumbnails)\n"
                 "  --strict exit 2 if Skottie logged any warning\n");
    std::exit(1);
}

void drawBackground(SkCanvas *canvas, const SkRect &r, const std::string &bg)
{
    if (bg == "none")
        return;
    if (bg == "checker") {
        SkPaint a, b;
        a.setColor(SkColorSetRGB(0x3a, 0x3a, 0x42));
        b.setColor(SkColorSetRGB(0x2a, 0x2a, 0x30));
        canvas->drawRect(r, a);
        const float cell = r.width() / 16;
        for (int y = 0; y < 16; ++y)
            for (int x = y % 2; x < 16; x += 2)
                canvas->drawRect(SkRect::MakeXYWH(r.x() + x * cell, r.y() + y * cell, cell, cell), b);
        return;
    }
    SkPaint p;
    p.setColor(SkColorSetRGB(0, 0, 0) | 0xff000000 | uint32_t(std::strtoul(bg.c_str(), nullptr, 16)));
    canvas->drawRect(r, p);
}

void drawFrame(SkCanvas *canvas, skottie::Animation *anim, double t, const SkRect &cell, float pad,
               const std::string &bg, const SkRect &region)
{
    drawBackground(canvas, cell, bg);
    const SkSize s = anim->size();
    const SkRect r = region.isEmpty() ? SkRect::MakeSize(s) : region;
    const SkRect inner = cell.makeInset(cell.width() * pad, cell.height() * pad);
    const float scale = std::min(inner.width() / r.width(), inner.height() / r.height());
    const float ox = inner.centerX() - (r.x() + r.width() / 2) * scale;
    const float oy = inner.centerY() - (r.y() + r.height() / 2) * scale;
    const SkRect dst = SkRect::MakeXYWH(ox, oy, s.width() * scale, s.height() * scale);
    canvas->save();
    canvas->clipRect(cell);
    anim->seekFrameTime(t * anim->duration());
    anim->render(canvas, &dst);
    canvas->restore();
}

} // namespace

int main(int argc, char **argv)
{
    if (argc < 3)
        usage();
    const char *in = argv[1];
    const char *out = argv[2];
    int size = 512, sheet = 0;
    double t = 0.5;
    float pad = 0.06f;
    bool strict = false;
    std::string bg = "1c1c22";
    SkRect region = SkRect::MakeEmpty();
    for (int i = 3; i < argc; ++i) {
        const std::string a = argv[i];
        auto next = [&]() -> const char * { if (++i >= argc) usage(); return argv[i]; };
        if (a == "--size") size = std::atoi(next());
        else if (a == "--t") t = std::atof(next());
        else if (a == "--sheet") sheet = std::atoi(next());
        else if (a == "--bg") bg = next();
        else if (a == "--pad") pad = float(std::atof(next()));
        else if (a == "--strict") strict = true;
        else if (a == "--region") {
            float x, y, w, h;
            if (std::sscanf(next(), "%f,%f,%f,%f", &x, &y, &w, &h) != 4)
                usage();
            region = SkRect::MakeXYWH(x, y, w, h);
        }
        else usage();
    }

    sk_sp<SkData> data = SkData::MakeFromFileName(in);
    if (!data) {
        std::fprintf(stderr, "cannot read %s\n", in);
        return 1;
    }
    auto logger = sk_make_sp<Logger>();
    skottie::Animation::Builder builder(skottie::Animation::Builder::kPreferEmbeddedFonts);
    builder.setLogger(logger);
    sk_sp<skottie::Animation> anim = builder.make(static_cast<const char *>(data->data()), data->size());
    if (!anim) {
        std::fprintf(stderr, "error: Skottie could not parse %s\n", in);
        return 1;
    }

    std::printf("size %gx%g  fps %g  duration %.2fs  frames %g..%g\n", anim->size().width(),
                anim->size().height(), anim->fps(), anim->duration(), anim->inPoint(), anim->outPoint());
    if (const sk_sp<skottie::SlotManager> &slots = builder.getSlotManager()) {
        const auto info = slots->getSlotInfo();
        std::printf("slots:");
        for (const SkString &id : info.fColorSlotIDs) std::printf(" %s(color)", id.c_str());
        for (const SkString &id : info.fScalarSlotIDs) std::printf(" %s(scalar)", id.c_str());
        for (const SkString &id : info.fVec2SlotIDs) std::printf(" %s(vec2)", id.c_str());
        for (const SkString &id : info.fTextSlotIDs) std::printf(" %s(text)", id.c_str());
        for (const SkString &id : info.fImageSlotIDs) std::printf(" %s(image)", id.c_str());
        std::printf("\n");
    }

    sk_sp<SkSurface> surface = SkSurfaces::Raster(SkImageInfo::MakeN32Premul(size, size));
    SkCanvas *canvas = surface->getCanvas();
    canvas->clear(SK_ColorTRANSPARENT);
    if (sheet > 0) {
        const float cell = float(size) / sheet;
        for (int i = 0; i < sheet * sheet; ++i) {
            const double ft = double(i) / (sheet * sheet - 1) * 0.999;
            drawFrame(canvas, anim.get(), ft,
                      SkRect::MakeXYWH((i % sheet) * cell, (i / sheet) * cell, cell, cell).makeInset(1, 1),
                      pad, bg, region);
        }
    } else {
        drawFrame(canvas, anim.get(), t, SkRect::MakeWH(size, size), pad, bg, region);
    }

    if (!writePng(out, surface->makeImageSnapshot().get())) {
        std::fprintf(stderr, "cannot write %s\n", out);
        return 1;
    }
    return strict && logger->warnings ? 2 : 0;
}
