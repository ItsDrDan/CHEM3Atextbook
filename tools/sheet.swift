import Foundation
import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let outdir = a[2]; let lo = Int(a[3])!, hi = Int(a[4])!
let cols = 6, rows = 5, tw = 260, th = 336
var start = lo
while start <= hi {
  let W = cols*tw, H = rows*(th+18)
  let img = NSImage(size: NSSize(width:W,height:H))
  img.lockFocus()
  NSColor(white:0.75,alpha:1).set(); NSRect(x:0,y:0,width:W,height:H).fill()
  for i in 0..<(cols*rows) {
    let n = start+i; if n>hi {break}
    guard let pg = doc.page(at:n-1) else {continue}
    let c = i%cols, r = i/cols
    let x = CGFloat(c*tw), y = CGFloat(H-(r+1)*(th+18))
    let rect = pg.bounds(for:.mediaBox)
    let s = min(CGFloat(tw-6)/rect.width, CGFloat(th-6)/rect.height)
    NSColor.white.set(); NSRect(x:x+3,y:y+3,width:rect.width*s,height:rect.height*s).fill()
    let ctx = NSGraphicsContext.current!.cgContext
    ctx.saveGState(); ctx.translateBy(x:x+3,y:y+3); ctx.scaleBy(x:s,y:s); pg.draw(with:.mediaBox,to:ctx); ctx.restoreGState()
    ("p\(n)" as NSString).draw(at: NSPoint(x:x+6,y:y+CGFloat(th)), withAttributes:[.font:NSFont.boldSystemFont(ofSize:14),.foregroundColor:NSColor.red])
  }
  img.unlockFocus()
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
  try! rep.representation(using:.jpeg, properties:[.compressionFactor:0.6])!.write(to: URL(fileURLWithPath:"\(outdir)/sheet_\(start).jpg"))
  start += cols*rows
}
