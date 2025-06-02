## 🧭 User-Desktop App – Functional Guideline (Tailored Version)

---

### 🔹 **1. Owner Management (Dashboard Item #1)**

#### ✅ Features:

- List all owners (`Owners` table)
- Add New Owner: Opens a **modal form**:

  - `Ownercode` (auto-generated)
  - `Ownername`
  - `Ownerphone`
  - `Note`

- Edit/Delete owner (optional if not linked to properties)

#### 🔄 Behavior:

- Called from dashboard or **inline from property form** if no owner found.

---

### 🔹 **2. Property Management (Dashboard Item #2)**

#### ✅ Add New Property:

##### Form Fields:

- `realstatecode`: Auto-generated → `Companyco + Random(4)`
- `Property Type`: Dropdown from `Maincode` where `recty = 03`
- `Build Type`: Dropdown from `Maincode` where `recty = 04`
- `Unit of Measure`: Auto-select from `Maincode` (`recty = 05`)
- `Yearmake`: Date input (Year only)
- `Area`, `Facade`, `Depth`: Decimal
- `Bedrooms`, `Bathrooms`: Integer
- `Is Corner`: Yes/No
- `Offer Type`: Dropdown (`Maincode`, `recty = 06`)
- `Province` & `Region`: From `Maincode`
- `Address`, `Descriptions`: Text
- `Photo Upload`: 5–10 files (saved to `realstatephotos`)
- `Owner`: Select from `Owners` table

  - If not found → click “Add Owner” → open modal

##### On Save:

- Insert into `Realstatspecification`
- Insert photos into `realstatephotos`

---

### 🟦 **3. Update Property GUI (Dashboard Item #3)**

#### ✅ Workflow:

1. User sees list of all properties (summary list with basic info)
2. Search by:

   - `realstatecode`
   - Owner name
   - Region
   - Property type, etc.

#### 📋 On Result:

- Click property row → open action dropdown:

  - **Edit**:

    - Opens form (same as Add Property) pre-filled with data.
    - On save: update `Realstatspecification` and related photo/owner links.

  - **Delete**:

    - Confirm delete (with cascade for photos).
    - Remove from `Realstatspecification` and `realstatephotos`.

---

### 📊 **4. Search & Report (Dashboard Item #4)**

#### ✅ Features:

- Full property list with filters:

  - By type, year, region, corner, size, etc.

- View property details (read-only)
- Export to PDF/Excel for:

  - Filtered list
  - Single property full report

- Optionally include photos in report

#### 🧩 Technologies:

- Filtering logic from `Realstatspecification` joins with `Maincode`, `Owners`
- Use SQLite queries with LIKE, BETWEEN, etc.

---

### ⚙️ **5. Settings (Dashboard Item #5)**

#### Suggested Options:

- Set local company code (`Companyco`)
- Default photo save path
- Auto-backup/export directory
- Theme/UI preferences

---

### 🕓 **6. Recent Activity (Dashboard Item #6)**

#### Functionality:

- View last actions (insert, update, delete)
- Show:

  - Timestamp
  - Action type
  - Property code
  - Performed by (optional)

- Can be stored in a local log file or activity DB table.

---

## 💾 Database Usage Overview

| Table                   | Used In                                               |
| ----------------------- | ----------------------------------------------------- |
| `Realstatspecification` | Add, Update, Search, Reports                          |
| `Owners`                | Owner Management, Add/Edit Property                   |
| `realstatephotos`       | Photo uploads                                         |
| `Maincode`              | Dropdowns & lookups (type, units, offer, build, etc.) |

---
