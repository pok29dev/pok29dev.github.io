# Pok's Workspace

พื้นที่เก็บผลงานของ **Pok Kusuwan** — Developer, Entrepreneur และ AI-Agent Developer

---

## 📚 หนังสือ / คอร์ส

### เรียนลัด thClaws ฉบับอ่านเอง (Self-Study Book)

หนังสือสำหรับเปลี่ยนจาก "เคยใช้ Chat AI ถาม-ตอบ" ไปสู่ "ใช้ AI Agent ลงมือทำงานจริงบนเครื่องตัวเอง" — อ่านและทำตามเองได้ ไม่ต้องมีผู้สอน

> **แนวคิดหลัก:** *"Chat AI ตอบคำถาม / thClaws ทำงานให้"*

- **เหมาะสำหรับ:** พนักงานออฟฟิศ / ผู้ใช้ทั่วไป ที่เคยใช้ ChatGPT, Copilot, Gemini แต่อยากก้าวไปใช้ AI Agent
- **ระยะเวลา:** ~2 ชั่วโมง (บทนำ 10 นาที + บท 1–6)
- **เปิดอ่าน:** [หน้าหลักของหนังสือ](thclaws-2hr-course/README.md)

| บท | เนื้อหา | เวลาประมาณ |
|----|---------|-------------|
| [บทนำ — เริ่มต้น วิธีอ่าน](thclaws-2hr-course/chapter-00-เริ่มต้น-วิธีอ่าน.md) | วิธีใช้หนังสือ, สิ่งที่ต้องมีก่อนเริ่ม, ภาพรวมเส้นทาง | 10 นาที |
| [บท 1 — รู้จัก thClaws](thclaws-2hr-course/chapter-01-รู้จัก-thclaws.md) | thClaws คืออะไร, ต่างจาก Chat AI อย่างไร | 15 นาที |
| [บท 2 — ติดตั้งและตั้งค่า](thclaws-2hr-course/chapter-02-ติดตั้ง-และ-ตั้งค่า.md) | ติดตั้ง, ใส่ API Key, ตั้ง instruction | 30 นาที |
| [บท 3 — เริ่มใช้งานจริง](thclaws-2hr-course/chapter-03-เริ่มใช้งาน-จริง.md) | 3 โหมด, working directory, GUI, session, คำสั่งแรก | 30 นาที |
| [บท 4 — Tools, Skills, MCP](thclaws-2hr-course/chapter-04-tools-skills-mcp.md) | Built-in tools, Skills, MCP | 35 นาที |
| [บท 5 — thClaws Cloud](thclaws-2hr-course/chapter-05-thclaws-cloud.md) | thClaws.cloud คืออะไร, 3 องค์ประกอบ, Access Key, Hosted Workspace | 20 นาที |
| [บท 6 — ทบทวนและก้าวต่อไป](thclaws-2hr-course/chapter-06-ทบทวน-และ-ก้าวต่อไป.md) | เช็กลิสต์คำสั่ง, งานปฏิบัติรวม, แบบตรวจความเข้าใจ, เส้นทางไปต่อ | 40 นาที |

> 💡 แนะนำให้อ่านตามลำดับ บทนำ → บท 6 เพราะแต่ละบทต่อยอดจากบทก่อนหน้า แต่ละบทจบด้วย "ลงมือทำเอง" และ "ตรวจความเข้าใจ" ที่ทำได้คนเดียว

---

## 📁 ไฟล์ตัวอย่าง / Demo Data

ชุดข้อมูลสมมติ (fictional) สำหรับฝึกอบรมและลองทำ Hands-on กับ AI Agent — แบ่งเป็น 2 กลุ่ม

### 1. ไฟล์ตัวอย่างสำหรับหนังสือ (Self-Study)

ไฟล์ใน [`thclaws-2hr-course/samples/`](thclaws-2hr-course/samples/README.md) ใช้กับกิจกรรมลงมือทำของบท 3–5 — คัดลอกไปวางใน working directory (`~/thclaws-2hr`) ก่อนเริ่ม

**⬇️ ดาวน์โหลด:** [รวมทุกไฟล์ `samples.zip`](thclaws-2hr-course/samples/samples.zip)

| ไฟล์ | ชนิด | ใช้ในบท | เนื้อหา |
|------|------|---------|---------|
| [⬇️ `meeting_notes.txt`](thclaws-2hr-course/samples/meeting_notes.txt) | ข้อความ | 3, 4 | บันทึกประชุมวางแผนเปิดตัวสินค้า — สรุป/แยก action items |
| [⬇️ `notes.txt`](thclaws-2hr-course/samples/notes.txt) | ข้อความ | 3 | บันทึกงานประจำวัน — สรุปงาน/เตือนงานค้าง |
| [⬇️ `monthly-sales.csv`](thclaws-2hr-course/samples/monthly-sales.csv) | CSV | 4 | ยอดขาย 6 เดือน 3 สินค้า — สร้าง Excel/วิเคราะห์ |
| [⬇️ `customer-contacts.csv`](thclaws-2hr-course/samples/customer-contacts.csv) | CSV | 4 | รายชื่อลูกค้า — สร้างสเปรดชีต/จัดประเภท |
| [⬇️ `meeting-transcript.docx`](thclaws-2hr-course/samples/meeting-transcript.docx) | Word | 4 | บันทึกประชุมทีมขาย — ทดสอบอ่าน/สรุปเอกสาร Word |
| [⬇️ `company-policy.pdf`](thclaws-2hr-course/samples/company-policy.pdf) | PDF | 4 | นโยบายบริษัท — ทดสอบอ่าน/สรุป PDF |

> ดูวิธีใช้ต่อบทได้ใน [`samples/README.md`](thclaws-2hr-course/samples/README.md)

### 2. ชุดข้อมูลอบรม (Workshop)

ข้อมูลใน [`demo-files/`](demo-files/README.md) สำหรับอบรม **AI Agent & Work Automation Prompting** — ประกอบด้วยใบงาน PDF + ไฟล์ข้อมูลที่ใช้ทดสอบ (workshop + cafe) ดูรายละเอียดได้ที่ [`demo-files/README.md`](demo-files/README.md)
