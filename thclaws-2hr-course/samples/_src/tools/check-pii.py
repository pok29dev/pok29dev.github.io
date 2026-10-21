#!/usr/bin/env python3
# ตรวจความถูกต้องของ output/thclaws-2hr-course-v2/samples/pii-demo.txt
# - checksum ของเลขบัตร 13 หลัก: "ถูกจับ" ต้องผ่าน / "checksum ไม่ผ่าน" ต้องไม่ผ่าน
# - เลขที่เว้นวรรคต้องมี 13 หลักจริง และต้องไม่อยู่ในรูปติดกัน
# - นับองค์ประกอบตามเกณฑ์ขั้นต่ำ
import re, sys, pathlib

P = pathlib.Path("output/thclaws-2hr-course-v2/samples/pii-demo.txt")
text = P.read_text(encoding="utf-8")


def checksum(s: str):
    """หลักตรวจสอบไทย: น้ำหนัก 13..2 กับ 12 หลักแรก, (11 - sum % 11) % 10"""
    if len(s) != 13 or not s.isdigit():
        return None
    total = sum(w * int(c) for w, c in zip(range(13, 1, -1), s[:12]))
    return (11 - (total % 11)) % 10


def ok(s: str) -> bool:
    c = checksum(s)
    return c is not None and int(s[-1]) == c


# ---- ชุดที่อ้างว่า "ถูกจับ" (ต้องผ่าน checksum) ----
VALID = ["3100600445635", "1103700212345", "1209800456780", "3901200789012",
         "5103701456780", "6201200788122", "1509901122337", "4102800912342"]

# ---- ชุดที่อ้างว่า "checksum ไม่ผ่าน" (ต้องไม่ผ่านจริง) ----
INVALID = ["1234567890124", "1103700212349", "3901200789018"]

# ---- เลขบัตรพิมพ์เว้นวรรค (13 หลัก แต่ต้องอยู่ในรูปมีช่องว่าง) ----
SPACED = ["3 1006 00445 63 5", "1 1037 00212 34 5", "5 1037 01456 78 0"]

# ---- เบอร์โทรที่นับเป็น "ถูกจับ" ----
PHONES = ["081-234-5678", "02-123-4567", "089-456-1234", "0623456789",
          "๐๘๖-๗๘๙-๐๑๒๓", "095-444-7788", "0876543210", "053-221-998",
          "091-778-9900", "02-641-8899", "076-221-334", "044-312-556"]

# ---- ชื่อที่มีคำนำหน้าทางการ (นับเป็น "ถูกจับ") ----
PREFIXED = ["นายสมชาย ใจดี", "นางสาวปรีดา ศรีสุข", "นายวรชัย บุญมี",
            "นางมาลี รักเรียน", "ด.ช.ธนกฤต พูลสุข", "นางสาวกนกวรรณ ทองคำ",
            "นายอนุชิต แก้วมณี", "นางสุนีย์ พงษ์ไพศาล", "น.ส.จิราพร เลิศวิทยา",
            "ด.ญ.ปุณิกา ชัยวัฒน์", "นายธีรภัทร สุขสมบูรณ์", "นางอรทัย ใจกล้า",
            "นายศักดิ์ชัย เรืองฤทธิ์", "นางสาวพิมพ์ชนก ดวงแก้ว"]

# ---- ทะเบียนรถ (มีคำว่า "ทะเบียน" นำหน้า) ----
PLATES = ["ทะเบียน 1กก 1234 กรุงเทพมหานคร", "ทะเบียน 2ขค 5678 กรุงเทพมหานคร",
          "ทะเบียน 3ฒฮ 9012 นนทบุรี"]

# ---- รายการที่อ้างว่า "ยังไม่ถูกจับ" ----
NEG = ["คุณสมชาย", "somchai.j@example.com", "99/1 ถนนสุขุมวิท",
       "123-4-56789-0", "INV-2026-0042"]

fails = []
print(f"ไฟล์: {P}  ({len(text)} ตัวอักษร)\n")

print("== 1) เลขบัตร 13 หลัก — ชุดที่อ้างว่า 'ถูกจับ' ต้องผ่าน checksum ==")
vpass = 0
for n in VALID:
    c, in_file = checksum(n), n in text
    good = ok(n) and in_file
    vpass += good
    print(f"  {n}  computed={c} last={n[-1]}  inFile={in_file}  -> {'PASS' if good else 'FAIL'}")
    if not good:
        fails.append(n)
print(f"  สรุป: ผ่านครบ {vpass}/{len(VALID)}")

print("\n== 2) 'checksum ไม่ผ่าน' ต้องไม่ผ่านจริง และต้องอยู่ในไฟล์ ==")
vbad = 0
for n in INVALID:
    c, in_file = checksum(n), n in text
    good = (not ok(n)) and in_file
    vbad += good
    print(f"  {n}  computed={c} last={n[-1]}  inFile={in_file}  -> {'PASS' if good else 'FAIL'}")
    if not good:
        fails.append(n)
print(f"  สรุป: ไม่ผ่านครบ {vbad}/{len(INVALID)}")

print("\n== 3) เลขบัตรที่เว้นวรรค: 13 หลักจริง + อยู่ในรูปมีช่องว่าง ==")
for s in SPACED:
    digits = re.sub(r"\D", "", s)
    concat = digits in text          # ถ้าติดกันในไฟล์ด้วย ถือว่าปกติ (ใช้เทียบคู่)
    good = len(digits) == 13 and (s in text)
    print(f"  '{s}'  digits={len(digits)}  inFileSpaced={s in text}  -> {'PASS' if good else 'FAIL'}")
    if not good:
        fails.append(s)
    _ = concat

print("\n== 4) สแกนหาเลข 13 หลักติดกันทั้งหมดในไฟล์ (ต้องเป็นชุดที่รู้จัก) ==")
found = sorted(set(re.findall(r"(?<![\d])(\d{13})(?![\d])", text)))
known = set(VALID) | set(INVALID)
for n in found:
    tag = "valid" if n in VALID else ("invalid" if n in INVALID else "ไม่รู้จัก")
    cs = "ผ่าน" if ok(n) else "ไม่ผ่าน"
    print(f"  {n}  checksum {cs}  [{tag}]")
    if tag == "ไม่รู้จัก":
        fails.append(n)
print(f"  พบ {len(found)} หมายเลข / รู้จักทั้งหมด: {'ใช่' if set(found) <= known else 'ไม่'}")

print("\n== 5) องค์ประกอบอื่น (ต้องปรากฏในไฟล์) ==")
for label, items, need in [("ชื่อมีคำนำหน้า", PREFIXED, 12), ("เบอร์โทร", PHONES, 10),
                           ("ทะเบียนรถ", PLATES, 3)]:
    miss = [i for i in items if i not in text]
    print(f"  {label}: {len(items)} รายการ (เกณฑ์ >= {need})  ขาด: {miss if miss else '-'}")
    if len(items) < need or miss:
        fails.append(label)
miss_neg = [i for i in NEG if i not in text]
print(f"  รายการ 'ยังไม่ถูกจับ': {len(NEG)} รายการ (เกณฑ์ >= 5)  ขาด: {miss_neg if miss_neg else '-'}")
if len(NEG) < 5 or miss_neg:
    fails.append("neg")
thai_digit_phone = [p for p in PHONES if any(ch in "๐๑๒๓๔๕๖๗๘๙" for ch in p)]
print(f"  เบอร์ที่เขียนด้วยเลขไทย: {len(thai_digit_phone)} รายการ -> {thai_digit_phone}")
if not thai_digit_phone:
    fails.append("thai-digits")
for s in ["ข้อมูลสมมติสำหรับฝึกอบรม", "sensitive", "🔓", "[NAME_", "[PHONE_", "[ID_", "[PLATE_"]:
    if s not in text:
        fails.append(f"missing:{s}")
        print(f"  !! ไม่พบข้อความที่ต้องมี: {s}")

print(f"\n== ความยาว ==\n  {len(text)} ตัวอักษร (เกณฑ์ >= 8500) -> {'PASS' if len(text) >= 8500 else 'FAIL'}")
if len(text) < 8500:
    fails.append("length")

print("\n===== สรุป =====")
if fails:
    print("FAIL:", fails)
    sys.exit(1)
print("ทุกข้อผ่าน ✔  (ถูกจับ/ผ่าน checksum %d · ไม่ผ่าน %d · เว้นวรรค %d)"
      % (len(VALID), len(INVALID), len(SPACED)))
