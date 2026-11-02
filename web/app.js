const I18N = {
  en: {
    workspace: "WORKSPACE", overview: "Overview", scans: "Scans & findings", newScan: "New assessment",
    secureWorkspace: "SECURE WORKSPACE", signIn: "Sign in", signInSub: "Access your compliance workspace.",
    workspaceName: "Workspace name", emailAddress: "Email address", password: "Password",
    passwordHint: "Use at least 12 characters. This becomes the workspace owner account.",
    createWorkspace: "Create workspace", authLocalOnly: "Accounts are stored only in this local prototype database.",
    teamAudit: "Team & audit", teamTitle: "Workspace team", teamSubtitle: "Manage workspace members and review the audit trail.",
    members: "Members", membersSub: "Users belonging to this workspace", roleCompliance: "Compliance officer",
    roleDeveloper: "Developer", roleAuditor: "Auditor (read only)", roleAdmin: "Admin",
    temporaryPassword: "Initial password", addMember: "Add member", auditLog: "Audit log", deactivate: "Deactivate",
    inactive: "Inactive", active: "Active", deactivateConfirm: "Deactivate this account and end its active sessions?",
    memberDeactivated: "Workspace account deactivated.",
    auditSub: "Recent workspace security events", signOut: "Sign out", popupBlocked: "Allow pop-ups to open the report in a new tab.", role_owner: "Owner",
    role_admin: "Admin", role_compliance_officer: "Compliance officer", role_developer: "Developer", role_auditor: "Auditor",
    noMembers: "No members found.", noAuditEvents: "No audit events.", memberAdded: "Workspace member added.",
    signedOut: "Signed out.", passwordRequired: "Password must contain at least 12 characters.",
    privacyTitle: "Private by default", privacyBody: "Repository files are scanned locally and never sent to an AI provider.", localMode: "LOCAL MODE",
    demoWorkspace: "Demo workspace", localPrototype: "Local prototype", language: "Language", overviewEyebrow: "YOUR COMPLIANCE WORKSPACE",
    welcome: "Good morning", welcomeSub: "A clearer view of your AI governance posture starts here.", startAssessment: "Start an assessment",
    prototypeTitle: "Local prototype · not production-ready", prototypeBody: "Local deployment only. Authentication is enabled, but this is not independently security-reviewed. Do not upload confidential or real personal data.",
    totalScans: "Total assessments", allTime: "All time", openFindings: "Open findings", needReview: "Need human review",
    reviewed: "Reviewed", humanValidated: "Human-validated findings", latestRisk: "Latest risk screen", indicativeOnly: "Indicative · not legal advice",
    recentAssessments: "Recent assessments", recentSub: "Your latest repository reviews", viewAll: "View all", noAssessments: "No assessments yet",
    noAssessmentsSub: "Upload a ZIP archive to start your first review.", startFirst: "Start your first scan",
    howItWorks: "How it works", methodSub: "Evidence first. People in control.", stepOne: "Share intended use",
    stepOneSub: "Risk depends on how an AI system is used—not just its code.", stepTwo: "Scan code privately",
    stepTwoSub: "Rules inspect supported files on this machine. Source code is not retained.", stepThree: "Review every signal",
    stepThreeSub: "Findings are indicators for a human—not automated legal conclusions.",
    footerNotice: "ReguGuard is a readiness tool, not a certification or legal service.",
    assessmentSetup: "ASSESSMENT SETUP", newAssessmentTitle: "Start an assessment",
    newAssessmentSub: "Tell us how the system is intended to be used, then upload a source archive.",
    useCase: "Use-case context", useCaseSub: "A risk screen needs context beyond code.", projectName: "Project name",
    sector: "Sector", selectSector: "Select a sector", general: "General software", hr: "HR & employment", finance: "Finance & credit",
    education: "Education", healthcare: "Healthcare", public: "Public services", other: "Other / unknown",
    intendedUsers: "Intended users", usersPlaceholder: "e.g. Recruiters and hiring teams", projectPlaceholder: "e.g. Candidate matching platform",
    purpose: "Intended purpose", purposePlaceholder: "Describe what the system does, who uses it, and who may be affected.",
    consequentialTitle: "Can it materially influence decisions about people?",
    consequentialSub: "For example, access to a job, education, credit, healthcare or public services.",
    repository: "Repository archive", repositorySub: "ZIP only · files are inspected locally and never executed.",
    dropTitle: "Drop your ZIP archive here", dropSub: "or browse files · max 25 MB",
    uploadFootnote: "Source files are held in memory during the scan and are not saved to disk.",
    cancel: "Cancel", runAssessment: "Run assessment", scopeTitle: "What this scan checks",
    scopeOne: "Potential credentials and exposed secrets", scopeTwo: "Email addresses and IBAN-like patterns",
    scopeThree: "AI framework and dataset references", scopeFour: "Possible special-category data indicators",
    scopeFive: "Basic technical documentation presence", scopeLimitTitle: "Important limitation",
    scopeLimitBody: "Pattern matching is not a full security or privacy audit. It can miss issues or flag false positives.",
    assessmentHistory: "ASSESSMENT HISTORY", allAssessments: "Scans & findings",
    allAssessmentsSub: "Inspect results and record human review decisions.", newAssessment: "New assessment",
    allScans: "All assessments", allScansSub: "Most recent first", searchProjects: "Search projects...",
    project: "Project", date: "Date", risk: "Risk screen", findings: "Findings", status: "Status", actions: "Actions",
    completed: "Completed", open: "Open", approved: "Approved", rejected: "Rejected", queued: "Queued", failed: "Failed",
    noSearchResults: "No matching assessments.", noFindings: "No findings from the enabled checks.",
    indicativeRisk: "Indicative risk screen", purposeLabel: "Intended purpose", sectorLabel: "Sector",
    sourceFiles: "Supported text files", report: "Open / print report", deleteScan: "Delete assessment", backToScans: "Back to assessments",
    evidence: "Evidence", legalReference: "Reference for human review", humanReview: "Human review",
    saveReview: "Save review", commentPlaceholder: "Optional review note", noComment: "No note",
    unknownRisk: "Needs review", potential_high_risk: "Potential high-impact use", transparency_review: "Transparency review",
    no_high_risk_signal: "No high-impact signal found", needs_review: "Needs more context",
    secret: "Potential exposed secret", personal_data: "Possible personal data", sensitive_data: "Possible sensitive data",
    ai_dependency: "AI framework reference", dataset_reference: "Dataset reference", missing_docs: "Technical docs not found",
    critical: "Critical", high: "High", medium: "Medium", low: "Low",
    scanSuccess: "Assessment completed. Findings are ready for human review.",
    scanFailed: "The assessment could not be completed.", selectZip: "Choose a ZIP archive first.",
    reportDownloaded: "Report is ready. SHA-256 integrity hash: ", deleteConfirm: "Permanently delete this assessment and its findings?",
    scanDeleted: "Assessment deleted.", reviewSaved: "Review decision saved.", loading: "Loading…",
    noPurpose: "No intended purpose provided.", requestError: "Request failed",
  },
  de: {
    workspace: "ARBEITSBEREICH", overview: "Übersicht", scans: "Prüfungen & Hinweise", newScan: "Neue Prüfung",
    secureWorkspace: "SICHERER ARBEITSBEREICH", signIn: "Anmelden", signInSub: "Melden Sie sich bei Ihrem Compliance-Arbeitsbereich an.",
    workspaceName: "Name des Arbeitsbereichs", emailAddress: "E-Mail-Adresse", password: "Passwort",
    passwordHint: "Mindestens 12 Zeichen. Dieses Konto erhält die Eigentümerrolle.",
    createWorkspace: "Arbeitsbereich erstellen", authLocalOnly: "Konten werden nur in der lokalen Prototyp-Datenbank gespeichert.",
    teamAudit: "Team & Audit", teamTitle: "Arbeitsbereich-Team", teamSubtitle: "Mitglieder verwalten und Audit-Protokoll einsehen.",
    members: "Mitglieder", membersSub: "Nutzer dieses Arbeitsbereichs", roleCompliance: "Compliance-Beauftragte",
    roleDeveloper: "Entwickler", roleAuditor: "Auditor (nur Lesen)", roleAdmin: "Administrator",
    temporaryPassword: "Anfangspasswort", addMember: "Mitglied hinzufügen", auditLog: "Audit-Protokoll", deactivate: "Deaktivieren",
    inactive: "Inaktiv", active: "Aktiv", deactivateConfirm: "Dieses Konto deaktivieren und aktive Sitzungen beenden?",
    memberDeactivated: "Arbeitsbereich-Konto deaktiviert.",
    auditSub: "Letzte Sicherheitsereignisse des Arbeitsbereichs", signOut: "Abmelden", popupBlocked: "Erlauben Sie Pop-ups, um den Bericht in einem neuen Tab zu öffnen.", role_owner: "Eigentümer",
    role_admin: "Administrator", role_compliance_officer: "Compliance-Beauftragte", role_developer: "Entwickler", role_auditor: "Auditor",
    noMembers: "Keine Mitglieder gefunden.", noAuditEvents: "Keine Audit-Ereignisse.", memberAdded: "Mitglied hinzugefügt.",
    signedOut: "Abgemeldet.", passwordRequired: "Das Passwort muss mindestens 12 Zeichen enthalten.",
    privacyTitle: "Datenschutz standardmäßig", privacyBody: "Repository-Dateien werden lokal geprüft und nie an einen KI-Anbieter gesendet.", localMode: "LOKALER MODUS",
    demoWorkspace: "Demo-Arbeitsbereich", localPrototype: "Lokaler Prototyp", language: "Sprache", overviewEyebrow: "IHR COMPLIANCE-ARBEITSBEREICH",
    welcome: "Guten Morgen", welcomeSub: "Hier erhalten Sie einen klareren Überblick über Ihre KI-Governance.", startAssessment: "Prüfung starten",
    prototypeTitle: "Lokaler Prototyp · nicht produktionsreif", prototypeBody: "Nur lokaler Betrieb. Anmeldung ist aktiviert, aber unabhängig sicherheitsgeprüft wurde der Prototyp nicht. Keine vertraulichen oder echten personenbezogenen Daten hochladen.",
    totalScans: "Prüfungen insgesamt", allTime: "Gesamtzeitraum", openFindings: "Offene Hinweise", needReview: "Menschliche Prüfung erforderlich",
    reviewed: "Geprüft", humanValidated: "Menschlich validierte Hinweise", latestRisk: "Letzte Risikoprüfung", indicativeOnly: "Indikativ · keine Rechtsberatung",
    recentAssessments: "Letzte Prüfungen", recentSub: "Ihre neuesten Repository-Prüfungen", viewAll: "Alle anzeigen", noAssessments: "Noch keine Prüfungen",
    noAssessmentsSub: "Laden Sie ein ZIP-Archiv für Ihre erste Prüfung hoch.", startFirst: "Erste Prüfung starten",
    howItWorks: "So funktioniert es", methodSub: "Nachweise zuerst. Menschen entscheiden.", stepOne: "Verwendungszweck angeben",
    stepOneSub: "Das Risiko hängt von der Verwendung eines KI-Systems ab, nicht nur vom Code.", stepTwo: "Code lokal prüfen",
    stepTwoSub: "Regeln prüfen unterstützte Dateien auf diesem Gerät. Quellcode wird nicht gespeichert.", stepThree: "Jeden Hinweis prüfen",
    stepThreeSub: "Hinweise unterstützen menschliche Prüfung und sind keine automatisierten Rechtsurteile.",
    footerNotice: "ReguGuard ist ein Bereitschaftswerkzeug, keine Zertifizierung oder Rechtsberatung.",
    assessmentSetup: "PRÜFUNG EINRICHTEN", newAssessmentTitle: "Prüfung starten",
    newAssessmentSub: "Beschreiben Sie den Verwendungszweck und laden Sie anschließend ein Quellcode-Archiv hoch.",
    useCase: "Anwendungskontext", useCaseSub: "Eine Risikoprüfung braucht Kontext über den Code hinaus.", projectName: "Projektname",
    sector: "Sektor", selectSector: "Sektor auswählen", general: "Allgemeine Software", hr: "Personal & Beschäftigung",
    finance: "Finanzen & Kredit", education: "Bildung", healthcare: "Gesundheitswesen", public: "Öffentliche Dienste", other: "Andere / unbekannt",
    intendedUsers: "Vorgesehene Nutzer", usersPlaceholder: "z. B. Personalverantwortliche", projectPlaceholder: "z. B. Bewerber-Matching-Plattform",
    purpose: "Verwendungszweck", purposePlaceholder: "Beschreiben Sie Funktion, Nutzer und möglicherweise betroffene Personen.",
    consequentialTitle: "Kann das System Entscheidungen über Menschen wesentlich beeinflussen?",
    consequentialSub: "Zum Beispiel Zugang zu Arbeit, Bildung, Krediten, Gesundheits- oder öffentlichen Diensten.",
    repository: "Repository-Archiv", repositorySub: "Nur ZIP · Dateien werden lokal geprüft und niemals ausgeführt.",
    dropTitle: "ZIP-Archiv hier ablegen", dropSub: "oder Datei auswählen · maximal 25 MB",
    uploadFootnote: "Quelldateien bleiben während der Prüfung im Arbeitsspeicher und werden nicht gespeichert.",
    cancel: "Abbrechen", runAssessment: "Prüfung ausführen", scopeTitle: "Was wird geprüft",
    scopeOne: "Mögliche Zugangsdaten und offengelegte Geheimnisse", scopeTwo: "E-Mail-Adressen und IBAN-ähnliche Muster",
    scopeThree: "KI-Framework- und Dataset-Verweise", scopeFour: "Hinweise auf besondere Datenkategorien",
    scopeFive: "Vorhandensein grundlegender technischer Dokumentation", scopeLimitTitle: "Wichtige Einschränkung",
    scopeLimitBody: "Mustererkennung ist kein vollständiges Sicherheits- oder Datenschutzaudit. Probleme können übersehen oder fälschlich erkannt werden.",
    assessmentHistory: "PRÜFUNGSVERLAUF", allAssessments: "Prüfungen & Hinweise",
    allAssessmentsSub: "Ergebnisse ansehen und menschliche Prüfentscheidungen dokumentieren.", newAssessment: "Neue Prüfung",
    allScans: "Alle Prüfungen", allScansSub: "Neueste zuerst", searchProjects: "Projekte suchen...",
    project: "Projekt", date: "Datum", risk: "Risikoprüfung", findings: "Hinweise", status: "Status", actions: "Aktionen",
    completed: "Abgeschlossen", open: "Offen", approved: "Bestätigt", rejected: "Zurückgewiesen", queued: "In Warteschlange", failed: "Fehlgeschlagen",
    noSearchResults: "Keine passenden Prüfungen.", noFindings: "Keine Hinweise in den aktivierten Prüfungen.",
    indicativeRisk: "Indikative Risikoprüfung", purposeLabel: "Verwendungszweck", sectorLabel: "Sektor",
    sourceFiles: "Unterstützte Textdateien", report: "Bericht öffnen / drucken", deleteScan: "Prüfung löschen", backToScans: "Zurück zu Prüfungen",
    evidence: "Nachweis", legalReference: "Rechtsbezug zur menschlichen Prüfung", humanReview: "Menschliche Prüfung",
    saveReview: "Prüfung speichern", commentPlaceholder: "Optionale Prüfanmerkung", noComment: "Keine Anmerkung",
    unknownRisk: "Prüfung erforderlich", potential_high_risk: "Mögliche Hochrisikoanwendung", transparency_review: "Transparenzprüfung",
    no_high_risk_signal: "Kein Hochrisikosignal erkannt", needs_review: "Weitere Angaben erforderlich",
    secret: "Mögliches offengelegtes Geheimnis", personal_data: "Mögliche personenbezogene Daten",
    sensitive_data: "Mögliche sensible Daten", ai_dependency: "KI-Framework-Verweis", dataset_reference: "Dataset-Verweis",
    missing_docs: "Technische Dokumentation nicht gefunden",
    critical: "Kritisch", high: "Hoch", medium: "Mittel", low: "Niedrig",
    scanSuccess: "Prüfung abgeschlossen. Hinweise können jetzt menschlich geprüft werden.",
    scanFailed: "Die Prüfung konnte nicht abgeschlossen werden.", selectZip: "Wählen Sie zuerst ein ZIP-Archiv.",
    reportDownloaded: "Bericht bereit. SHA-256-Integritäts-Hash: ", deleteConfirm: "Diese Prüfung und alle Hinweise dauerhaft löschen?",
    scanDeleted: "Prüfung gelöscht.", reviewSaved: "Prüfentscheidung gespeichert.", loading: "Wird geladen…",
    noPurpose: "Kein Verwendungszweck angegeben.", requestError: "Anfrage fehlgeschlagen",
  },
  uz: {
    workspace: "ISH MAYDONI", overview: "Umumiy ko‘rinish", scans: "Skanlar va topilmalar", newScan: "Yangi baholash",
    secureWorkspace: "HIMOYALANGAN ISH MAYDONI", signIn: "Kirish", signInSub: "Muvofiqlik ish maydoningizga kiring.",
    workspaceName: "Ish maydoni nomi", emailAddress: "Email manzil", password: "Parol",
    passwordHint: "Kamida 12 ta belgi. Bu akkaunt ish maydoni egasi bo‘ladi.",
    createWorkspace: "Ish maydoni yaratish", authLocalOnly: "Akkauntlar faqat mahalliy prototip bazasida saqlanadi.",
    teamAudit: "Jamoa va audit", teamTitle: "Ish maydoni jamoasi", teamSubtitle: "A’zolarni boshqaring va audit jurnalini ko‘ring.",
    members: "A’zolar", membersSub: "Ushbu ish maydonidagi foydalanuvchilar", roleCompliance: "Muvofiqlik mutaxassisi",
    roleDeveloper: "Dasturchi", roleAuditor: "Auditor (faqat o‘qish)", roleAdmin: "Administrator",
    temporaryPassword: "Boshlang‘ich parol", addMember: "A’zo qo‘shish", auditLog: "Audit jurnali", deactivate: "Faolsizlantirish",
    inactive: "Faol emas", active: "Faol", deactivateConfirm: "Akkaunt faolsizlantirilib, ochiq sessiyalar tugatilsinmi?",
    memberDeactivated: "Ish maydoni akkaunti faolsizlantirildi.",
    auditSub: "Ish maydonidagi so‘nggi xavfsizlik hodisalari", signOut: "Chiqish", popupBlocked: "Hisobot yangi oynada ochilishi uchun qalqib chiquvchi oynalarga ruxsat bering.", role_owner: "Egasi",
    role_admin: "Administrator", role_compliance_officer: "Muvofiqlik mutaxassisi", role_developer: "Dasturchi", role_auditor: "Auditor",
    noMembers: "A’zolar topilmadi.", noAuditEvents: "Audit hodisalari yo‘q.", memberAdded: "A’zo qo‘shildi.",
    signedOut: "Tizimdan chiqildi.", passwordRequired: "Parol kamida 12 ta belgidan iborat bo‘lishi kerak.",
    privacyTitle: "Maxfiylik birinchi o‘rinda", privacyBody: "Repo fayllari mahalliy tekshiriladi va AI provayderiga yuborilmaydi.", localMode: "MAHALLIY REJIM",
    demoWorkspace: "Demo ish maydoni", localPrototype: "Mahalliy prototip", language: "Til", overviewEyebrow: "MUVOFIQLIK ISH MAYDONINGIZ",
    welcome: "Xush kelibsiz", welcomeSub: "AI boshqaruvi holatini aniqroq ko‘rish shu yerdan boshlanadi.", startAssessment: "Baholashni boshlash",
    prototypeTitle: "Mahalliy prototip · production uchun tayyor emas", prototypeBody: "Faqat mahalliy ishga tushirish uchun. Kirish himoyasi bor, ammo mustaqil xavfsizlik auditi yo‘q. Maxfiy yoki haqiqiy shaxsiy ma’lumot yuklamang.",
    totalScans: "Jami baholashlar", allTime: "Barcha vaqt", openFindings: "Ochiq topilmalar", needReview: "Inson tekshiruvi kerak",
    reviewed: "Ko‘rib chiqilgan", humanValidated: "Inson tasdiqlagan topilmalar", latestRisk: "So‘nggi xavf skriningi", indicativeOnly: "Dastlabki · yuridik maslahat emas",
    recentAssessments: "So‘nggi baholashlar", recentSub: "Repo bo‘yicha oxirgi tekshiruvlar", viewAll: "Barchasini ko‘rish", noAssessments: "Hali baholash yo‘q",
    noAssessmentsSub: "Birinchi tekshiruv uchun ZIP arxiv yuklang.", startFirst: "Birinchi skanni boshlash",
    howItWorks: "Qanday ishlaydi", methodSub: "Avval dalil. Qaror insonda.", stepOne: "Foydalanish maqsadini kiriting",
    stepOneSub: "Xavf tizim kodiga emas, undan qanday foydalanilishiga bog‘liq.", stepTwo: "Kodni mahalliy skan qiling",
    stepTwoSub: "Qoidalar fayllarni shu qurilmada tekshiradi. Manba kod saqlanmaydi.", stepThree: "Har bir signalni ko‘rib chiqing",
    stepThreeSub: "Topilmalar inson tekshiruvi uchun signal, avtomatik yuridik xulosa emas.",
    footerNotice: "ReguGuard — tayyorgarlik vositasi, sertifikat yoki yuridik xizmat emas.",
    assessmentSetup: "BAHOLASHNI SOZLASH", newAssessmentTitle: "Baholashni boshlash",
    newAssessmentSub: "Tizim qanday ishlatilishini yozing, so‘ng manba arxivini yuklang.",
    useCase: "Foydalanish konteksti", useCaseSub: "Xavfni baholash uchun koddan tashqari kontekst ham kerak.", projectName: "Loyiha nomi",
    sector: "Soha", selectSector: "Sohani tanlang", general: "Umumiy dasturiy ta’minot", hr: "HR va ishga qabul",
    finance: "Moliya va kredit", education: "Ta’lim", healthcare: "Sog‘liqni saqlash", public: "Davlat xizmatlari", other: "Boshqa / noma’lum",
    intendedUsers: "Foydalanuvchilar", usersPlaceholder: "masalan, HR va ishga qabul jamoasi", projectPlaceholder: "masalan, nomzodlarni saralash tizimi",
    purpose: "Foydalanish maqsadi", purposePlaceholder: "Tizim vazifasi, undan kim foydalanishi va kimga ta’sir qilishini yozing.",
    consequentialTitle: "Tizim odamlar haqidagi muhim qarorlarga ta’sir qiladimi?",
    consequentialSub: "Masalan, ish, ta’lim, kredit, tibbiyot yoki davlat xizmatlaridan foydalanish.",
    repository: "Repo arxivi", repositorySub: "Faqat ZIP · fayllar mahalliy tekshiriladi va ishga tushirilmaydi.",
    dropTitle: "ZIP arxivni shu yerga tashlang", dropSub: "yoki fayl tanlang · eng ko‘pi 25 MB",
    uploadFootnote: "Manba fayllari skan paytida xotirada bo‘ladi va diskka saqlanmaydi.",
    cancel: "Bekor qilish", runAssessment: "Baholashni boshlash", scopeTitle: "Skan nimalarni tekshiradi",
    scopeOne: "Ochiq qolgan maxfiy kalitlar", scopeTwo: "Email va IBANga o‘xshash naqshlar",
    scopeThree: "AI freymvorki va dataset havolalari", scopeFour: "Maxsus toifadagi ma’lumot belgilari",
    scopeFive: "Texnik hujjatlar mavjudligi", scopeLimitTitle: "Muhim cheklov",
    scopeLimitBody: "Naqshlarni topish to‘liq xavfsizlik yoki maxfiylik auditi emas. Muammolar qolib ketishi yoki noto‘g‘ri signal berishi mumkin.",
    assessmentHistory: "BAHOLASH TARIXI", allAssessments: "Skanlar va topilmalar",
    allAssessmentsSub: "Natijalarni ko‘ring va inson tekshiruvini qayd qiling.", newAssessment: "Yangi baholash",
    allScans: "Barcha baholashlar", allScansSub: "Avval eng yangilari", searchProjects: "Loyihalarni qidirish...",
    project: "Loyiha", date: "Sana", risk: "Xavf skriningi", findings: "Topilmalar", status: "Holat", actions: "Amallar",
    completed: "Tugallandi", open: "Ochiq", approved: "Tasdiqlandi", rejected: "Rad etildi", queued: "Navbatda", failed: "Xatolik",
    noSearchResults: "Mos baholash topilmadi.", noFindings: "Yoqilgan tekshiruvlarda topilma yo‘q.",
    indicativeRisk: "Dastlabki xavf skriningi", purposeLabel: "Foydalanish maqsadi", sectorLabel: "Soha",
    sourceFiles: "Qo‘llab-quvvatlanadigan matn fayllari", report: "Hisobotni ochish / chop etish", deleteScan: "Baholashni o‘chirish", backToScans: "Baholashlarga qaytish",
    evidence: "Dalil", legalReference: "Inson ko‘rigi uchun huquqiy havola", humanReview: "Inson tekshiruvi",
    saveReview: "Tekshiruvni saqlash", commentPlaceholder: "Ixtiyoriy izoh", noComment: "Izoh yo‘q",
    unknownRisk: "Qo‘shimcha tekshiruv kerak", potential_high_risk: "Yuqori ta’sir ehtimoli", transparency_review: "Shaffoflik tekshiruvi",
    no_high_risk_signal: "Yuqori xavf belgisi topilmadi", needs_review: "Kontekst yetarli emas",
    secret: "Ochiq maxfiy kalit ehtimoli", personal_data: "Shaxsiy ma’lumot ehtimoli",
    sensitive_data: "Maxsus ma’lumot ehtimoli", ai_dependency: "AI freymvorki havolasi", dataset_reference: "Dataset havolasi",
    missing_docs: "Texnik hujjat topilmadi",
    critical: "Kritik", high: "Yuqori", medium: "O‘rta", low: "Past",
    scanSuccess: "Baholash tugadi. Topilmalarni inson ko‘rib chiqishi mumkin.",
    scanFailed: "Baholashni yakunlab bo‘lmadi.", selectZip: "Avval ZIP arxiv tanlang.",
    reportDownloaded: "Hisobot tayyor. SHA-256 yaxlitlik xeshi: ", deleteConfirm: "Ushbu baholash va topilmalar butunlay o‘chirilsinmi?",
    scanDeleted: "Baholash o‘chirildi.", reviewSaved: "Tekshiruv qarori saqlandi.", loading: "Yuklanmoqda…",
    noPurpose: "Foydalanish maqsadi kiritilmagan.", requestError: "So‘rov bajarilmadi",
  },
};

const SECTOR_KEYS = {
  general: "general", hr: "hr", finance: "finance", education: "education",
  healthcare: "healthcare", public: "public", other: "other",
};
const storedLanguage = localStorage.getItem("reguguard-language");
let language = ["en", "de", "uz"].includes(storedLanguage) ? storedLanguage : "en";
let scansCache = [];
let currentScanId = null;
let csrfToken = "";
let currentUser = null;
let authSetupRequired = false;

const t = (key) => I18N[language][key] || I18N.en[key] || key;
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[char]));
const localDate = (date) => {
  try { return new Intl.DateTimeFormat(language === "de" ? "de-DE" : language === "uz" ? "uz-UZ" : "en-GB", { dateStyle: "medium", timeStyle: "short" }).format(new Date(date)); }
  catch { return date; }
};

function showNotice(message, type = "error") {
  const notice = document.querySelector("#notice");
  notice.className = `notice ${type === "info" ? "notice-info" : ""}`;
  notice.textContent = message;
  notice.hidden = false;
  window.clearTimeout(showNotice.timer);
  showNotice.timer = window.setTimeout(() => { notice.hidden = true; }, 7000);
}

function applyLanguage() {
  document.documentElement.lang = language;
  document.querySelector("#language").value = language;
  document.querySelector("#language").setAttribute("aria-label", t("language"));
  document.querySelector("#auth-language").value = language;
  document.querySelector("#auth-language").setAttribute("aria-label", t("language"));
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const key = element.dataset.i18n;
    if (I18N[language][key]) element.textContent = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("#sector option").forEach((option) => {
    if (option.dataset.i18n) option.textContent = t(option.dataset.i18n);
  });
  document.querySelector("#breadcrumb-current").textContent = t("overview");
  if (!currentUser) {
    document.querySelector("#auth-title").textContent = t(authSetupRequired ? "createWorkspace" : "signIn");
    document.querySelector("#auth-subtitle").textContent = t(authSetupRequired ? "passwordHint" : "signInSub");
  }
  if (currentUser) document.querySelector("#profile-role").textContent = t(`role_${currentUser.role}`);
  renderMetrics();
  renderRecent();
  renderTable(document.querySelector("#scan-filter").value);
  if (currentScanId) openScan(currentScanId, false);
}

function showView(name) {
  document.querySelectorAll(".view").forEach((view) => { view.hidden = view.id !== `view-${name}`; });
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === name));
  const breadcrumbKeys = { overview: "overview", scans: "scans", "new-scan": "newScan", team: "teamAudit" };
  document.querySelector("#breadcrumb-current").textContent = t(breadcrumbKeys[name] || "overview");
  if (name === "scans") refreshScans();
  if (name === "team") refreshTeam();
}

function statusPill(status, className = "review-tag") {
  const key = status === "completed" ? "completed" : status;
  return `<span class="${className} ${escapeHtml(status)}">${escapeHtml(t(key))}</span>`;
}

function renderMetrics() {
  document.querySelector("#metric-scans").textContent = scansCache.length;
  const openCount = scansCache.reduce((total, scan) => total + Number(scan.open_count || 0), 0);
  const reviewedCount = scansCache.reduce((total, scan) => total + Number(scan.reviewed_count || 0), 0);
  document.querySelector("#metric-open").textContent = openCount;
  document.querySelector("#metric-reviewed").textContent = reviewedCount;
  document.querySelector("#metric-risk").textContent = scansCache.length ? t(scansCache[0].risk_category) : "—";
  document.querySelector("#nav-scan-count").textContent = scansCache.length;
}

function renderRecent() {
  const target = document.querySelector("#recent-scans");
  if (!scansCache.length) {
    target.innerHTML = `<div class="empty-state"><div class="empty-symbol">◈</div><strong>${escapeHtml(t("noAssessments"))}</strong><p>${escapeHtml(t("noAssessmentsSub"))}</p><button class="button button-secondary" data-action="new-scan">${escapeHtml(t("startFirst"))}</button></div>`;
    return;
  }
  target.innerHTML = scansCache.slice(0, 5).map((scan) => `
    <div class="scan-row" role="button" tabindex="0" data-open-scan="${escapeHtml(scan.id)}">
      <span class="scan-glyph">◈</span><span class="scan-copy"><strong>${escapeHtml(scan.project_name)}</strong><small>${escapeHtml(localDate(scan.created_at))} · ${Number(scan.finding_count)} ${escapeHtml(t("findings").toLowerCase())}</small></span>
      ${statusPill(scan.risk_category, "risk-tag")}
    </div>`).join("");
}

function renderTable(filter = "") {
  const target = document.querySelector("#scan-table");
  if (!scansCache.length) {
    target.innerHTML = `<div class="table-empty">${escapeHtml(t("noAssessments"))}</div>`;
    return;
  }
  const normalized = filter.trim().toLocaleLowerCase();
  const rows = scansCache.filter((scan) => scan.project_name.toLocaleLowerCase().includes(normalized));
  if (!rows.length) {
    target.innerHTML = `<div class="table-empty">${escapeHtml(t("noSearchResults"))}</div>`;
    return;
  }
  target.innerHTML = `<table><thead><tr><th>${escapeHtml(t("project"))}</th><th>${escapeHtml(t("date"))}</th><th>${escapeHtml(t("risk"))}</th><th>${escapeHtml(t("findings"))}</th><th>${escapeHtml(t("status"))}</th></tr></thead><tbody>${rows.map((scan) => `
    <tr data-open-scan="${escapeHtml(scan.id)}" tabindex="0"><td><strong>${escapeHtml(scan.project_name)}</strong></td><td>${escapeHtml(localDate(scan.created_at))}</td><td>${statusPill(scan.risk_category, "risk-tag")}</td><td>${Number(scan.finding_count)}</td><td>${statusPill(scan.status)}</td></tr>`).join("")}</tbody></table>`;
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (["POST", "PATCH", "DELETE", "PUT"].includes((options.method || "GET").toUpperCase()) && csrfToken) {
    headers.set("X-CSRF-Token", csrfToken);
  }
  const response = await fetch(path, { ...options, headers, credentials: "same-origin" });
  if (!response.ok) {
    let message = `${t("requestError")} (${response.status})`;
    try { message = (await response.json()).error || message; } catch { /* Response may not be JSON. */ }
    throw new Error(message);
  }
  return response;
}

async function refreshScans() {
  try {
    const response = await request("/api/scans");
    scansCache = (await response.json()).scans;
    renderMetrics();
    renderRecent();
    renderTable(document.querySelector("#scan-filter").value);
  } catch (error) {
    showNotice(error.message);
  }
}

async function loadAuthState() {
    try {
      const response = await request("/api/auth/state");
      const state = await response.json();
      authSetupRequired = state.setup_required;
      currentUser = state.user;
      csrfToken = state.csrf_token || "";
      document.querySelector("#setup-form").hidden = !authSetupRequired;
      document.querySelector("#login-form").hidden = authSetupRequired;
      document.querySelector("#auth-screen").hidden = Boolean(currentUser);
      document.querySelector(".app-shell").hidden = !currentUser;
      document.querySelector("#auth-error").hidden = true;
      if (currentUser) {
        document.querySelector("#signed-in-email").textContent = currentUser.email;
        document.querySelector("#profile-name").textContent = currentUser.tenant_name;
        document.querySelector("#profile-role").textContent = t(`role_${currentUser.role}`);
        document.querySelector("#profile-avatar").textContent = currentUser.tenant_name.slice(0, 1).toUpperCase();
        const canManageTeam = ["owner", "admin"].includes(currentUser.role);
        const canScan = ["owner", "admin", "compliance_officer", "developer"].includes(currentUser.role);
        document.querySelector("#team-nav").hidden = !canManageTeam;
        document.querySelector("#invite-form").hidden = !canManageTeam;
        document.querySelector("#invite-admin-role").hidden = currentUser.role !== "owner";
        document.querySelectorAll('[data-action="new-scan"], .nav-item[data-view="new-scan"]').forEach((element) => {
          element.hidden = !canScan;
        });
        await refreshScans();
        applyLanguage();
      } else {
        applyLanguage();
      }
    } catch (error) {
      document.querySelector("#auth-screen").hidden = false;
      document.querySelector("#app-shell")?.setAttribute("hidden", "");
      showAuthError(error.message);
    }
  }

function showAuthError(message) {
    const box = document.querySelector("#auth-error");
    box.textContent = message;
    box.hidden = false;
  }

async function submitAuthForm(form, path) {
    const payload = Object.fromEntries(new FormData(form).entries());
    try {
      const response = await request(path, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
      });
      const result = await response.json();
      csrfToken = result.csrf_token;
      await loadAuthState();
    } catch (error) {
      showAuthError(error.message);
    }
  }

async function refreshTeam() {
    if (!currentUser) return;
    try {
      const membersResponse = await request("/api/team");
      const members = (await membersResponse.json()).members;
      document.querySelector("#team-list").innerHTML = members.length
        ? `<table><thead><tr><th>${escapeHtml(t("emailAddress"))}</th><th>${escapeHtml(t("status"))}</th><th>${escapeHtml(t("actions"))}</th></tr></thead><tbody>${members.map((member) => `<tr><td>${escapeHtml(member.email)}</td><td>${escapeHtml(t(`role_${member.role}`))} · ${escapeHtml(t(member.active ? "active" : "inactive"))}</td><td>${member.active && member.role !== "owner" && member.id !== currentUser.id ? `<button class="text-button" data-deactivate-user="${escapeHtml(member.id)}">${escapeHtml(t("deactivate"))}</button>` : ""}</td></tr>`).join("")}</tbody></table>`
        : `<div class="table-empty">${escapeHtml(t("noMembers"))}</div>`;
    } catch (error) {
      document.querySelector("#team-list").innerHTML = `<div class="table-empty">${escapeHtml(error.message)}</div>`;
    }
    try {
      const auditResponse = await request("/api/audit");
      const events = (await auditResponse.json()).events;
      document.querySelector("#audit-list").innerHTML = events.length
        ? `<table><thead><tr><th>${escapeHtml(t("actions"))}</th><th>${escapeHtml(t("emailAddress"))}</th><th>${escapeHtml(t("date"))}</th></tr></thead><tbody>${events.map((event) => `<tr><td>${escapeHtml(event.action)}</td><td>${escapeHtml(event.actor_email)}</td><td>${escapeHtml(localDate(event.created_at))}</td></tr>`).join("")}</tbody></table>`
        : `<div class="table-empty">${escapeHtml(t("noAuditEvents"))}</div>`;
    } catch (error) {
      document.querySelector("#audit-list").innerHTML = `<div class="table-empty">${escapeHtml(error.message)}</div>`;
    }
  }

async function addTeamMember(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = Object.fromEntries(new FormData(form).entries());
    try {
      await request("/api/team", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
      });
      form.reset();
      await refreshTeam();
      showNotice(t("memberAdded"), "info");
    } catch (error) { showNotice(error.message); }
  }

  async function deactivateMember(id) {
    if (!window.confirm(t("deactivateConfirm"))) return;
    try {
      await request(`/api/team/${encodeURIComponent(id)}`, { method: "DELETE" });
      await refreshTeam();
      showNotice(t("memberDeactivated"), "info");
    } catch (error) { showNotice(error.message); }
  }

async function signOut() {
    try {
      await request("/api/auth/logout", { method: "POST" });
      csrfToken = "";
      currentUser = null;
      scansCache = [];
      await loadAuthState();
    } catch (error) { showNotice(error.message); }
}

async function openScan(id, reveal = true) {
  try {
    const response = await request(`/api/scans/${encodeURIComponent(id)}`);
    const { scan, findings } = await response.json();
    currentScanId = id;
    const target = document.querySelector("#scan-detail");
    target.hidden = false;
    const canReview = ["owner", "admin", "compliance_officer"].includes(currentUser?.role);
    const canDelete = ["owner", "admin", "compliance_officer"].includes(currentUser?.role);
    const findingsMarkup = findings.length ? findings.map((finding) => `
      <article class="finding-card">
        <div class="finding-head"><h3>${escapeHtml(t(finding.rule_key))}</h3>${statusPill(finding.severity, "severity-tag")}${statusPill(finding.review_status)}</div>
        <p><strong>${escapeHtml(finding.file_path)}:${Number(finding.line_number)}</strong></p>
        <pre>${escapeHtml(finding.evidence)}</pre>
        <p><strong>${escapeHtml(t("legalReference"))}:</strong> ${escapeHtml(finding.regulation)}</p>
        ${canReview ? `<div class="finding-review"><label class="sr-only" for="status-${escapeHtml(finding.id)}">${escapeHtml(t("humanReview"))}</label>
          <select id="status-${escapeHtml(finding.id)}"><option value="open" ${finding.review_status === "open" ? "selected" : ""}>${escapeHtml(t("open"))}</option><option value="approved" ${finding.review_status === "approved" ? "selected" : ""}>${escapeHtml(t("approved"))}</option><option value="rejected" ${finding.review_status === "rejected" ? "selected" : ""}>${escapeHtml(t("rejected"))}</option></select>
          <input id="comment-${escapeHtml(finding.id)}" aria-label="${escapeHtml(t("commentPlaceholder"))}" placeholder="${escapeHtml(t("commentPlaceholder"))}" value="${escapeHtml(finding.comment)}">
          <button class="button button-secondary" data-save-finding="${escapeHtml(finding.id)}">${escapeHtml(t("saveReview"))}</button></div>` : ""}
      </article>`).join("") : `<div class="table-empty">${escapeHtml(t("noFindings"))}</div>`;
    const deleteAction = canDelete ? `<button class="button button-secondary" data-delete-scan="${escapeHtml(scan.id)}">${escapeHtml(t("deleteScan"))}</button>` : "";
    target.innerHTML = `<div class="detail-header"><div><h2>${escapeHtml(scan.project_name)}</h2><p>${escapeHtml(localDate(scan.created_at))} · ${Number(scan.file_count)} ${escapeHtml(t("sourceFiles"))}</p></div><div class="detail-actions"><button class="button button-secondary" data-report="${escapeHtml(scan.id)}">${escapeHtml(t("report"))}</button>${deleteAction}<button class="button button-secondary" data-action="show-scans">${escapeHtml(t("backToScans"))}</button></div></div>
      <div class="risk-summary"><strong>${escapeHtml(t("indicativeRisk"))}:</strong> ${escapeHtml(t(scan.risk_category))}<br><strong>${escapeHtml(t("purposeLabel"))}:</strong> ${escapeHtml(scan.purpose || t("noPurpose"))}<br><strong>${escapeHtml(t("sectorLabel"))}:</strong> ${escapeHtml(SECTOR_KEYS[scan.sector] ? t(SECTOR_KEYS[scan.sector]) : scan.sector)}</div>
      <h2>${escapeHtml(t("findings"))} <span class="nav-count">${findings.length}</span></h2>${findingsMarkup}`;
    if (reveal) {
      showView("scans");
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    await refreshScans();
  } catch (error) {
    showNotice(error.message);
  }
}

async function createScan(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const file = form.elements.file.files[0];
  if (!file) return showNotice(t("selectZip"));
  const button = document.querySelector("#submit-scan");
  button.disabled = true;
  const label = button.querySelector("[data-i18n]");
  label.textContent = t("loading");
  try {
    const formData = new FormData(form);
    const response = await request("/api/scans", { method: "POST", body: formData });
    const result = await response.json();
    form.reset();
    document.querySelector("#file-name").textContent = "";
    await refreshScans();
    currentScanId = result.scan_id;
    await openScan(result.scan_id);
    showNotice(t("scanSuccess"), "info");
  } catch (error) {
    showNotice(`${t("scanFailed")} ${error.message}`);
  } finally {
    button.disabled = false;
    label.textContent = t("runAssessment");
  }
}

async function saveFinding(id) {
  const status = document.querySelector(`#status-${CSS.escape(id)}`).value;
  const comment = document.querySelector(`#comment-${CSS.escape(id)}`).value;
  try {
    await request(`/api/findings/${encodeURIComponent(id)}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status, comment }),
    });
    await openScan(currentScanId, false);
    showNotice(t("reviewSaved"), "info");
  } catch (error) { showNotice(error.message); }
}

async function downloadReport(id) {
  const url = `/api/scans/${encodeURIComponent(id)}/report?lang=${language}`;
  const reportWindow = window.open("about:blank", "_blank");
  if (!reportWindow) {
    showNotice(t("popupBlocked"));
    return;
  }
  try {
    const response = await request(`${url}&metadata=1`);
    const metadata = await response.json();
    reportWindow.location.href = url;
    showNotice(`${t("reportDownloaded")}${metadata.sha256}`, "info");
  } catch (error) {
    reportWindow.close();
    showNotice(error.message);
  }
}

async function deleteScan(id) {
  if (!window.confirm(t("deleteConfirm"))) return;
  try {
    await request(`/api/scans/${encodeURIComponent(id)}`, { method: "DELETE" });
    currentScanId = null;
    document.querySelector("#scan-detail").hidden = true;
    await refreshScans();
    showNotice(t("scanDeleted"), "info");
  } catch (error) { showNotice(error.message); }
}

document.addEventListener("click", (event) => {
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action === "new-scan") showView("new-scan");
  if (action === "overview") showView("overview");
  if (action === "show-scans") showView("scans");
  const scanRow = event.target.closest("[data-open-scan]");
  if (scanRow) openScan(scanRow.dataset.openScan);
  const saveButton = event.target.closest("[data-save-finding]");
  if (saveButton) saveFinding(saveButton.dataset.saveFinding);
  const reportButton = event.target.closest("[data-report]");
  if (reportButton) downloadReport(reportButton.dataset.report);
  const deleteButton = event.target.closest("[data-delete-scan]");
  if (deleteButton) deleteScan(deleteButton.dataset.deleteScan);
  const deactivateButton = event.target.closest("[data-deactivate-user]");
  if (deactivateButton) deactivateMember(deactivateButton.dataset.deactivateUser);
});

document.addEventListener("keydown", (event) => {
  if ((event.key === "Enter" || event.key === " ") && event.target.matches("[data-open-scan]")) {
    event.preventDefault();
    openScan(event.target.dataset.openScan);
  }
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => showView(button.dataset.view));
});
document.querySelector("#language").addEventListener("change", (event) => {
  language = event.target.value;
  localStorage.setItem("reguguard-language", language);
  applyLanguage();
});
document.querySelector("#auth-language").addEventListener("change", (event) => {
  language = event.target.value;
  localStorage.setItem("reguguard-language", language);
  applyLanguage();
});
document.querySelector("#scan-form").addEventListener("submit", createScan);
document.querySelector("#setup-form").addEventListener("submit", (event) => {
  event.preventDefault();
  submitAuthForm(event.currentTarget, "/api/auth/setup");
});
document.querySelector("#login-form").addEventListener("submit", (event) => {
  event.preventDefault();
  submitAuthForm(event.currentTarget, "/api/auth/login");
});
document.querySelector("#invite-form").addEventListener("submit", addTeamMember);
document.querySelector("#sign-out").addEventListener("click", signOut);
document.querySelector("#scan-filter").addEventListener("input", (event) => renderTable(event.target.value));
document.querySelector("#archive").addEventListener("change", (event) => {
  const file = event.target.files[0];
  document.querySelector("#file-name").textContent = file ? file.name : "";
});
const dropZone = document.querySelector("#drop-zone");
dropZone.addEventListener("dragover", (event) => { event.preventDefault(); dropZone.classList.add("dragging"); });
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragging"));
dropZone.addEventListener("drop", (event) => {
  event.preventDefault();
  dropZone.classList.remove("dragging");
  const file = event.dataTransfer.files[0];
  if (!file || !file.name.toLowerCase().endsWith(".zip")) return showNotice(t("selectZip"));
  const transfer = new DataTransfer();
  transfer.items.add(file);
  document.querySelector("#archive").files = transfer.files;
  document.querySelector("#file-name").textContent = file.name;
});

document.querySelector("#app-shell")?.removeAttribute("id");
applyLanguage();
loadAuthState();
