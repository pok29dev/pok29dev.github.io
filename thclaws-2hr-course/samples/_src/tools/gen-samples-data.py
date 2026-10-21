#!/usr/bin/env python3
"""Generate realistic Thai sample datasets for the thClaws 2-hr course.

Outputs (into output/thclaws-2hr-course-v2/samples/):
  - monthly-sales.csv       12 months x 18-20 SKU  (216 + 6 rows = 222)
  - daily-sales-2026.csv    365 days x 3 categories (1,095 rows)
  - customer-contacts.csv   1,000 customer master rows

Invariants enforced (asserted at the end of this script):
  * the original 18 rows of monthly-sales.csv survive byte-for-byte in value
  * daily-sales-2026.csv aggregates EXACTLY to monthly-sales.csv per (month, category)
"""
import csv
import random
from datetime import date, timedelta

OUT = "output/thclaws-2hr-course-v2/samples"  # รันจาก workspace root: python3 output/thclaws-2hr-course-v2/samples/_src/tools/gen-samples-data.py
rng = random.Random(20260930)

MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
          "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
MDAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
YEAR = 2026

CAT = {"แก้วเดี่ยว": "แก้วเดี่ยว", "เหยือกใหญ่": "เหยือกใหญ่", "จัดเลี้ยง": "ชุดจัดเลี้ยง"}

# ---------------------------------------------------------------- monthly data
# (หมวด, สินค้า, ราคาต่อหน่วย, {month_index: จำนวน})
ORIGINAL_18 = [  # month_idx, สินค้า, จำนวน, ราคา, ยอดขายรวม  -- must stay identical
    (0, "กาแฟดำ", 1200, 60, 72000), (0, "ชาเขียว", 800, 55, 44000), (0, "ลาเต้", 950, 75, 71250),
    (1, "กาแฟดำ", 1350, 60, 81000), (1, "ชาเขียว", 900, 55, 49500), (1, "ลาเต้", 1100, 75, 82500),
    (2, "กาแฟดำ", 1400, 65, 91000), (2, "ชาเขียว", 950, 55, 52250), (2, "ลาเต้", 1200, 75, 90000),
    (3, "กาแฟดำ", 1250, 65, 81250), (3, "ชาเขียว", 850, 55, 46750), (3, "ลาเต้", 1050, 75, 78750),
    (4, "กาแฟดำ", 1500, 65, 97500), (4, "ชาเขียว", 1000, 55, 55000), (4, "ลาเต้", 1300, 75, 97500),
    (5, "กาแฟดำ", 1600, 65, 104000), (5, "ชาเขียว", 1100, 55, 60500), (5, "ลาเต้", 1400, 75, 105000),
]

# สินค้าใหม่/ที่เหลือ: (หมวด, สินค้า, ราคา, จำนวนเดือน ม.ค., จำนวนเดือน ธ.ค., โมเดลการเติบโต)
NEW_SKUS = [
    # แก้วเดี่ยว
    ("แก้วเดี่ยว", "กาแฟดำ", 65, 1600, 2100, "lin"),
    ("แก้วเดี่ยว", "ชาเขียว", 55, 1100, 1450, "lin"),
    ("แก้วเดี่ยว", "ลาเต้", 75, 1400, 1850, "lin"),
    ("แก้วเดี่ยว", "อเมริกาโน่เย็น", 65, 720, 1280, "lin"),
    ("แก้วเดี่ยว", "กาแฟโบราณ", 50, 540, 980, "lin"),
    ("แก้วเดี่ยว", "มอคค่า", 80, 480, 860, "lin"),
    # เหยือกใหญ่ (ไลน์ใหม่ โตเร็ว)
    ("เหยือกใหญ่", "เหยือกกาแฟดำ", 450, 70, 380, "lin"),
    ("เหยือกใหญ่", "เหยือกชาเขียว", 420, 45, 300, "lin"),
    ("เหยือกใหญ่", "เหยือกลาเต้", 520, 60, 350, "lin"),
    ("เหยือกใหญ่", "เหยือกอเมริกาโน่", 480, 50, 320, "lin"),
    ("เหยือกใหญ่", "เหยือกกาแฟโบราณ", 400, 30, 220, "lin"),
    ("เหยือกใหญ่", "เหยือกมอคค่า", 560, 35, 240, "lin"),
    # ชุดจัดเลี้ยง (ตามฤดูกาล งานอีเวนต์/ประชุม)
    ("ชุดจัดเลี้ยง", "ชุดประชุม 10 ท่าน", 1200, 28, 62, "lin"),
    ("ชุดจัดเลี้ยง", "ชุดประชุม 20 ท่าน", 2300, 16, 38, "lin"),
    ("ชุดจัดเลี้ยง", "ชุดเบรกเช้า 15 ท่าน", 1600, 22, 45, "lin"),
    ("ชุดจัดเลี้ยง", "ชุดงานอีเวนต์ 30 ท่าน", 3400, 8, 26, "lin"),
    ("ชุดจัดเลี้ยง", "ชุดสัมมนา 50 ท่าน", 5500, 3, 14, "lin"),
    ("ชุดจัดเลี้ยง", "ชุดต้อนรับแขก VIP", 2900, 5, 18, "lin"),
]
# กาแฟโอ๊ก — เปิดตัว 1 ต.ค. 2026 ตามบันทึกการประชุม (มีข้อมูลเฉพาะ ต.ค.-ธ.ค.)
OAK = [("แก้วเดี่ยว", "กาแฟโอ๊ก (แก้วเดี่ยว)", 70, {9: 350, 10: 450, 11: 520}),
       ("เหยือกใหญ่", "เหยือกกาแฟโอ๊ก", 470, {9: 40, 10: 70, 11: 95})]

# seasonal index applied to the new SKUs only (original 18 keep their exact numbers)
SEASON = [0.95, 1.00, 1.05, 0.90, 1.00, 1.02, 1.09, 1.22, 1.05, 1.20, 1.22, 1.32]


def lin(a, b, i, n=11):
    return round(a + (b - a) * i / n)


monthly = {}          # (mi, หมวด, สินค้า) -> [จำนวน, ราคา, ยอดขายรวม]
for mi, prod, qty, price, rev in ORIGINAL_18:
    assert qty * price == rev, (prod, qty, price, rev)
    monthly[(mi, "แก้วเดี่ยว", prod)] = [qty, price, rev]

for cat, prod, price, jan, dec, _ in NEW_SKUS:
    for mi in range(12):
        if prod in ("กาแฟดำ", "ชาเขียว", "ลาเต้"):          # ต่อจาก มิ.ย. ของ SKU เดิม
            if mi < 6:
                continue
        base = lin(jan, dec, mi)
        qty = round(base * SEASON[mi])
        monthly[(mi, cat, prod)] = [qty, price, qty * price]

# กาแฟโอ๊กเปิดตัว 1 ต.ค. 2026 จึงมีข้อมูลเฉพาะ ต.ค.-ธ.ค.
for cat, prod, price, per_month in OAK:
    for mi, qty in per_month.items():
        monthly[(mi, cat, prod)] = [qty, price, qty * price]

# ------------------------------------------------------------ daily weights
HOLIDAYS = {  # วันหยุดนักขัตฤกษ์ที่ลงวันที่แน่นอน (ไม่รวมวันสำคัญทางจันทรคติ)
    (1, 1): 0.50, (4, 6): 0.60, (4, 13): 0.35, (4, 14): 0.35, (4, 15): 0.35,
    (5, 1): 0.70, (5, 4): 0.60, (8, 12): 0.80, (10, 23): 0.65, (12, 5): 0.70,
    (12, 10): 0.70, (12, 31): 1.45,
}
CAT_DAY = {  # ตัวคูณตามประเภทวัน ต่อหมวด
    "แก้วเดี่ยว": {"sat": 1.25, "sun": 0.85, "hol": 0.60},
    "เหยือกใหญ่": {"sat": 1.20, "sun": 0.90, "hol": 0.70},
    "ชุดจัดเลี้ยง": {"sat": 1.30, "sun": 1.10, "hol": 0.50},
}


def weights(y, m, cat):
    """น้ำหนักต่อวันของเดือนหนึ่ง (ก่อนปรับให้ผลรวมเท่าที่ต้องการ)"""
    out = []
    d = date(y, m, 1)
    while d.month == m:
        hol = HOLIDAYS.get((d.month, d.day))
        if hol is not None:
            w = CAT_DAY[cat]["hol"] * (1.45 if (d.month, d.day) == (12, 31) else 1.0)
        elif d.weekday() == 5:
            w = CAT_DAY[cat]["sat"]
        elif d.weekday() == 6:
            w = CAT_DAY[cat]["sun"]
        else:
            w = 1.0
        # อีเวนต์ก่อนวันหยุดใหญ่: ชุดจัดเลี้ยงมีออเดอร์ล่วงหน้า
        if cat == "ชุดจัดเลี้ยง" and hol is not None and 1 <= d.day <= 28:
            nxt = d + timedelta(days=1)
            if (nxt.month, nxt.day) in HOLIDAYS and HOLIDAYS[(nxt.month, nxt.day)] < 0.8:
                w *= 1.60
        out.append((d, w))
        d += timedelta(days=1)
    return out


def allocate(total, ws):
    """แบ่ง total ตามน้ำหนัก ws เป็นจำนวนเต็ม ผลรวมต้องเท่า total เป๊ะ"""
    s = sum(w for _, w in ws)
    raw = [total * w / s for _, w in ws]
    base = [int(x) for x in raw]
    rem = total - sum(base)
    order = sorted(range(len(raw)), key=lambda i: (raw[i] - base[i]), reverse=True)
    for i in order[:rem]:
        base[i] += 1
    return base


# daily[(iso_date, หมวด)] -> [จำนวนชิ้น, ยอดขายรวม]
daily = {}
for mi in range(12):
    for cat in ("แก้วเดี่ยว", "เหยือกใหญ่", "ชุดจัดเลี้ยง"):
        skus = [(p, v) for (m2, c2, p), v in monthly.items() if m2 == mi and c2 == cat]
        ws = weights(YEAR, mi + 1, cat)
        dqty = [0] * len(ws)
        drev = [0] * len(ws)
        for prod, (qty, price, rev) in sorted(skus):
            alloc = allocate(qty, ws)
            assert sum(alloc) == qty
            for i, q in enumerate(alloc):
                dqty[i] += q
                drev[i] += q * price
        for i, (d, _) in enumerate(ws):
            daily[(d.isoformat(), cat)] = [dqty[i], drev[i]]

# ------------------------------------------------------------ write monthly CSV
rows = []
for mi in range(12):
    for cat_th in ("แก้วเดี่ยว", "เหยือกใหญ่", "จัดเลี้ยง"):
        cat = CAT[cat_th]
        for (m2, c2, p), (qty, price, rev) in monthly.items():
            if m2 == mi and c2 == cat:
                rows.append([MONTHS[mi], cat_th, p, qty, price, rev])
    # เรียงสินค้าเดิม (กาแฟดำ/ชาเขียว/ลาเต้) ขึ้นก่อนในหมวดแก้วเดี่ยว
with open(f"{OUT}/monthly-sales.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["เดือน", "หมวด", "สินค้า", "จำนวน", "ราคาต่อหน่วย", "ยอดขายรวม"])
    w.writerows(rows)

# ------------------------------------------------------------ write daily CSV
ORDER_CAT = ["แก้วเดี่ยว", "เหยือกใหญ่", "ชุดจัดเลี้ยง"]
ORDERS_DIV = {"แก้วเดี่ยว": 2.3, "เหยือกใหญ่": 1.8, "ชุดจัดเลี้ยง": 1.1}
drows = []
d = date(YEAR, 1, 1)
while d.year == YEAR:
    for cat in ORDER_CAT:
        qty, rev = daily[(d.isoformat(), cat)]
        orders = 0 if qty == 0 else max(1, round(qty / ORDERS_DIV[cat]))
        drows.append([d.isoformat(), cat, qty, rev, orders])
    d += timedelta(days=1)
with open(f"{OUT}/daily-sales-2026.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["วันที่", "หมวด", "จำนวนชิ้น", "ยอดขายรวม", "จำนวนออเดอร์"])
    w.writerows(drows)

# ------------------------------------------------------------ customer master
FIRST = [  # (ชื่อ, เพศ, roman)
    ("สมชาย", "นาย", "somchai"), ("สาวี", "นางสาว", "savee"), ("นที", "นาย", "natee"),
    ("ปาริชาติ", "นางสาว", "parichat"), ("อนุชา", "นาย", "anutcha"), ("กมลชนก", "นางสาว", "kamonchanok"),
    ("วีระ", "นาย", "weera"), ("ณัฐริกา", "นางสาว", "nattarika"), ("ธนกร", "นาย", "thanakorn"),
    ("สุนิสา", "นางสาว", "sunisa"), ("ปรีชา", "นาย", "preecha"), ("วราภรณ์", "นาง", "waraporn"),
    ("ศักดา", "นาย", "sakda"), ("อรุณี", "นาง", "arunee"), ("กิตติ", "นาย", "kitti"),
    ("จิราพร", "นางสาว", "jiraporn"), ("เอกชัย", "นาย", "ekachai"), ("ทิพวรรณ", "นาง", "tipawan"),
    ("ชัยวัฒน์", "นาย", "chaiwat"), ("นภาพร", "นางสาว", "napaporn"), ("ณัฐพงษ์", "นาย", "nattapong"),
    ("พิมพ์ชนก", "นางสาว", "pimchanok"), ("พงศกร", "นาย", "pongsakorn"), ("รัตนา", "นาง", "rattana"),
    ("รัฐพล", "นาย", "ratthaphon"), ("ลลิตา", "นางสาว", "lalita"), ("สุรชัย", "นาย", "surachai"),
    ("ศิริพร", "นาง", "siriporn"), ("อดิศร", "นาย", "adisorn"), ("อุษา", "นาง", "usa"),
    ("จตุรงค์", "นาย", "jaturong"), ("เพ็ญศรี", "นาง", "phensri"), ("ธีรภัทร", "นาย", "teerapat"),
    ("มณีรัตน์", "นางสาว", "maneerat"), ("นครินทร์", "นาย", "nakharin"), ("ดวงใจ", "นาง", "duangjai"),
    ("ปิยะ", "นาย", "piya"), ("กนกวรรณ", "นางสาว", "kanokwan"), ("วัฒนา", "นาย", "wattana"),
    ("ชนัญชิดา", "นางสาว", "chananchida"),
]
LAST = [  # (นามสกุล, roman)
    ("ใจดี", "jaidee"), ("รักงาน", "rakngan"), ("แสงทอง", "saengthong"), ("งามดี", "ngamdee"),
    ("วิเศษ", "wiset"), ("สุขสวัสดิ์", "sukhasawat"), ("ศรีสุข", "srisuk"), ("บุญมี", "boonmee"),
    ("ทองคำ", "thongkham"), ("พูลสวัสดิ์", "poonsawat"), ("จันทร์เพ็ญ", "chanpen"),
    ("วงศ์สว่าง", "wongsawang"), ("สายทอง", "saitong"), ("เรืองรอง", "ruengrong"),
    ("มั่นคง", "mankong"), ("ดวงแก้ว", "duangkaew"), ("นาคทอง", "nakthong"), ("ปิ่นทอง", "pinthong"),
    ("หาญกล้า", "hankla"), ("ชุ่มใจ", "chumjai"), ("ทรัพย์เจริญ", "sapcharoen"),
    ("ก้องเกียรติ", "kongkiat"), ("เกษมสุข", "kasemsuk"), ("อินทร์ทอง", "inthong"),
    ("สมบูรณ์", "somboon"), ("สมใจ", "somjai"), ("ศรีวิไล", "sriwilai"),
]
assert len(FIRST) == 40 and len(LAST) == 27  # 40 x 27 = 1,080

ORGS = [  # (ชื่อบริษัท, โดเมน, ประเภทลูกค้า, จังหวัด)
    ("บริษัท ไทยคอฟฟี่ จำกัด", "thaicoffee.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("บริษัท กรีนที จำกัด", "greentea.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("บริษัท ริทเวลล์ จำกัด", "retailwell.co.th", "ร้านค้าปลีก", "กรุงเทพมหานคร"),
    ("ร้านกาแฟ โอ๊ก", "oakcoffee.com", "ร้านอาหารและคาเฟ่", "กรุงเทพมหานคร"),
    ("บริษัท สยามเทค โซลูชันส์ จำกัด", "siamtech.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("บริษัท อักษรพริ้นติ้ง จำกัด", "aksornprint.co.th", "ลูกค้าองค์กร", "นนทบุรี"),
    ("บริษัท กรุงไทยโลจิสติกส์ จำกัด", "ktlogistics.co.th", "ลูกค้าองค์กร", "สมุทรปราการ"),
    ("บริษัท ฟินเทค วัน จำกัด", "fintechone.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("บริษัท บ้านและที่ดิน พร็อพเพอร์ตี้ จำกัด", "banland.co.th", "ลูกค้าองค์กร", "ปทุมธานี"),
    ("บริษัท เมดิแคร์ เฮลท์ จำกัด", "medicare.co.th", "ลูกค้าองค์กร", "ขอนแก่น"),
    ("บริษัท เชียงใหม่คราฟต์ จำกัด", "cmcraft.co.th", "ลูกค้าองค์กร", "เชียงใหม่"),
    ("บริษัท ภูเก็ตมารีน จำกัด", "phuketmarine.co.th", "ลูกค้าองค์กร", "ภูเก็ต"),
    ("บริษัท หาดใหญ่ซีฟู้ด จำกัด", "hadyaisf.co.th", "ลูกค้าองค์กร", "สงขลา"),
    ("บริษัท นครราชสีมา อิเล็กทริก จำกัด", "koratelectric.co.th", "ลูกค้าองค์กร", "นครราชสีมา"),
    ("บริษัท อุบลเกษตรภัณฑ์ จำกัด", "ubonagri.co.th", "ลูกค้าองค์กร", "อุบลราชธานี"),
    ("เอเจนซีโฆษณา พระรามเก้า", "rama9ads.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("สำนักงานบัญชี รัชดา", "ratchadaacc.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("คลินิกทันตกรรม ยิ้มสวย", "yimsuay.com", "โรงพยาบาลและคลินิก", "กรุงเทพมหานคร"),
    ("โรงพยาบาล เมืองนนท์", "muangnonhosp.go.th", "โรงพยาบาลและคลินิก", "นนทบุรี"),
    ("โรงพยาบาล ราชบุรีรวมใจ", "ratchaburihosp.go.th", "โรงพยาบาลและคลินิก", "ราชบุรี"),
    ("โรงเรียน สาธิตวิทยา", "satitwittaya.ac.th", "โรงเรียนและมหาวิทยาลัย", "นครปฐม"),
    ("มหาวิทยาลัย เทคโนโลยีลานนา", "lannatech.ac.th", "โรงเรียนและมหาวิทยาลัย", "เชียงใหม่"),
    ("วิทยาลัยอาชีวะ ชลบุรี", "chonvoc.ac.th", "โรงเรียนและมหาวิทยาลัย", "ชลบุรี"),
    ("เทศบาลนคร สุราษฎร์ธานี", "suratcity.go.th", "หน่วยงานราชการ", "สุราษฎร์ธานี"),
    ("การไฟฟ้าส่วนภูมิภาค สาขาลำปาง", "pealampang.go.th", "หน่วยงานราชการ", "ลำปาง"),
    ("การประปานครหลวง ฝ่ายสาขา", "mwa.co.th", "หน่วยงานราชการ", "กรุงเทพมหานคร"),
    ("โรงแรม แม่น้ำโขง ริเวอร์ไซด์", "mekongriver.co.th", "โรงแรมและที่พัก", "หนองคาย"),
    ("โรงแรม เกาะสมุย บีช รีสอร์ท", "samuibeach.th", "โรงแรมและที่พัก", "สุราษฎร์ธานี"),
    ("โฮสเทล อยุธยา โอลด์ทาวน์", "ayutthayahostel.com", "โรงแรมและที่พัก", "พระนครศรีอยุธยา"),
    ("คาเฟ่ บ้านสวน เพลิน", "bansuanplearn.com", "ร้านอาหารและคาเฟ่", "เชียงราย"),
    ("ร้านอาหาร ป้าแต๋ว ต้มยำ", "pataew.com", "ร้านอาหารและคาเฟ่", "ขอนแก่น"),
    ("เบเกอรี อบหอม", "obhom.co.th", "ร้านอาหารและคาเฟ่", "นครราชสีมา"),
    ("ศูนย์อาหาร ไทยสมายล์", "thaismilefood.co.th", "ร้านค้าปลีก", "กรุงเทพมหานคร"),
    ("ซูเปอร์มาร์เก็ต เมืองทอง", "muangthongmart.co.th", "ร้านค้าปลีก", "ปทุมธานี"),
    ("มินิมาร์ท ซีเล็คช็อป", "selectshop.co.th", "ร้านค้าปลีก", "ชลบุรี"),
    ("บริษัท อีสานก่อสร้าง จำกัด", "isarnbuild.co.th", "ลูกค้าองค์กร", "ร้อยเอ็ด"),
    ("บริษัท สงขลาประมง จำกัด", "songkhlafish.co.th", "ลูกค้าองค์กร", "สงขลา"),
    ("สำนักงานทนายความ ยุติธรรม", "yutithamlaw.co.th", "ลูกค้าองค์กร", "กรุงเทพมหานคร"),
    ("สหกรณ์การเกษตร เชียงราย", "crcoop.co.th", "หน่วยงานราชการ", "เชียงราย"),
    ("บริษัท พัทยา อีเวนต์ จำกัด", "pattayaevent.co.th", "ลูกค้าองค์กร", "ชลบุรี"),
]

POS = {
    "ลูกค้าองค์กร": ["ผู้จัดการฝ่ายจัดซื้อ", "เจ้าหน้าที่จัดซื้อ", "ผู้จัดการฝ่ายปฏิบัติการ",
                     "เจ้าหน้าที่ธุรการ", "ผู้ช่วยผู้จัดการ", "เลขานุการบริษัท"],
    "ร้านค้าปลีก": ["เจ้าของร้าน", "ผู้จัดการร้านค้า", "พนักงานขาย", "หัวหน้าสาขา"],
    "ร้านอาหารและคาเฟ่": ["เจ้าของร้าน", "ผู้จัดการร้าน", "หัวหน้าบาร์", "พนักงานขาย"],
    "โรงแรมและที่พัก": ["ผู้จัดการฝ่ายอาหารและเครื่องดื่ม", "หัวหน้าแผนกต้อนรับ", "เจ้าหน้าที่จัดซื้อ"],
    "โรงเรียนและมหาวิทยาลัย": ["เจ้าหน้าที่พัสดุ", "หัวหน้าฝ่ายอาคารสถานที่", "เจ้าหน้าที่ธุรการ"],
    "โรงพยาบาลและคลินิก": ["หัวหน้าฝ่ายโภชนาการ", "เจ้าหน้าที่จัดซื้อ", "ผู้จัดการอาคาร"],
    "หน่วยงานราชการ": ["เจ้าพนักงานพัสดุ", "เจ้าหน้าที่ธุรการ", "หัวหน้าฝ่ายบริหารทั่วไป"],
}
TIER_AMT = {  # (ระดับ, ช่วงยอดซื้อสะสม)
    "A": (900_000, 4_800_000), "B": (250_000, 900_000), "C": (40_000, 250_000),
}

ORIGINAL6 = [
    ("CUS-0001", "นาย สมชาย ใจดี", "ผู้จัดการฝ่ายขาย", "บริษัท ไทยคอฟฟี่ จำกัด", "ลูกค้าองค์กร", "กรุงเทพมหานคร", "somchai@thaicoffee.co.th", "081-234-5678"),
    ("CUS-0002", "นางสาว สาวี รักงาน", "เจ้าหน้าที่การตลาด", "บริษัท กรีนที จำกัด", "ลูกค้าองค์กร", "กรุงเทพมหานคร", "savee@greentea.co.th", "082-345-6789"),
    ("CUS-0003", "นาย นที แสงทอง", "เจ้าหน้าที่จัดซื้อ", "บริษัท ไทยคอฟฟี่ จำกัด", "ลูกค้าองค์กร", "กรุงเทพมหานคร", "natee@thaicoffee.co.th", "083-456-7890"),
    ("CUS-0004", "นางสาว ปาริชาติ งามดี", "ผู้จัดการร้านค้า", "บริษัท ริทเวลล์ จำกัด", "ร้านค้าปลีก", "กรุงเทพมหานคร", "parichat@retailwell.co.th", "084-567-8901"),
    ("CUS-0005", "นาย อนุชา วิเศษ", "เจ้าของร้าน", "ร้านกาแฟ โอ๊ก", "ร้านอาหารและคาเฟ่", "กรุงเทพมหานคร", "anutcha@oakcoffee.com", "085-678-9012"),
    ("CUS-0006", "นางสาว กมลชนก สุขสวัสดิ์", "พนักงานขาย", "บริษัท ไทยคอฟฟี่ จำกัด", "ลูกค้าองค์กร", "กรุงเทพมหานคร", "kamonchanok@thaicoffee.co.th", "086-789-0123"),
]

used = {("somchai", "jaidee"), ("savee", "rakngan"), ("natee", "saengthong"),
        ("parichat", "ngamdee"), ("anutcha", "wiset"), ("kamonchanok", "sukhasawat")}
crow = []
for code, name, pos, org, typ, prov, mail, phone in ORIGINAL6:
    tier = rng.choice(["A", "A", "B"])
    lo, hi = TIER_AMT[tier]
    crow.append([code, name, pos, org, typ, prov, mail, phone, "2026-01-05", tier, rng.randrange(lo, hi, 500), "ใช้งาน"])

combos = []
for (fn, prefix, fr), (ln, lr) in ((a, b) for a in FIRST for b in LAST):
    handle = f"{fr}.{lr}"
    if (fr, lr) in used:
        continue
    combos.append((fn, prefix, fr, ln, lr, handle))
assert len(combos) == 1074, len(combos)

for i, (fn, prefix, fr, ln, lr, handle) in enumerate(combos, start=7):
    org, dom, typ, prov = ORGS[rng.randrange(len(ORGS))]
    pos = POS[typ][rng.randrange(len(POS[typ]))]
    # วันที่สมัคร: กระจายทั้งปี 2026 เอนไปทางปลายปี (ฐานลูกค้าโต)
    doy = int(3 + (rng.random() ** 0.75) * 350)
    signup = (date(2026, 1, 1) + timedelta(days=min(doy, 358))).isoformat()
    tier = rng.choices(["A", "B", "C"], weights=[0.18, 0.47, 0.35])[0]
    lo, hi = TIER_AMT[tier]
    amount = rng.randrange(lo, hi, 500)
    status = rng.choices(["ใช้งาน", "รอเปิดบัญชี", "พักใช้งาน", "ปิดบัญชี"], weights=[0.85, 0.05, 0.06, 0.04])[0]
    if rng.random() < 0.15:  # 15% ใช้เบอร์สำนักงาน (รหัสพื้นที่จริง + 02 สำหรับกรุงเทพฯ)
        area = rng.choice(["02", "02", "02", "053", "043", "038", "074", "076", "044",
                           "034", "032", "056", "073", "042", "077"])
        phone = f"{area}-{rng.randrange(100,999):03d}-{rng.randrange(1000,9999):04d}"
    else:
        phone = f"0{8 if rng.random() < 0.75 else 9}{rng.randrange(1,10)}-{rng.randrange(100,999):03d}-{rng.randrange(1000,9999):04d}"
    crow.append([f"CUS-{i:04d}", f"{prefix} {fn} {ln}", pos, org, typ, prov,
                 f"{handle}@{dom}", phone, signup, tier, amount, status])

with open(f"{OUT}/customer-contacts.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["รหัสลูกค้า", "ชื่อ-นามสกุล", "ตำแหน่ง", "บริษัท", "ประเภทลูกค้า", "จังหวัด",
                "อีเมล", "โทรศัพท์", "วันที่สมัคร", "ระดับลูกค้า", "ยอดซื้อสะสม(บาท)", "สถานะ"])
    w.writerows(crow)

# ------------------------------------------------------------------ verify
assert len(crow) == 1080, len(crow)
assert len(rows) == 222, len(rows)
assert len(drows) == 1095, len(drows)

# 18 แถวเดิมต้องอยู่ครบและค่าเท่าเดิม
have = {(mi, p): (q, pr, rv) for mi in range(12)
        for (m2, c2, p), (q, pr, rv) in monthly.items() if m2 == mi and False}
flat = {}
for mi in range(12):
    for (m2, c2, p), v in monthly.items():
        if m2 == mi:
            flat[(m2, p)] = tuple(v)
for mi, prod, qty, price, rev in ORIGINAL_18:
    assert flat[(mi, prod)] == (qty, price, rev), (mi, prod, flat[(mi, prod)])

# daily ต้องรวมได้เท่า monthly ทุก (เดือน, หมวด)
agg = {}
for d_iso, cat, qty, rev, _o in drows:
    m = int(d_iso.split("-")[1]) - 1
    a = agg.setdefault((m, cat), [0, 0])
    a[0] += qty
    a[1] += rev
for (m, cat), v in agg.items():
    tot = [0, 0]
    for (m2, c2, p), (q, pr, rv) in monthly.items():
        if m2 == m and c2 == cat:
            tot[0] += q
            tot[1] += rv
    assert v == tot, (m, cat, v, tot)

print("monthly-sales.csv      rows:", len(rows))
print("daily-sales-2026.csv   rows:", len(drows))
print("customer-contacts.csv  rows:", len(crow))
ym, yr = 0, 0
for (m, cat), (q, r) in sorted(agg.items()):
    yr += r
print("ยอดขายรวมทั้งปี 2026 :", f"{yr:,} บาท")
aug = sum(r for (m, cat), (q, r) in agg.items() if m == 7)
print("ยอดขาย ส.ค. 2026     :", f"{aug:,} บาท", "| เฉลี่ย/สัปดาห์:", f"{aug // 4:,} บาท")
print("OK — invariants passed")
