# TracyAI

## Tracy – Pravni AI asistent

**"No trace, no case" - ekipa RegulaTOS**

Tracy je pravni raziskovalni pomočnik, zasnovan za študente prava, pravne strokovnjake, raziskovalce, pa tudi potrošnike in uporabnike digitalnih storitev. Združuje **pravno raziskovanje sodnih primerov** in **analizo pogojev uporabe (TOS)**, da pomaga razumeti in zaščititi pravice uporabnikov.

Umetna inteligenca v pravu ne sme delovati kot "črna skrinjica" (**blackbox**). S Tracy gradimo **sledljiv in transparenten AI**, kjer so vsi koraki raziskave in odločanja jasno vidni. To pomeni večjo zanesljivost, zmanjšanje napačnih interpretacij in boljše razumevanje pravnih tveganj.

---

## Ključne funkcionalnosti  

- **Iskanje sodnih primerov** – Tracy uporablja **CourtListener API** za iskanje relevantnih sodnih odločb v ZDA.  
- **Preverjanje citatov** – Preverja pravni status in precedenčno vrednost sodnih primerov.  
- **Analiza pogojev uporabe** – Z lastnim API-jem Tracy pridobi in analizira **TOS podjetij** ter identificira **sive cone in zlonamerne pravne določbe**.  
- **Prijazen uporabniški vmesnik** – Gradio UI omogoča intuitivno interakcijo s sistemom.  
- **Sledljivost in transparentnost** – Vsak pravni rezultat je utemeljen s preverljivimi viri.  

Tracy je zasnovana kot orodje ne samo za **pravne strokovnjake**, temveč tudi za **potrošnike in uporabnike digitalnih storitev**, ki želijo **razumeti in zaščititi svoje pravice**. Z analizo **pogodb in pogojev uporabe** Tracy pomaga prepoznati **skrite pasti**, ki jih pogosto vsebujejo pravni dokumenti spletnih platform.

---

## Kako Tracy združuje pravno raziskovanje in zaščito uporabnikov

Tracy temelji na dveh ključnih podatkovnih virih:

1. **CourtListener API** – Dostopa do javno dostopnih sodnih odločb v ZDA, kar omogoča **pravnim strokovnjakom in raziskovalcem** iskanje primerov, preverjanje citatov in analizo pravne prakse.  
2. **Naš API za analizo pogojev uporabe** – Uporablja podatkovno infrastrukturo **[Digital Services Terms and Conditions Database](https://platform-contracts.digital-strategy.ec.europa.eu/)** Evropske komisije, s katero pridobiva in analizira **pogoje uporabe podjetij**. To omogoča uporabnikom, da **prepoznajo potencialno škodljive določbe** in se izognejo tveganjem.  

Pogoji uporabe (TOS) pogosto vsebujejo **zapletene pravne formulacije**, ki jih povprečen uporabnik težko razume. Tracy pomaga razčleniti te dokumente in poudariti **nepoštene ali zavajajoče klavzule**, s čimer uporabnikom omogoča boljšo zaščito njihovih pravic.

---

## Struktura projekta  

```
- tools/                 # Dodatna, neintegrirana orodja  
- Gradio_UI/             # Uporabniški vmesnik, zgrajen z Gradio (Hugging Face)  
- agent.json             # Metapodatki in konfiguracije agenta  
- app.py                 # Glavna skripta aplikacije  
- prompts.yaml           # Predloge pozivov za AI model  
```

---

## Pregled funkcionalnosti (`app.py`)  

- **`search_court_cases()`** – Poišče pravne primere glede na uporabniške parametre.  
- **`check_citation_status()`** – Preveri precedenčno vrednost in status sodnega primera.  
- **`extract_tos_content(company_name)`** – Pridobi pogoje uporabe podjetja prek našega API-ja.  
- **`search_terms_of_service(company_name)`** – Analizira pogoje uporabe in identificira potencialno škodljive določbe.  
- **`FinalAnswerTool`** – Izboljšuje odgovore, ki jih ustvari AI.  
- **`HfApiModel (Qwen LLM)`** – Prilagojen **Qwen 32B LLM**, optimiziran za pravno analizo s tehniko **Low-Rank Adaptation (LoRA)**.  
- **`GradioUI`** – Zagotavlja interaktivni uporabniški vmesnik.  

---

## Zahteve za uporabo  

- **Python 3.8+**  
- **Hugging Face API ključ**  
- **CourtListener API ključ**  

---

## Avtorji  

- Ekipa RegulaTOS: **Fedja Močnik**, **Oliver Majer**, **Jaša Catar**, **Neva Marjanovič**

---

## Zahvale  

- **Hugging Face** – za njihove odprtokodne modele in Gradio framework.  
- **CourtListener API** – za dostop do pravnih podatkov in sodnih odločb.  
- **[Digital Services Terms and Conditions Database](https://platform-contracts.digital-strategy.ec.europa.eu/)** – za podatkovno infrastrukturo, ki omogoča analizo pogojev uporabe digitalnih storitev.  
---

## Zakaj je sledljiv AI ključen?  

V pravu je preglednost **bistvenega pomena**. Tracy ne ponuja le odgovorov, temveč **pokaže, kako do njih pride**. To zagotavlja:  

1. **Zanesljivost pravnih analiz** – Manj napačnih interpretacij in več zaupanja v rezultate.  
2. **Sledljivost odločitev** – Uporabniki lahko preverijo in razumejo, zakaj je AI podal določen odgovor.  
3. **Zaščito pred zavajajočimi pravnimi določbami** – Uporabniki digitalnih storitev lahko prepoznajo tveganja v pogojih uporabe.  

Z združevanjem **pravnega raziskovanja** in **zaščite potrošnikov** Tracy ponuja **inovativno rešitev** za transparentno in varno uporabo umetne inteligence v pravnem kontekstu.

