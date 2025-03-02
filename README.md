# TracyAI
**Tracy** - Pravni AI asistent

"No trace, no case"

Tracy je pravni raziskovalni pomočnik, ki temelji na umetni inteligenci in je zasnovan za študente prava, pravne strokovnjake ter raziskovalce. Uporablja prilagojen veliki jezikovni model (LLM - 32B Qwen finetunan za pravno uporabo) za iskanje ustreznih sodnih primerov v ZDA s pomočjo CourtListener API. To orodje se lahko uporablja za pravne domače naloge, raziskave primerov ali splošno pravno referenco.

V pravu umetna inteligenca ne sme delovati kot "črna skrinjica" (blackbox). S Tracy gradimo sledljiv in transparenten AI, kjer so vsi koraki raziskave in odločanja jasno prikazani.

## Funkcionalnosti

Iskanje primerov: Poiščite sodne primere v ZDA na podlagi ključnih besed, pristojnosti in časovnega obdobja.

Preverjanje citatov: Preverite status in obravnavo pravnega citata.

Gradio UI: Uporabniku prijazen vmesnik, zgrajen na podlagi Hugging Face odprtokodne dokumentacije.

Analiza s pomočjo LLM: Uporablja prilagojen Qwen model za zagotavljanje inteligentne pravne analize.

### Struktura projekta
```
- tools/                 # Dodatna, neintegrirana orodja
- Gradio_UI/             # Uporabniški vmesnik, zgrajen z Gradio (Hugging Face)
- agent.json             # Metapodatki in konfiguracije agenta
- app.py                 # Glavna skripta aplikacije
- prompts.yaml           # Predloge pozivov za AI model
```

## Pregled funkcionalnosti (app.py)

Glavna logika projekta je implementirana v **app.py**. Tu je pregled ključnih komponent:

search_court_cases(): Pošlje zahtevo API-ju CourtListener za iskanje pravnih primerov glede na parametre uporabnika.

check_citation_status(): Preveri status in precedenčno vrednost primera na podlagi njegovega citata.

FinalAnswerTool: Obdeluje in izboljšuje končne odgovore, ki jih ustvari AI.

HfApiModel (Qwen LLM): Uporablja Hugging Face Qwen LLM, ki je bil prilagojen na podatkih o sodnih primerih v ZDA s tehniko Low-Rank Adaptation (LoRA). LoRA je učinkovita metoda za prilagajanje velikih modelov z minimalnimi računalniškimi viri.

GradioUI: Zagotavlja interaktivni vmesnik za uporabnike.

### O CourtListener API

CourtListener API je brezplačna pravna raziskovalna baza, ki omogoča dostop do sodnih odločb v ZDA. Uporabnikom omogoča pridobivanje mnenj, metapodatkov in precedenčnega statusa sodnih primerov. Ta projekt uporablja CourtListener za iskanje ustreznih pravnih informacij na podlagi uporabniških poizvedb.

### Zahteve

Za delovanje projekta potrebujete:

Python 3.8+

Hugging Face API ključ (brezplačno na voljo)

CourtListener API ključ (brezplačno ob registraciji)


**Avtorji**: Fedja Močnik, Oliver Majer

## Zahvale

Hugging Face za njihove odprtokodne modele in Gradio framework.

CourtListener API za omogočanje brezplačnega dostopa do pravnih podatkov.

## Zakaj sledljiv AI?

V pravu je preglednost ključnega pomena. Tracy je zasnovana tako, da omogoča sledljivost vseh svojih odločitev in raziskav. Naš cilj je graditi AI, ki omogoča transparentnost in ponovljivost pravne analize, kar povečuje zaupanje in zanesljivost rezultatov.
