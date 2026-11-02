# ReguGuard AI — Texnik vazifa (TZ) v1.0

ReguGuard AI — kompaniyalarning dasturiy ta'minoti va AI tizimlarini EU AI Act va GDPR bo'yicha skanerlab, nemis tilida «Readiness & Gap Audit Report» (PDF) chiqaradigan, Yevropada joylashgan B2B SaaS. Holat: 2026-yil 2-noyabr.

## 1. Maqsad va qiymat taklifi

**Muammo.** Nemis KMUlari va korporatsiyalari AI Act, GDPR va tegishli standartlar bo'yicha o'z tizimlarini qo'lda, yuristlar va konsultantlar bilan, qimmat va sekin tekshiradi.

**Yechim.** Platforma kod, konfiguratsiya, hujjat va ma'lumotlar oqimini avtomatik tahlil qiladi, har bir topilmani aniq qonun moddasiga bog'laydi va ustuvorlashtirilgan tuzatish rejasi beradi.

**Maqsadli foydalanuvchilar.**

- CTO / Head of Engineering — texnik topilmalar va tuzatish rejasi
- Datenschutzbeauftragter (DSB) va Compliance Officer — GDPR/AI Act hisobotlari
- Konsalting firmalari — o'z mijozlari uchun white-label audit

**Muvaffaqiyat mezonlari (MVP).**

- Bitta repozitoriy uchun to'liq skan: 15 daqiqadan kam (≤ 100 000 qator kod)
- Har bir topilma kamida bitta aniq modda/bandga havola qiladi (havolasiz topilma chiqarilmaydi)
- EN/DE/UZ hisobotni 1 bosishda yaratish: 60 soniyadan kam; PDF/A talabi release mezonlari bilan tekshiriladi

## 2. Huquqiy asos va muhim chegaralar

**Eng muhim qaror: mahsulot «sertifikat» bermaydi.** AI Act bo'yicha rasmiy muvofiqlik baholashni provayderning o'zi yoki notified body bajaradi va CE-belgisi shu yo'l bilan beriladi. Dasturiy vosita buni o'rnini bosa olmaydi. Shuning uchun hujjat nomi: **«Compliance Readiness & Gap Assessment Report»**, nemischa **«Konformitäts-Bereitschaftsbericht»**. «Sertifikat» so'zi UI, PDF va marketingda ishlatilmaydi. Bu nemis yuristlari ishonchini ham oshiradi va chalg'ituvchi reklama (UWG) xavfini kamaytiradi.

**Xavf toifasi kodning o'zidan emas, intended purpose va kontekstdan kelib chiqadi.** Bir xil kod HR skriningda ishlatilsa boshqa, spam filtrida ishlatilsa boshqa baholanishi mumkin. Shu sababli tizim majburiy use-case anketasini (maqsad, foydalanuvchilar, qaror ta'siri) yig'adi. Platforma ko'rsatadigan toifa — tekshiruv uchun indikativ natija; rasmiy huquqiy tasnif yoki muvofiqlik xulosasi emas.

## 3. Regulyator kontekst (2026-11-02 holati)

Quyidagi jadval dastlabki rejalashtirish uchun mo'ljallangan va ishlab chiqarishdagi huquqiy manba hisoblanmaydi. AI Act muddatlari va Digital Omnibus haqidagi da'volar rasmiy kuchga kirgan matn bilan tasdiqlanmaguncha **tekshirilmagan** deb qaraladi. Ishlab chiqarishga chiqarishdan oldin yurist/EU AI Act mutaxassisi har bir talab, sana va havolani EUR-Lex hamda tegishli regulyatorning rasmiy nashridan tekshirishi, tekshiruv sanasi va manba versiyasini Regulatory KB'ga kiritishi shart. Ikkilamchi maqolalar faqat izlash uchun yordamchi manbadir.

| Talab | Qo'llanish sanasi | Platforma moduli |
| --- | --- | --- |
| Taqiqlangan amaliyotlar va AI savodxonligi (AI literacy) | 2025-02-02 dan amalda | Prohibited-practice skaneri |
| GPAI (umumiy maqsadli AI) majburiyatlari | 2025-08-02 dan amalda | GPAI provayder/deployer checklist |
| Shaffoflik (Art. 50) | 2026-08-02 dan amalda deb xabar qilinadi, tekshirish kerak | Transparency tekshiruvi |
| Mustaqil yuqori xavfli tizimlar (Annex III: HR, kredit, ta'lim va h.k.) | 2027-12-02 (avval 2026-08-02) | To'liq gap-analiz |
| Mahsulotga o'rnatilgan yuqori xavfli AI (Annex I) | 2028-08-02 (avval 2027-08-02) | To'liq gap-analiz |
| GDPR | Amalda | PII pipeline, DPIA yordamchisi |
| NIS2, Cyber Resilience Act | Keyingi bosqich | v2 modullari |

Muhim: **Regulatory Knowledge Base (KB) versiyalanadi**. Har bir talab uchun yurisdiksiya, rasmiy manba URL'i, hujjat/versiya, tegishli modda/band, amal qilish sanasi, tekshiruvchi va tekshirilgan sana saqlanadi. Har bir hisobot KB versiyasi va sanasini ko'rsatadi. Yangi KB versiyasi eski hisobotni o'zgartirmaydi; tegishli talab o'zgarganda hisobot «qayta ko'rib chiqish kerak» deb belgilanadi. Rasmiy manba yoki yuridik tasdiq yo'q bo'lsa, tizim talabni tasdiqlangan huquqiy xulosa sifatida ko'rsatmaydi.

Manbalar: [AI Omnibus (Reg. (EU) 2026/1744) sharhi](https://www.softwareimprovementgroup.com/eu-ai-act-summary/), [Gibson Dunn tahlili](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/), [Mondaq](https://www.mondaq.com/eu-digital-omnibus-on-ai-enters-into-force/1825722).

## 4. Maxfiylik dizayni (mijoz kodi — bu nozik ma'lumot)

Mijoz kodini tashqi LLM API'ga yuborish o'zi GDPR va tijorat sirlari xavfi. Shu sababli:

1. **EU-only qayta ishlash.** Production ma'lumotlari uchun tanlangan hosting, backup, log va AI sub-processor'lar EU hududida bo'lishi kerak. EU regionning o'zi GDPR muvofiqligini kafolatlamaydi: DPA, subprocessors, transfer mexanizmi va konfiguratsiya alohida tekshiriladi.
2. **Model rejimlari.** Arxitektura self-hosted model, tasdiqlangan EU-region API va keyinchalik BYOK'ni qo'llashi mumkin. MVP default'i — self-hosted yoki model ishlatmasdan qoidalarga asoslangan tahlil; tashqi API faqat tenant aniq yoqib, DPA/data residency tekshirilgandan keyin. BYOK MVP scope'iga kirmaydi.
3. **Mijoz ma'lumoti bilan model o'qitilmaydi.** Shartnoma va texnik jihatdan: training uchun log saqlanmaydi.
4. **Minimizatsiya.** LLM'ga butun repo emas, faqat tegishli parchalar (chunk) yuboriladi; secrets va PII oldindan maskalanadi.
5. **Saqlash muddati.** Yuklangan manba kod skandan keyin standart bo'yicha 7 kun ichida o'chiriladi (sozlanadi). Topilma va hisobotda qolishi mumkin bo'lgan kod parchasi alohida redaksiya va retention siyosatiga bo'ysunadi; ularni saqlash uchun maqsad, ruxsat va o'chirish muddati belgilanadi.
6. **Hujjatlar to'plami:** AVV (Auftragsverarbeitungsvertrag, GDPR Art. 28), TOM ro'yxati, sub-processor ro'yxati, Impressum va Datenschutzerklärung.

## 5. Arxitektura va texnologiyalar

MVP'da uchta deploy qilinadigan ilova komponenti bo'ladi: Java Core API, Python AI Engine va React Web. PostgreSQL, Redis va obyekt xotira — ilova xizmatlari emas, boshqariladigan infratuzilma bog'liqliklaridir. Java Core tenant, xavfsizlik, API, job holati va hisobotni boshqaradi; Python esa izolyatsiyalangan tahlil worker'i sifatida ishlaydi.

| Komponent | Texnologiya | Vazifasi |
| --- | --- | --- |
| Enterprise Core | Java 21 (LTS) + Spring Boot 3.x, Spring Security, Spring Modulith, Flyway | Tenant, foydalanuvchi, RBAC, audit log, job orkestratsiyasi va PDF |
| AI Engine | Python 3.12, FastAPI, LangGraph/LlamaIndex, Pydantic v2 | Agentlar, RAG, PII aniqlash, topilmalarni generatsiya qilish |
| Ma'lumotlar | PostgreSQL 16, Redis navbat, S3-mos obyekt xotira | Relyatsion ma'lumot, job navbati, manba fayllari va hisobotlar |
| Frontend | React 18 + TypeScript + Vite + TailwindCSS + TanStack Query | Dashboard, hisobot ko'rinishi, i18n (EN/DE/UZ) |
| Hisobot | Java: OpenHTMLtoPDF yoki JasperReports; Thymeleaf shablon | EN/DE/UZ hisobot, PDF/A talabi release mezonlariga muvofiq |
| Kuzatuv | OpenTelemetry, Prometheus, Grafana, Loki | Metrikalar, trace, log |
| DevOps | Docker, GitHub Actions, Terraform, Hetzner Cloud (yoki AWS eu-central-1) | CI/CD, IaC, deploy |

**Aloqa.** Frontend faqat Core API bilan gaplashadi (REST + OpenAPI 3.1). MVP'da Core ↔ AI Engine ichki REST, xizmat identifikatsiyasi va mTLS bilan ishlaydi; tashqi tarmoqdan AI Engine'ga kirish taqiqlanadi. Uzoq skanlar Redis Streams orqali asinxron bajariladi, job holati Core'da saqlanadi. Bir dona navbat texnologiyasi tanlanadi; MVP'da Redis Streams ishlatiladi, RabbitMQ muqobilini parallel joriy etilmaydi. AI Engine DB'ga to'g'ridan-to'g'ri yozmaydi — versiyalangan sxemaga mos natijani Core'ga qaytaradi. Har bir job idempotent bo'lishi, qayta urinishlar chegaralangan bo'lishi va o'lik xabarlar kuzatilishi kerak.

**Nega bu bo'linish.** Java qismi tenant izolyatsiyasi, audit va SSO'ni barqaror ushlaydi; Python qismi tez o'zgaruvchan AI kodini ajratib turadi va mustaqil deploy qilinadi.

## 6. Funksional talablar

| ID | Talab | Ustuvorlik |
| --- | --- | --- |
| FR-1 | Yuklash: ZIP, GitHub/GitLab read-only ulanish yoki CI uchun REST API | MVP |
| FR-2 | Use-case anketasi (intended purpose, sohasi, foydalanuvchilar, avtomatik qaror ta'siri) | MVP |
| FR-3 | AI Act bo'yicha indikativ risk skriningi: Taqiqlangan / Yuqori / Shaffoflik majburiyati / Boshqa; anketa asoslari va tasdiqlangan modda havolalari | MVP |
| FR-4 | Kod va hujjat skani: ML kutubxonalari, dataset yo'llari, loglash, saqlash, uchinchi tomon API'lar, texnik hujjat yo'qligi | MVP |
| FR-5 | PII/maxfiy ma'lumotlarni aniqlash va AI'ga yuborishdan oldin redaksiya qilish (7-bo'lim); manba fayllarini o'zgartirmaslik | MVP |
| FR-6 | Topilmalar: jiddiylik, dalil (fayl:qator), modda, tuzatish tavsiyasi, taxminiy mehnat hajmi | MVP |
| FR-7 | EN/DE/UZ hisobot, SHA-256 integrity hash'i (PDF'dan tashqari metadata/manifestda) va versiya raqami | MVP |
| FR-8 | Inson tekshiruvi: compliance officer topilmani «tasdiqlash / rad etish / izoh» qila oladi (human-in-the-loop) | MVP |
| FR-9 | Tarix va farq: ikki skan orasidagi o'zgarish (regressiya) | v1.1 |
| FR-10 | CI/CD plagin: GitHub Action, PR'da compliance gate | v1.1 |
| FR-11 | Texnik hujjat generatori (Annex IV qoralamasi), DPIA qoralamasi, VVT (Art. 30) shabloni | v1.2 |
| FR-12 | White-label, SSO (SAML/OIDC), Webhook | v2 |

## 7. GDPR anonimlashtirish pipeline

Pipeline aniq va tekshiriladigan bo'lishi kerak; faqat LLM'ga ishonilmaydi. **Redaksiya/psevdonimlash anonimlashtirish bilan bir xil emas.** MVP'da asosiy maqsad — tashqi modelga uzatiladigan parchadan PII va sirlarni olib tashlash; foydalanuvchiga qonuniy ma'noda anonimlashtirish kafolatlanmaydi. Asl manba fayllari hech qachon avtomatik ravishda tahrirlanmaydi.

1. **Aniqlash (qatlamli).** Regex va tekshiruv summalari (IBAN, telefon, Steuer-ID, PLZ), so'ng NER (Presidio + nemis modeli, masalan spaCy de\_core\_news / GLiNER), so'ng faqat noaniq holatlar uchun LLM tasdig'i.
2. **Toifalash.** Oddiy PII, maxsus toifa (Art. 9: sog'liq, din va h.k.), maxfiy kalitlar.
3. **Harakat siyosati** (tenant bo'yicha sozlanadi): tashqi AI kontekstida redaksiya/maskalash; ichki tahlilda zarur bo'lsa psevdonimlash. Qaytarilmas anonimlashtirish va format saqlovchi shifrlash MVP doirasiga kirmaydi. Har bir rejimda nima saqlanishi va kim ko'rishi hujjatlashtiriladi.
4. **Kalit boshqaruvi.** Psevdonim xaritasi MVP'da yoqilmaydi. Maydon darajasidagi shifrlash talab qilinganda, tasdiqlangan kriptografik kutubxona va KMS/Vault envelope encryption ishlatiladi; kriptografiyani qo'lda amalga oshirish taqiqlanadi. KMS provayderi tasdiqlamagan rotatsiya muddati konfiguratsiya sifatida belgilanadi va rotatsiya/backup'dan tiklash sinovdan o'tkaziladi.
5. **Sifat o'lchovi.** Har relizda versiyalangan, huquqiy asosda ishlatiladigan va ma'lumot sizib chiqarmaydigan nemis benchmarkida PII recall ≥ 0.95 va precision ≥ 0.90 maqsad qilinadi (toifalar bo'yicha alohida hisobot). Benchmark hajmi, confidence interval va test to'plami treningdan ajratilgani qayd etiladi. Maqsad bajarilmasa, release bloklanadi yoki mas'ul shaxs tasdiqlagan, hujjatlashtirilgan istisno talab qilinadi.
6. **Izoh.** Anonimlash «to'liq» bo'ladi deb va'da qilinmaydi; hisobotda qolgan xavf (re-identification risk) ochiq yoziladi.

## 8. AI Engine: agentlar va ishonchlilik

**Tahlil pipeline'i.** Bosqichlar alohida agent bo'lishi shart emas; MVP'da deterministik kod va oddiy xizmatlardan boshlanadi. LLM faqat noaniq tasnif yoki matn loyihasi uchun ishlatiladi.

1. *Intake* — use-case anketasi va repo xaritasini (til, freymvork, ML kutubxonalar) yig'adi.
2. *Classifier* — anketa asosida ehtimoliy toifani taklif qiladi; huquqiy tasnifni yakuniy deb e'lon qilmaydi.
3. *Evidence* — kod va hujjatdan dalil (fayl, qator) topadi; dalilsiz xulosa chiqarmaydi.
4. *Mapper* — dalilni faqat tasdiqlangan Regulatory KB talabiga bog'laydi.
5. *Validation* — sxema, manba, qator oralig'i va dalil mavjudligini mashina tekshiradi; LLM'ning o'z-o'zini tanqid qilishi dalil tekshiruvi o'rnini bosa olmaydi.
6. *Report* — tasdiqlangan maydonlardan shablon asosida EN/DE/UZ matn yaratadi; huquqiy xulosa yoki avtomatik muvofiqlik hukmini chiqarmaydi.

**Regulatory Knowledge Base.** Rasmiy matnlar (EUR-Lex'dagi AI Act, GDPR, EDPB/AI Office yo'riqnomalari, DSK/BfDI hujjatlari) moddasi bo'yicha bo'lingan, versiyalangan; har bir javob chunk ID bilan keladi. Lisenziya va nashr huquqi tekshiriladi.

**Ishonchlilik qoidalari.**

- Strukturalangan chiqish (Pydantic/JSON Schema). Havola KB'da mavjud bo'lmasa yoki dalil repo'dan qayta olinib tasdiqlanmasa, topilma chiqarilmaydi. Dalil uchun repozitoriy commit hash'i, fayl yo'li va 1-based qator oralig'i saqlanadi.
- Har topilmada `confidence` va «inson tekshiruvi talab qilinadi» bayrog'i.
- Prompt injection himoyasi: yuklangan kod/hujjat ishonchsiz ma'lumot hisoblanadi; LLM'da shell, repo yozish va umumiy internet vositalari yo'q. Worker tarmoq egress'i deny-by-default; parsersandbox, CPU/xotira/timeout/quota limitlari va fayl turi/size limitlari majburiy.
- Eval to'plami: kamida 150 etiketlangan namuna (xavf toifasi, topilma, modda); har PR'da regressiya testi, maqsad: toifa aniqligi ≥ 85% MVP'da, 90% v1.1'da.
- Kuzatuv: har chaqiruv uchun prompt versiyasi, model, token, kechikish, narx (PII'siz) saqlanadi.
- AI provayderi tenant uchun ruxsat etilmagan bo'lsa yoki EU data residency/DPA tekshirilmagan bo'lsa, so'rov tashqi modelga yuborilmaydi; boshqa provayderga avtomatik fallback yo'q.
- Yuklangan kod hech qachon ishga tushirilmaydi. ZIP/Git ingest path traversal, symlink, zip bomb, haddan tashqari fayl soni/hajmi, zararli encoding va parser xatolariga qarshi himoyalanadi; limit oshsa skan aniq sabab bilan to'xtaydi.
- Har bir skan `queued → running → completed | failed | cancelled` holatiga ega; progress/xato sababi UI/API'da ko'rinadi. Qayta urinishlar idempotent va chegaralangan; retention muddati tugagach source fayllari o'chiriladi.

## 9. Xavfsizlik va ma'lumotlar modeli

**Asosiy jadvallar:** `tenant`, `app_user`, `role`, `project`, `scan_run`, `finding`, `evidence`, `regulation_ref`, `report`, `audit_event`, `consent_record`, `encryption_key_meta`.

**Talablar.**

- Multi-tenant izolyatsiya: PostgreSQL Row-Level Security + har so'rovda `tenant_id`; tenant konteksti faqat server tomonda, tranzaksiya doirasida o'rnatiladi. Ilova DB roli jadval egasi yoki `BYPASSRLS` huquqiga ega bo'lmaydi; migratsiya roli alohida. REST, worker, obyekt xotira va hisobot yuklab olish yo'llari uchun tenantlararo manfiy testlar majburiy.
- Spring Security: OAuth2/OIDC, MFA (TOTP/WebAuthn), RBAC rollari: Owner, Admin, Compliance Officer, Developer, Auditor (faqat o'qish).
- Audit log o'zgarmas (append-only, hash zanjiri): kim, nima, qachon, qaysi tenant; 10 yil saqlash sozlanadi.
- Shifrlash: tashqi va xizmatlararo aloqa TLS 1.2+ (TLS 1.3 afzal), disk/object storage shifrlashi va zarur maydonlarda KMS envelope encryption; sirlar Vault/KMS'da. «AES-256-GCM»ni barcha ma'lumotga majburan qo'llash o'rniga tahdid modeli va kalit aylanishi hujjatlashtiriladi.
- OWASP ASVS L2 ga moslik; SAST (CodeQL), SCA (Dependabot, Trivy), SBOM (CycloneDX) har buildda.
- GDPR huquqlari: ma'lumot subyekti so'rovlarini bajarishga yordam beruvchi eksport/o'chirish jarayoni va tekshiriladigan audit. Qonuniy saqlash istisnolari hamda backup'dan o'chirish muddati hujjatlashtiriladi. Kriptografik o'chirish faqat ma'lumotlar haqiqatan tenantga xos kalit bilan shifrlangani va barcha nusxalar qamrab olingani tasdiqlanganda qo'llanadi.
- Rejalashtirilgan sertifikatlar: ISO 27001 va BSI C5 yo'l xaritasi (12–18 oy); MVP'da TOM hujjati.

## 10. Nofunksional talablar

| Ko'rsatkich | Maqsad (MVP) |
| --- | --- |
| Mavjudlik | 99.5% oylik (v1.1: 99.9% oylik); o'lchash va planned maintenance istisnasi hujjatlashtiriladi |
| API javob vaqti (p95), AI'siz endpointlar | < 300 ms |
| Skan (100 000 qator kod) | < 15 daqiqa; belgilangan hardware, til/fayl turlari, model va PII maskalash bilan benchmarkda o'lchanadi |
| Bir vaqtdagi skanlar | 20 job; belgilangan hardware'dagi yuklama testida, p95 navbat kutishi va xato ulushi bilan o'lchanadi |
| RPO / RTO | 1 soat / 4 soat |
| Qamrov: unit + integratsion test | ≥ 80% (Java), ≥ 75% (Python) |
| Til | UI va hisobot: EN, DE, UZ |
| Accessibility | WCAG 2.1 AA (BFSG talablariga tayyorgarlik) |

## 11. Frontend (React + TypeScript + Tailwind)

- Sahifalar: Dashboard (umumiy xavf bahosi, trend), Project, Scan natijalari, Finding tafsiloti (dalil + modda + tuzatish), Report markazi, Sozlamalar (model rejimi, saqlash muddati, rollar).
- Topilmalar jadvali: filtr (jiddiylik, modda, status), massaviy status o'zgartirish.
- Har bir topilmada «Nima uchun?» paneli: dalil, modda matni, ishonch darajasi.
- i18n (react-i18next), nemis tili birlamchi; UI va hisobot EN/DE/UZ; sana/raqam formati de-DE.
- Holat: TanStack Query; shakllar: React Hook Form + Zod; testlar: Vitest, Playwright (E2E).
- Dizayn: toza, kontrastli, kamida WCAG AA; haqiqiy hisobot misollari bilan demo rejimi.

## 12. DevOps va deploy

- Monorepo yoki 3 repo: `core`, `ai-engine`, `web`; har biri uchun Dockerfile (multi-stage, non-root).
- GitHub Actions: lint, test, SAST, SCA, image build, imzolash (cosign), staging'ga avtomatik deploy, productionga qo'lda tasdiq.
- Infratuzilma Terraform bilan: Hetzner Cloud (Falkenstein/Nuremberg) + Kubernetes (k3s) yoki Docker Compose (MVP); alternativ AWS eu-central-1.
- Backup: PostgreSQL PITR, shifrlangan; har oy tiklash mashqi.
- Muhitlar: dev, staging, prod; prod ma'lumoti stagingga ko'chirilmaydi (sintetik ma'lumot).
- Git ulanishi minimal read-only scope bilan ishlaydi; tokenlar secret store'da shifrlanadi, log/API javobiga chiqarilmaydi va uzilganda bekor qilinadi. MVP'da repository'ga write yoki PR yaratish ruxsati yo'q.

## 13. Hisobot tuzilmasi (PDF, nemis tilida)

1. Titul: mijoz, loyiha, sana, hisobot versiyasi va bilim bazasi versiyasi. PDF faylining SHA-256 hash'i PDF tashqarisidagi API metadata/manifestda beriladi; o'z hash'ini o'z ichiga olgan PDF talab qilinmaydi.
2. Rahbariyat uchun xulosa (Management Summary): xavf toifasi va 5 ta asosiy topilma
3. Qamrov va metodologiya, taxminlar va cheklovlar (nima tekshirilmadi)
4. Xavf klassifikatsiyasi: asoslar, anketa javoblari, modda havolalari
5. Topilmalar: jiddiylik, dalil, talab (Art./Annex), tavsiya, mehnat hajmi
6. GDPR bo'limi: PII xaritasi, ma'lumotlar oqimi, huquqiy asos bo'yicha savollar
7. Tuzatish yo'l xaritasi (ustuvorlashtirilgan)
8. Ilova: dalillar ro'yxati, inson tekshiruvi tarixi
9. **Huquqiy ogohlantirish:** hisobot huquqiy maslahat yoki rasmiy muvofiqlik sertifikati emas; yakuniy baholash yurist/notified body tomonidan

Format: PDF/A-2b talabi tanlangan renderer bilan prototipda tekshiriladi; PDF/A muvofiqligi validator bilan CI'da tekshiriladi. SHA-256 hash raqamli imzo emas; hash PDF tashqarisida API javobi yoki alohida manifestda beriladi. Raqamli imzo talab qilinsa, imzolovchi identifikatsiyasi, kalit boshqaruvi va imzo formati alohida talab qilinadi. Tegishli joyda sahifa raqami, jadvalli mundarija va glossariy ishlatiladi. PDF/A o'z-o'zidan WCAG accessibility talablarini kafolatlamaydi. Nemis matni native-speaker/yurist tomonidan har bir release shabloni uchun tasdiqlanadi.

## 14. Yo'l xaritasi (MVP — 12 hafta)

1. **1–2-hafta:** talablar, Regulatory KB sxemasi, repo, CI/CD, Spring Security + tenant asosi. *Gate:* login, RBAC va tenant izolyatsiya testlari ishlaydi.
2. **3–5-hafta:** xavfsiz ZIP yuklash, anketa, AI Act klassifikatsiyasi (FR-1–3), kamida 150 namunali eval to'plami. *Gate:* tasdiqlanmagan qonuniy xulosa yo'q; toifa aniqligi eval mezoniga yetadi yoki feature release'dan chiqariladi.
3. **6–8-hafta:** kod/hujjat skaneri, topilmalar, dalil ko'rsatish (FR-4, 6), dashboard. *Gate:* 3 ta ochiq-manbali demo loyihada to'liq skan.
4. **9–10-hafta:** PII pipeline, shifrlash, KMS (FR-5). *Gate:* PII recall/precision maqsadlari.
5. **11-hafta:** PDF hisobot EN/DE/UZ, human-in-the-loop (FR-7, 8). *Gate:* yurist/native-speaker tekshiruvi.
6. **12-hafta:** xavfsizlik testi, yuklama testi, pilot (2–3 kompaniya yoki konsultant). *Gate:* DoD (quyida).

**Definition of Done (MVP).** Barcha MVP FR yopilgan; kritik/yuqori zaiflik yo'q; tenant izolyatsiya testlari yashil; eval maqsadlariga erishilgan; API hujjati (OpenAPI) va runbook tayyor; pilot mijozdan yozma fikr.

## 15. Xavflar

| Xavf | Ta'siri | Chorasi |
| --- | --- | --- |
| Qonun sanalari/talablari yana o'zgaradi | Hisobot eskiradi | Versiyalangan KB, har oy huquqiy yangilanish, sanani hisobotda ko'rsatish |
| «Sertifikat» deb noto'g'ri tushunish | Yuridik javobgarlik | «Readiness Report» nomi, ogohlantirish, ToS'da javobgarlik chegarasi |
| LLM hallutsinatsiyasi | Noto'g'ri topilma | Dalil va havola majburiy, Critic agent, inson tekshiruvi |
| Mijoz kodining sizib chiqishi | Ishonch va GDPR xavfi | EU-only, self-hosted rejim, shifrlash, qisqa saqlash |
| Prompt injection yuklangan kod orqali | Manipulyatsiya | Ma'lumot/ko'rsatma ajratish, vositasiz agentlar, chiqish validatsiyasi |
| Nemis tilidagi sifat | Obro' | Glossariy, native tekshiruv, DE eval |
| Bir kishilik jamoa uchun hajm katta | Kechikish | MVP faqat 3 modul: klassifikatsiya, PII, hisobot |

## 16. Ish topish uchun portfolio strategiyasi

- **Birinchi navbatda vertikal slice:** anketa → xavf toifasi → PII skan → nemis PDF. Hammasini to'liq emas, bittasini mukammal qiling.
- Ochiq GitHub repo (core + ai-engine + web), yaxshi README (DE/EN), arxitektura diagrammasi, ADR yozuvlari, CI badge'lari, demo video 3 daqiqa.
- Jonli demo uchun sintetik ma'lumot; haqiqiy mijoz ma'lumotini ko'rsatmang.
- Intervyuda gapiring: nega Java + Python bo'linishi, tenant izolyatsiyasi, AI eval metodologiyasi, hallutsinatsiyaga qarshi choralar, «nima uchun sertifikat emas».
- Nemis tili B1 uchun: hisobot shablonlari va UI matnlarini nemis tilida o'zingiz yozib, native tekshiruvdan o'tkazing; bu texnik lug'atingizni ham oshiradi.

## 17. MVP bo'yicha boshlang'ich qarorlar

- **MVP uchun default:** umumiy B2B software jamoalari; HR/fintech kabi yuqori ta'sirli use-case'lar faqat alohida yuridik ko'rib chiqish bilan. Anketa intended purpose'ni majburiy yig'adi.
- **Model default'i:** self-hosted yoki qoidalarga asoslangan tahlil; tashqi model o'chirilgan holda boshlanadi. EU-region API alohida data-protection review'dan so'ng yoqiladi; BYOK keyingi versiya.
- **Narx modeli:** MVP texnik qabuliga ta'sir qilmaydi; pilotdan keyingi discovery'da belgilanadi.
- **Yuridik hamkor:** production release'dan oldin nomi va tasdiqlash jarayoni belgilanadigan majburiy release dependency.

## 18. Muqobil: GreenOps AI (qisqa)

Bulut (AWS/Azure/Hetzner) hisob-kitob va metrikalarini o'qib, CO₂ va xarajatni hisoblaydi, rightsizing tavsiyalari beradi. Stack: Python (ingest + ML) + Go yoki Java (collector). Nemis bozori uchun mos kelishi: CSRD hisobotlari va energiya samaradorligi talablari. Bu loyiha ReguGuard'dan texnik jihatdan sodda, lekin ishonchli «ma'lumot manbalari» (cloud billing API'lari, emissiya koeffitsientlari) kerak va raqobat ko'proq.

## 19. MVP'ni qabul qilish va ishga tushirish mezonlari

Quyidagi mezonlar bajarilmaguncha MVP production-ready deb belgilanmaydi. «100% ishlaydi» kabi absolyut kafolat o'rniga, har bir talab uchun takror bajariladigan test va natija dalili talab qilinadi.

### 19.1 MVP chegarasi

- MVP: autentifikatsiya/RBAC, tenant va loyiha, ZIP ingest, use-case anketa, repo inventarizatsiyasi, qoidalarga asoslangan skan, dalil va tasdiqlangan KB havolali topilmalar, PII/sirlarni aniqlash, inson ko'rib chiqishi, EN/DE/UZ hisobot va audit izi.
- GitHub/GitLab OAuth, BYOK, white-label, SSO, CI gate, qaytariladigan psevdonimlash, billing va to'liq DPIA/VVT generatori MVP'da majburiy emas; ular alohida milestone bo'lmaguncha UI'da mavjud deb ko'rsatilmaydi.
- LLM provayderi yo'q yoki ishonchli, dalilga tayangan natija yaratolmasa ham tizim qoidalarga asoslangan skan va xatoni to'g'ri ko'rsatishi kerak; uydirma muvaffaqiyat yoki havolasiz topilma bo'lmaydi.

### 19.2 Majburiy qabul testlari

1. **Tenant/RBAC:** tenant A foydalanuvchisi tenant B loyiha, topilma, hisobot, obyekt yoki job ID'sini API, worker va to'g'ridan-to'g'ri URL orqali o'qiy/yoza olmaydi. Har bir rol uchun ruxsat matritsasi integratsion test bilan tekshiriladi.
2. **Ingest va izolyatsiya:** normal ZIP muvaffaqiyatli olinadi; buzilgan, limitdan katta, path traversal va zip bomb namunalarida job xavfsiz to'xtaydi; source fayl bajarilmaganligi tasdiqlanadi. Xom repo log, trace, error message va model promptlariga tushmaydi.
3. **Dalil va qonun manbasi:** har bir chiqarilgan topilma mavjud fayl/qator daliliga va amaldagi, tasdiqlangan KB yozuviga ega. Dalil yoki KB yozuvi olib tashlansa, topilma validatsiyadan o'tmaydi. Qatorlar yuklangan commit hash'iga mos keladi.
4. **PII:** benchmark natijasi toifalar bo'yicha precision/recall, dataset versiyasi va test hajmi bilan saqlanadi; maqsad bajarilmasa release gate bloklaydi. Tasdiqlanmagan maskalash «anonimlashtirildi» deb da'vo qilinmaydi.
5. **Hisobot:** EN/DE/UZ til tanlovi, sahifa soni, KB versiyasi, cheklovlar va huquqiy ogohlantirish tekshiriladi; PDF format-validatsiyasi CI'dan o'tadi; PDF uchun SHA-256 API metadata/manifestda beriladi va imzo deb nomlanmaydi. Tayyor hisobot <60 soniyada yaratilishi alohida benchmark bilan o'lchanadi.
6. **Hayot sikli:** skan queue/retry/cancel/failure yo'llari, retention muddati tugagach source fayllarini o'chirish, tenant o'chirish va audit yozuvlari sinovdan o'tadi. O'chirish natijasi tekshiriladigan event bilan qayd etiladi.
7. **Ishlash:** NFR benchmarki apparat konfiguratsiyasi, repo fixture, fayl turlari, model va parallel job sonini qayd etadi. 100k qator/15 daqiqa va 20 parallel job faqat ushbu benchmark takroran o'tganda bajarildi deb hisoblanadi.
8. **Ishga tushirish:** restore mashqi RPO/RTO'ni tasdiqlaydi; alert, runbook, incident/ma'lumot buzilishi jarayoni, rollback va production secret rotation amalda mashq qilinadi.

### 19.3 Release bloklovchi shartlar

- Huquqiy KB yozuvlari tegishli yurist/mutaxassis tomonidan ko'rib chiqilmagan yoki birlamchi manbasi yo'q.
- Tenantlararo kirish, maxfiy ma'lumot chiqib ketishi yoki source code bajarilishi mumkin bo'lgan tasdiqlangan nuqson mavjud.
- Kritik/yuqori darajali ochiq xavfsizlik nuqsoni, muvaffaqiyatsiz backup restore yoki o'chirish/retention testi mavjud.
- Topilma dalilsiz, noto'g'ri modda havolasi bilan yoki hisobot «sertifikat/muvofiqlik kafolati» taassurotini berib chiqadi.

Ushbu mezonlar mahsulotning huquqiy muvofiqligini kafolatlamaydi; ular texnik MVP'ni qabul qilish uchun eng kam tekshiriladigan shartlardir.

## 20. Hozirgi mahalliy MVP holati

Amaldagi kod Python standard-library HTTP serveri, SQLite va vanilla HTML/CSS/JavaScript orqali ishlaydigan, loopback manziliga cheklangan prototipdir. U ushbu TZ'dagi Java/Spring, React/TypeScript, PostgreSQL RLS va PDF/A arxitekturasini hali amalga oshirmaydi; bajarilgan imkoniyatlar va cheklovlar loyiha ildizidagi README'da sanab o'tilgan. EN/DE/UZ UI va chop etiladigan HTML hisobot mavjud, ammo PDF/A emas. Mahalliy avtomatlashtirilgan testlarning yashil bo'lishi TZ'ning production qabul mezonlari bajarilganini yoki «100%» xatosiz ishlashni anglatmaydi.
