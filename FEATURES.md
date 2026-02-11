## FabriCost – Main Features

- **Dual calculators**
  - 3D printing price calculator (filament + time)
  - Laser cutting price calculator (time only)

- **Piece management**
  - Add pieces with grams (3D), hours and minutes
  - Edit and delete pieces from a scrollable list
  - Empty hours or minutes are treated as 0 (only both empty is invalid)

- **Flexible pricing rules**
  - 3D: gram price, normal hour price, exceed-hour price, threshold, markup %
  - Laser: single hour price and markup %
  - All rules are editable and can be reset to factory defaults

- **Results and exports**
  - Per-piece cards with full price breakdown and final price
  - Global summary (total price + total printing/cutting time)
  - Detailed PDF quote (3D or Laser wording and layout)
  - Simple PDF (one line per piece with final price)

- **Receipts and clipboard**
  - Generate a styled receipt image for each piece
  - Image is copied directly to the Windows clipboard for pasting into chats
  - Text summary for a piece can also be copied to the clipboard

- **Language & settings persistence**
  - French and English UI with instant switching
  - All settings (language + pricing rules) saved in a local SQLite database and restored on next launch

- **Branding & UX**
  - FabriCost splash screen with logo and tagline
  - Mode selection menu (3D vs Laser) and About dialog (author: Mahou)
  - Modern, responsive Tkinter UI with separate input and results dashboards


