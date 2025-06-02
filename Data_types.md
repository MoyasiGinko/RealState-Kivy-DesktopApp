---

### **1. `Maincode` – General Coding Table**

| Field Name    | Data Type | Length | Description              | Sample Value          |
| ------------- | --------- | ------ | ------------------------ | --------------------- |
| `Recty`       | CHAR      | 2      | Record type code         | `01`, `02`, `03`, ... |
| `Code`        | CHAR      | 16     | Full classification code | `01001xxxxxxxxxxxxx`  |
| `Name`        | VARCHAR   | 50     | Name                     | `Iraq`, `Baghdad`     |
| `Description` | TEXT      | -      | Notes and description    | `Country Code`        |

📌 *Indexing should be applied on (`Recty`, `Code`) pair for fast lookups.*

---

### **2. `Companyinfo` – Company Information Table**

| Field Name             | Data Type | Length | Description                    | Sample Value       |
| ---------------------- | --------- | ------ | ------------------------------ | ------------------ |
| `Companyco`            | CHAR      | 4      | Unique company code (A###)     | `E901`             |
| `Companyna`            | VARCHAR   | 30     | Company name                   | `Best Real Estate` |
| `Cityco`               | CHAR      | 5      | City code                      | `02001`            |
| `Caddress`             | VARCHAR   | 50     | Address                        | `123 King St.`     |
| `Cophoneno`            | CHAR      | 11     | Phone number                   | `07901234567`      |
| `Username`             | CHAR      | 12     | Username                       | `adminuser`        |
| `Password`             | CHAR      | 8      | Password                       | `pass1234`         |
| `SubscriptionTCode`    | CHAR      | 1      | Type of subscription           | `1`, `2`           |
| `Lastpayment`          | DATE      | -      | Date of last payment           | `2025-05-15`       |
| `Subscriptionduration` | CHAR      | 1      | Subscription duration (months) | `3`                |
| `Registrationdate`     | DATE      | -      | Registration date              | `2025-04-01`       |
| `Descriptions`         | TEXT      | -      | Additional notes               | `Trial account`    |

📌 _Business rules around subscription, expiration, and transitions from trial to active are enforced here._

---

### **3. `Realstatspecification` – Property Specification Table**

| Field Name         | Data Type  | Length | Description                     | Sample Value       |
| ------------------ | ---------- | ------ | ------------------------------- | ------------------ |
| `Companyco`        | CHAR       | 4      | Company code                    | `E901`             |
| `realstatecode`    | CHAR       | 8      | Auto-generated property code    | `E901A7F2`         |
| `Rstatetcode`      | CHAR       | 1      | Real estate type                | `1`, `2`, `3`      |
| `Yearmake`         | DATE(YEAR) | -      | Year built                      | `2010`             |
| `Buildtcode`       | CHAR       | 1      | Building type                   | `1`, `2`, `3`      |
| `Property-area`    | DOUBLE     | (5,2)  | Area in square meters           | `145.75`           |
| `Unitm-code`       | CHAR       | 1      | Unit of measurement code        | `1`, `2`           |
| `Property-facade`  | DOUBLE     | (3,2)  | Facade length                   | `12.50`            |
| `Property-depth`   | DOUBLE     | (3,2)  | Depth of property               | `30.75`            |
| `N-of-bedrooms`    | INT        | 2      | Number of bedrooms              | `3`                |
| `N-of-bathrooms`   | INT        | 2      | Number of bathrooms             | `2`                |
| `Property-corner`  | BOOLEAN    | -      | Is it a corner property?        | `true`             |
| `Offer-Type-Code`  | CHAR       | 1      | Type of offer                   | `1` (rent/sale)    |
| `Province-code`    | CHAR       | 2      | Province code                   | `01`               |
| `Region-code`      | CHAR       | 9      | Region code                     | `0200101xx`        |
| `Property-address` | TEXT       | 250    | Full address                    | `Area X, Street Y` |
| `Photosituation`   | BOOLEAN    | -      | Are photos available?           | `true`             |
| `Ownercode`        | CHAR       | 4      | Owner code (linked to `Owners`) | `A123`             |
| `Descriptions`     | TEXT       | -      | Notes and description           | `Well maintained.` |

📌 _Ensure foreign key constraints to `Owners.Ownercode` and `Maincode.Code` where applicable._

---

### **4. `realstatephotos` – Property Photos Table**

| Field Name       | Data Type | Length | Description                | Sample Value     |
| ---------------- | --------- | ------ | -------------------------- | ---------------- |
| `realstatecode`  | CHAR      | 8      | Property code              | `E901A7F2`       |
| `Storagepath`    | VARCHAR   | 50     | Path where image is stored | `/photos/E901/`  |
| `photofilename`  | VARCHAR   | 30     | Image file name            | `front_view.jpg` |
| `Photoextension` | CHAR      | 4      | File extension             | `.jpg`, `.png`   |

📌 _This table is stored on a cheaper cloud service, separate from VPS._

---

### **5. `Owners` – Property Owners Table**

| Field Name   | Data Type | Length | Description           | Sample Value      |
| ------------ | --------- | ------ | --------------------- | ----------------- |
| `Ownercode`  | CHAR      | 4      | Owner code            | `A123`            |
| `ownername`  | VARCHAR   | 30     | Owner name            | `Mohammed Khaled` |
| `ownerphone` | CHAR      | 11     | Phone number          | `07812345678`     |
| `Note`       | TEXT      | -      | Notes about the owner | `Prefers email`   |

📌 _This table is editable only if owner isn't linked to property._

---

### **📦 Table Distribution**

| Platform          | Tables Included                                     |
| ----------------- | --------------------------------------------------- |
| **User Desktop**  | `Realstatspecification`, `realstatephotos`          |
| **Web VPS**       | `Maincode`, `Companyinfo`, `Owners`                 |
| **Shared (Sync)** | `Realstatspecification` (daily sync: desktop → VPS) |

---
