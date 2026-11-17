import Foundation
import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let outdir = a[2]; let scale = CGFloat(Double(a[3])!)
for s in a[4...] {
  let parts = s.split(separator:"-").map{Int($0)!}
  let lo = parts[0], hi = parts.count>1 ? parts[1] : parts[0]
  for n in lo...hi {
    guard let pg = doc.page(at:n-1) else {continue}
    let r = pg.bounds(for:.mediaBox)
    let w = Int(r.width*scale), h = Int(r.height*scale)
    let img = NSImage(size: NSSize(width:w,height:h))
    img.lockFocus()
    NSColor.white.set(); NSRect(x:0,y:0,width:w,height:h).fill()
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.scaleBy(x:scale,y:scale)
    pg.draw(with:.mediaBox, to:ctx)
    img.unlockFocus()
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    try! rep.representation(using:.png, properties:[:])!.write(to: URL(fileURLWithPath:"\(outdir)/p\(n).png"))
  }
}
