"""Generate expanded labeled training text for document classification."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "training_data.csv"

RESUME = [
    "curriculum vitae professional summary work experience education skills certifications",
    "objective seeking full time role software engineer python django flask rest api",
    "employment history company title dates responsibilities achievements metrics increased revenue",
    "technical skills programming languages frameworks databases cloud aws azure gcp",
    "projects portfolio github gitlab deployed application users open source contributor",
    "references available upon request contact phone email linkedin profile url",
    "internship experience summer analyst research assistant teaching assistant gpa honors",
    "volunteer leadership club president hackathon mentor coding bootcamp instructor",
    "languages spoken english spanish mandarin proficiency native fluent conversational",
    "certifications aws solutions architect pmp scrum master cisco ccna comptia security plus",
]

INVOICE = [
    "invoice number date due amount bill to ship to payment terms net thirty",
    "line item description quantity unit price extended total subtotal tax vat gst",
    "remit payment to bank account routing ach wire swift iban reference number",
    "purchase order number customer id account balance statement amount due usd eur",
    "credit memo debit note adjustment refund partial payment applied invoices",
    "shipping handling freight customs duty incoterms fob cif destination origin",
    "subscription billing period recurring charge prorate upgrade license seats",
    "vendor supplier remittance advice check number deposit applied receivables",
    "utility meter reading consumption kwh therms service address billing cycle",
    "medical bill cpt code copay deductible insurance claim patient responsibility",
]

RESEARCH = [
    "abstract introduction methods results discussion conclusion keywords doi arxiv",
    "peer reviewed journal manuscript submitted revised accepted publication citation",
    "experiment hypothesis dataset baseline model accuracy f1 auc precision recall",
    "statistical analysis p value confidence interval significance test anova regression",
    "systematic review meta analysis prisma inclusion exclusion forest plot",
    "figure table supplementary material appendix reproducibility code data availability",
    "grant acknowledgment funding agency ethics irb consent conflict interest",
    "related work prior art state of the art comparison ablation hyperparameters",
    "neural network transformer bert lstm cnn training validation test split",
    "theorem proof lemma mathematical model simulation parameter sensitivity analysis",
]

LEGAL = [
    "agreement parties whereas therefore witnesseth executed effective date governing law",
    "plaintiff defendant complaint answer discovery motion hearing court jurisdiction venue",
    "lease landlord tenant rent deposit term renewal termination notice default",
    "non disclosure confidential proprietary information term survival injunctive relief",
    "terms of service privacy policy arbitration limitation liability indemnification",
    "will testament executor beneficiary estate probate codicil residuary clause",
    "power of attorney agent principal durable healthcare financial notarized",
    "settlement release claims consideration mutual confidentiality non disparagement",
    "article section clause amendment severability entire agreement assignment consent",
    "intellectual property license sublicense royalty termination breach cure notice",
]

EXTRA = {
    "Resume": [
        "managed team of engineers roadmap sprint planning code review hiring interviews",
        "bachelor master phd degree university college graduation year dean list scholarship",
        "sales quota exceeded crm pipeline negotiation client retention account management",
        "nurse rn licensure clinical rotations patient care ehr epic cerner hospital",
        "graphic designer adobe creative suite branding typography layout print digital",
    ],
    "Invoice": [
        "proforma commercial export packing list weight dimensions harmonized tariff code",
        "restaurant tab gratuity suggested tip split check table server pos terminal",
        "construction progress billing milestone retainage lien waiver subcontractor",
        "saas annual contract true up overage metered api calls invoice reconciliation",
        "hotel folio room charge minibar tax resort fee checkout express",
    ],
    "Research Paper": [
        "randomized double blind placebo controlled crossover factorial design power analysis",
        "qualitative interviews thematic coding grounded theory saturation member checking",
        "protein expression western blot pcr sequencing genome transcriptome proteomics",
        "finite element structural load simulation mesh boundary conditions convergence",
        "survey likert scale reliability cronbach alpha factor analysis structural equation",
    ],
    "Legal Document": [
        "stock purchase merger acquisition due diligence representations warranties escrow",
        "employment offer at will compensation benefits non compete restrictive covenant",
        "trademark assignment recordation uspto specimen use commerce priority date",
        "subpoena deposition exhibit marked confidential attorney client privilege work product",
        "zoning variance hearing minutes resolution ordinance municipal code compliance",
    ],
}


def rows():
    base = [
        (RESUME, "Resume"),
        (INVOICE, "Invoice"),
        (RESEARCH, "Research Paper"),
        (LEGAL, "Legal Document"),
    ]
    for templates, label in base:
        for t in templates:
            yield t, label
            yield t + " " + t, label
            yield " ".join(reversed(t.split())), label
        for t in EXTRA[label]:
            yield t, label
            for i in range(3):
                yield f"{t} document section paragraph {i} details context", label


def main():
    seen = set()
    data = []
    for text, label in rows():
        key = (text[:80], label)
        if key not in seen:
            seen.add(key)
            data.append({"text": text, "label": label})

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["text", "label"])
        w.writeheader()
        w.writerows(data)

    print(f"Wrote {len(data)} samples to {OUT}")


if __name__ == "__main__":
    main()
