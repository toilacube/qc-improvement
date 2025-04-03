# Basic UI Style Guide Rules (Inferred from Lotte Mart Product Page)

This document outlines common UI styling rules based on the visual analysis of the Lotte Mart product page. These serve as a baseline for maintaining visual consistency.

## 1. Color Palette

*   **Primary Action Color (`Brand Red`):** Used for key actions like "Add to Cart", "Accept Cookies", highlighting important navigation ("Danh Mục"), selected states (image thumbnail border), and badges ("MỚI"). (Approximate Hex: `#E52E37` - based on visual guess, needs confirmation).
*   **Primary Text Color:** Black or a very dark grey (e.g., `#212529`) used for body text, product titles, prices, labels.
*   **Secondary Text Color/Icon Color:** Medium-dark grey (e.g., `#6c757d`) used for secondary information, default icons (search, user, cart, share, wishlist), inactive navigation text.
*   **Background Color (Main):** White (`#FFFFFF`).
*   **Background Color (Subtle/Sections):** Very light grey (e.g., `#F8F9FA`) potentially used for the header background, quantity selector buttons, secondary action buttons (wishlist).
*   **Background Color (Footer/Banner):** Dark grey/near-black (e.g., `#343a40`) for contrasting banners like the cookie notice.
*   **Text Color on Primary Background:** White (`#FFFFFF`) used on red buttons/backgrounds.
*   **Text Color on Dark Background:** White (`#FFFFFF`) used on the cookie banner.
*   **Border Color:** Light grey (e.g., `#CED4DA` or slightly lighter) used for input fields, inactive thumbnails, potentially dividing lines.

## 2. Typography

*   **Font Family:** A clean, readable sans-serif font appears to be used throughout (e.g., Roboto, Lato, Open Sans - specific font needs confirmation).
*   **Product Title (Heading 1 Equivalent):**
    *   Font Size: Large (e.g., 24px - 28px).
    *   Font Weight: Bold.
    *   Color: Primary Text Color.
*   **Price:**
    *   Font Size: Large (similar or slightly larger than Product Title, e.g., 26px - 30px).
    *   Font Weight: Bold.
    *   Color: Primary Text Color.
*   **Section Headings ("Mô tả ngắn", "Số lượng", "Sản phẩm gợi ý"):**
    *   Font Size: Medium-Large (e.g., 18px - 20px).
    *   Font Weight: Bold.
    *   Color: Primary Text Color.
*   **Body Text / Descriptions:**
    *   Font Size: Standard (e.g., 14px - 16px).
    *   Font Weight: Regular.
    *   Color: Primary Text Color.
    *   Line Height: Adequate for readability (e.g., 1.5).
*   **Button Text:**
    *   Font Size: Standard (e.g., 14px - 16px).
    *   Font Weight: Medium or Bold.
    *   Color: White (on Primary Red), Primary Text Color (on light backgrounds - less common).
*   **Link Text:**
    *   Font Size: Standard (same as body text).
    *   Font Weight: Regular.
    *   Color: Primary Text Color (or a dedicated Link Color, often blue, but appears black/dark grey here).
    *   Decoration: None by default; likely underlines on hover (needs confirmation). The "Xem thêm" link follows this pattern.
*   **Input Field Text:**
    *   Font Size: Standard.
    *   Font Weight: Regular.
    *   Color: Primary Text Color.
*   **Navigation Text:**
    *   Font Size: Standard.
    *   Font Weight: Medium or Regular.
    *   Color: White (on Red background), Secondary Text Color (default state).

## 3. Buttons

*   **Primary Action Button ("Thêm vào giỏ hàng", "Đã hiểu"):**
    *   Background: `Brand Red`.
    *   Text Color: White.
    *   Padding: Generous horizontal and vertical padding.
    *   Border: None.
    *   Border Radius: Slightly rounded corners (e.g., 4px - 6px).
    *   Font Weight: Medium or Bold.
*   **Secondary/Icon Buttons (Wishlist, Compare, Quantity +/-):**
    *   Background: Very Light Grey.
    *   Icon/Text Color: Secondary Text Color (Dark Grey).
    *   Padding: Balanced padding around icon/text.
    *   Border: Thin, Light Grey border or none (relying on background contrast).
    *   Border Radius: Slightly rounded corners (similar to primary) or potentially square (for +/-).

## 4. Links

*   **Standard Links:** Blend with body text color (Primary Text Color). Underline likely appears on hover.
*   **Navigation Links:** Follow specific navigation styling (see Header/Nav Bar rules).

## 5. Forms & Inputs

*   **Text Input (Search, Quantity):**
    *   Background: White or Very Light Grey (Search).
    *   Text Color: Primary Text Color.
    *   Border: Thin, Light Grey border.
    *   Border Radius: Slightly rounded corners.
    *   Padding: Adequate internal padding.
    *   Placeholder Text Color: Secondary Text Color (Medium-dark grey).

## 6. Layout & Spacing

*   **Consistency:** Maintain consistent spacing (margins/padding) between elements and sections.
*   **Whitespace:** Utilize ample whitespace to avoid clutter and improve readability.
*   **Alignment:** Elements within sections should be consistently aligned (e.g., left-aligned text, centered elements where appropriate).
*   **Responsiveness:** (Assumption) The layout should adapt gracefully to different screen sizes, although specific rules require testing/design specs.

**Note:** These rules are inferred from a single static image. Interactive states (hover, focus, active, disabled), specific pixel values, font names, and exact color codes would need to be confirmed from design specifications or browser inspection tools.