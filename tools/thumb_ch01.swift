// Chapter 1 table-of-contents thumbnail (400x400 PNG), matching the other chapters' style:
// dark background picture + big white condensed capitals. Original line art of measuring tools (no photo).
// Run: swift tools/thumb_ch01.swift figures/ch01/thumb_ch01.png
import AppKit

let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "thumb_ch01.png"
let S: CGFloat = 400
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(S), pixelsHigh: Int(S), bitsPerSample: 8,
                           samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB,
                           bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
let ctx = NSGraphicsContext.current!.cgContext

// Background: deep navy to teal
let grad = NSGradient(colors: [NSColor(calibratedRed: 0.05, green: 0.10, blue: 0.22, alpha: 1),
                               NSColor(calibratedRed: 0.04, green: 0.30, blue: 0.36, alpha: 1)])!
grad.draw(in: NSRect(x: 0, y: 0, width: S, height: S), angle: 60)

func stroke(_ p: NSBezierPath, _ a: CGFloat, _ w: CGFloat) {
    NSColor(calibratedRed: 0.75, green: 0.93, blue: 1.0, alpha: a).setStroke(); p.lineWidth = w; p.stroke()
}
// Graduated cylinder (left)
let cyl = NSBezierPath(roundedRect: NSRect(x: 34, y: 40, width: 62, height: 300), xRadius: 8, yRadius: 8)
stroke(cyl, 0.55, 3)
let base = NSBezierPath(); base.move(to: NSPoint(x: 18, y: 40)); base.line(to: NSPoint(x: 112, y: 40)); stroke(base, 0.55, 4)
let liquid = NSBezierPath(rect: NSRect(x: 37, y: 43, width: 56, height: 170))
NSColor(calibratedRed: 0.35, green: 0.80, blue: 0.95, alpha: 0.22).setFill(); liquid.fill()
let meniscus = NSBezierPath(); meniscus.move(to: NSPoint(x: 37, y: 218))
meniscus.curve(to: NSPoint(x: 93, y: 218), controlPoint1: NSPoint(x: 52, y: 204), controlPoint2: NSPoint(x: 78, y: 204))
stroke(meniscus, 0.7, 2.5)
for i in 0..<28 {
    let y = CGFloat(60 + i * 10); let long = i % 5 == 0
    let t = NSBezierPath(); t.move(to: NSPoint(x: 37, y: y)); t.line(to: NSPoint(x: long ? 62 : 50, y: y)); stroke(t, 0.45, 1.5)
}
// Beaker (right)
let bk = NSBezierPath()
bk.move(to: NSPoint(x: 280, y: 250)); bk.line(to: NSPoint(x: 288, y: 60))
bk.curve(to: NSPoint(x: 300, y: 48), controlPoint1: NSPoint(x: 288, y: 52), controlPoint2: NSPoint(x: 292, y: 48))
bk.line(to: NSPoint(x: 362, y: 48))
bk.curve(to: NSPoint(x: 374, y: 60), controlPoint1: NSPoint(x: 370, y: 48), controlPoint2: NSPoint(x: 374, y: 52))
bk.line(to: NSPoint(x: 382, y: 250)); stroke(bk, 0.5, 3)
for i in 0..<5 { let y = CGFloat(90 + i * 32); let t = NSBezierPath(); t.move(to: NSPoint(x: 292, y: y)); t.line(to: NSPoint(x: 318, y: y)); stroke(t, 0.4, 1.5) }
// Ruler (top, tilted)
ctx.saveGState(); ctx.translateBy(x: 120, y: 330); ctx.rotate(by: -0.12)
let ruler = NSBezierPath(rect: NSRect(x: 0, y: 0, width: 300, height: 34)); stroke(ruler, 0.45, 2.5)
for i in 0..<30 { let x = CGFloat(8 + i * 10); let h: CGFloat = i % 10 == 0 ? 18 : (i % 5 == 0 ? 13 : 8)
    let t = NSBezierPath(); t.move(to: NSPoint(x: x, y: 0)); t.line(to: NSPoint(x: x, y: h)); stroke(t, 0.45, 1.5) }
ctx.restoreGState()
// Darken for text contrast, like the photo thumbnails
NSColor(calibratedWhite: 0, alpha: 0.38).setFill(); NSRect(x: 0, y: 0, width: S, height: S).fill()

// Title in white condensed capitals, each line fitted to the width
let lines = ["MEASUREMENT,", "MATTER, AND", "THE SCIENTIFIC", "METHOD"]
let fontName = "DINCondensed-Bold"
let maxW: CGFloat = S - 44
let shadow = NSShadow(); shadow.shadowColor = NSColor(calibratedWhite: 0, alpha: 0.7); shadow.shadowBlurRadius = 6
shadow.shadowOffset = NSSize(width: 0, height: -2)
var sizes: [CGFloat] = []
for l in lines {
    var fs: CGFloat = 92
    while fs > 20 {
        let w = (l as NSString).size(withAttributes: [.font: NSFont(name: fontName, size: fs)!]).width
        if w <= maxW { break }; fs -= 1
    }
    sizes.append(fs)
}
let fs = min(sizes.min()!, 78)   // one size for all lines, like the other thumbnails
let font = NSFont(name: fontName, size: fs)!
let lineH = fs * 0.98
let total = lineH * CGFloat(lines.count)
var y = (S + total) / 2 - lineH * 0.82
for l in lines {
    let attrs: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: NSColor.white, .shadow: shadow]
    let w = (l as NSString).size(withAttributes: attrs).width
    (l as NSString).draw(at: NSPoint(x: (S - w) / 2, y: y - fs * 0.18), withAttributes: attrs)
    y -= lineH
}
NSGraphicsContext.restoreGraphicsState()
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: out))
print("wrote \(out)")
