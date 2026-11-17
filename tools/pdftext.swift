import Foundation
import PDFKit
let args = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: args[1]))!
let out = args[2]
var s = "PAGECOUNT \(doc.pageCount)\n"
if let attrs = doc.documentAttributes { for (k,v) in attrs { s += "META \(k): \(v)\n" } }
func walk(_ o: PDFOutline?, _ d: Int) { guard let o = o else {return}; for i in 0..<o.numberOfChildren { let c = o.child(at:i)!; let p = c.destination?.page.flatMap{doc.index(for:$0)} ?? -1; s += "OUTLINE \(String(repeating:"  ",count:d))\(c.label ?? "") @\(p+1)\n"; walk(c, d+1) } }
walk(doc.outlineRoot, 0)
for i in 0..<doc.pageCount { s += "\n=====PAGE \(i+1)=====\n" + (doc.page(at:i)?.string ?? "") }
try! s.write(toFile: out, atomically: true, encoding: .utf8)
