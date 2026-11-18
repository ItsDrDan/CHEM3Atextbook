# Request to LibreTexts support: cover author for the CHEM 3A Revision Draft

**Book:** Introductory Chemistry Atoms First for FCC - Revision Draft (Workbench, Conductor project DTvJm7TcCY, root page 597470 on chem.libretexts.org)

**Problem:** the compiled PDF cover prints the author as "Unknown".

**What we found (2026-11-17):** the cover author is looked up from author records in `Template:Custom/Data/Authors` (page 567488, the `authors_X.json` attachments). That page is read-only for faculty accounts, and it has no record for Daniel Kwasniewski or Seth Yates. The book's root page also carries no `authorname:` tag. The live FCC book (page 408941) has the same setup.

**Requested credit line:** Daniel Kwasniewski, Fresno City College. Adapted from *Introductory Chemistry, Atoms First for FCC*, compiled by Seth Yates.

**Please:**
1. Create author records `dkwasniewski` (Daniel Kwasniewski, Fresno City College) and, if you credit compilers on covers, one for Seth Yates.
2. Tell us which `authorname:` tag(s) to put on root page 597470 (we can add the tag ourselves), or add it for us.

**Conductor:** project DTvJm7TcCY has no author fields (`libreCoverID` 597470; lead Daniel Kwasniewski), so we could not set the cover there.

**Already done on our side:** the title page (597474) shows the credit line, and every chapter page carries `author@Daniel Kwasniewski`.
