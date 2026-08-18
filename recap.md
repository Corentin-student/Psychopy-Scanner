# Recap devis - Psychopy Scanner IONS

**TJM** : 200 €/jour

## Lots retenus

| # | Lot | Jours | Prix |
|---|-----|-------|------|
| 2 | Portabilite Windows (locale, serial, resolution, config) | 2-3 | 400 - 600 € |
| 3 | Constructeur de paradigmes par regles (rule builder generique) | 8-10 | 1 600 - 2 000 € |
| 4 | Refonte UI + integration branding IONS | 3-4 | 600 - 800 € |
| 5 | Installeur Windows (.exe/.msi) - RISQUE technique | 6-8 | 1 200 - 1 600 € |
| 8 | Open source + documentation (repo IONS public) | 1-2 | 200 - 400 € |

**Total : 20-27 jours** = **4 000 - 5 400 €**

## Lots retires du devis
- Lot 1 : Refactoring + i18n EN
- Lot 6 : Paradigme Stress MIST
- Lot 7 : Output configurable + BIDS

## Hors scope
- Portabilite Mac (.dmg/.app) - non demande
- Branding IONS (logo, charte) - fourni par le client

## Ordre recommande
1. Lot 2 - Portabilite Windows (fix les hardcodes bloquants)
2. Lot 4 - Refonte UI + branding IONS
3. Lot 3 - Constructeur de paradigmes (grosse valeur ajoutee)
4. Lot 5 - Installeur Windows (une fois l'app stable)
5. Lot 8 - Open source + docs (publication finale)

## Phases de livraison
- **Phase 1 - Base portable + UI** (Lots 2+4) : 5-7 j = 1 000 - 1 400 €
- **Phase 2 - Creation paradigmes** (Lot 3) : 8-10 j = 1 600 - 2 000 €
- **Phase 3 - Distribution publique** (Lots 5+8) : 7-10 j = 1 400 - 2 000 €

## Alerte risque
**Lot 5 (installeur)** : Corentin a deja echoue sur un .exe unique (memoire p.48-49). Flask + PsychoPy ne cohabitent pas dans PyInstaller. Prevoir 2-3 j de R&D/prototypage avant engagement final sur l'estimation.
