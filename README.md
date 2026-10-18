# Total Solar Eclipse of 2 August 2027 — maps & local circumstances

This repository computes the 2 August 2027 total solar eclipse from first principles and renders **41 maps**: a world overview, every country crossed by the path of totality, and a detailed set for **Egypt**, which gets the eclipse's greatest duration. The Egypt set has a governorate map, contact-time maps and 25 city maps (including Bawiti in Bahariya Oasis). The style follows Wolfram's [`SolarEclipse`](https://reference.wolfram.com/language/ref/SolarEclipse.html) maps: the path of totality, the obscuration zones, the central line and the local contact times.

![World overview](maps/01_world_overview_orthographic.png)

## Key facts (computed here)

| Quantity | Value |
|---|---|
| Date | Monday 2 August 2027 |
| Type | Total (Saros 136) |
| Greatest duration on the central line | 6m 23s (383.1 s) at 26.816N 31.143E, 10:00:17 UT, Sun altitude 80.9° — Western Desert ~36 km west of Tahta (Sohag) |
| Greatest eclipse | 25.502N 33.196E, 10:06:34 UT, totality 382.5 s (6m 22s) — Eastern Desert ~60 km east of Luxor |
| Central line on Earth | from 08:25:02 to 11:48:11 UT |
| Maximum path width | 259 km |
| Countries in the path of totality | Spain, Gibraltar, Morocco, Algeria, Tunisia, Libya, Egypt, the Halaib Triangle (administered by Egypt, claimed by Sudan; Natural Earth draws it as Sudan), Saudi Arabia, Yemen, Somalia (Somaliland/Puntland) |

All 2027 computations use NASA's published Besselian elements (F. Espenak, ΔT = 76 s); NASA lists greatest duration 6m 23.2s at 26°48.8'N 31°08.0'E and greatest eclipse 6m 22.7s at 25°30.4'N 33°10.8'E. An independent fit from JPL DE421 agrees within 0.3 s. Seconds are **truncated**, not rounded, as in NASA's tables (382.7 s → 6m 22s), so every Egyptian city gets at most 6m 22s; only a strip a few km wide along the central line reaches 6m 23s.

## Egypt — city by city (local time EEST = UT+3)

| City | Governorate | Type | Partial begins | Totality begins | Maximum | Totality ends | Partial ends | Totality | Obscuration | Sun alt. |
|---|---|---|---|---|---|---|---|---|---|---|
| Nag Hammadi | Qena | total | 11:38:51 | 13:00:33 | 13:03:44 | 13:06:56 | 14:25:07 | 6m 22s | 100.00% | 81.6° |
| Sohag | Sohag | total | 11:37:07 | 12:58:38 | 13:01:49 | 13:05:00 | 14:23:19 | 6m 22s | 100.00% | 81.2° |
| Abydos (El Balyana) | Sohag | total | 11:38:00 | 12:59:41 | 13:02:52 | 13:06:02 | 14:24:21 | 6m 21s | 100.00% | 81.5° |
| Qus | Qena | total | 11:40:07 | 13:01:51 | 13:05:01 | 13:08:12 | 14:26:12 | 6m 21s | 100.00% | 81.5° |
| Berenice | Red Sea | total | 11:48:31 | 13:10:34 | 13:13:45 | 13:16:54 | 14:33:58 | 6m 20s | 100.00% | 80.8° |
| Luxor | Luxor | total | 11:40:07 | 13:01:58 | 13:05:08 | 13:08:18 | 14:26:25 | 6m 20s | 100.00% | 81.8° |
| Tahta | Sohag | total | 11:36:28 | 12:57:56 | 13:01:06 | 13:04:16 | 14:22:37 | 6m 19s | 100.00% | 81.0° |
| Bawiti (Bahariya Oasis) | Giza | total | 11:29:26 | 12:50:10 | 12:53:19 | 12:56:28 | 14:15:23 | 6m 17s | 100.00% | 78.7° |
| El Hayz (Bahariya) | Giza | total | 11:29:14 | 12:50:08 | 12:53:17 | 12:56:25 | 14:15:32 | 6m 16s | 100.00% | 78.9° |
| Mandisha (Bahariya) | Giza | total | 11:29:35 | 12:50:19 | 12:53:27 | 12:56:35 | 14:15:30 | 6m 15s | 100.00% | 78.7° |
| Dendera | Qena | total | 11:39:40 | 13:01:21 | 13:04:28 | 13:07:35 | 14:25:38 | 6m 14s | 100.00% | 81.4° |
| Armant | Luxor | total | 11:39:58 | 13:01:55 | 13:05:02 | 13:08:08 | 14:26:23 | 6m 13s | 100.00% | 81.9° |
| Qena | Qena | total | 11:39:45 | 13:01:27 | 13:04:33 | 13:07:38 | 14:25:41 | 6m 11s | 100.00% | 81.3° |
| Asyut | Asyut | total | 11:35:23 | 12:56:46 | 12:59:49 | 13:02:53 | 14:21:22 | 6m 07s | 100.00% | 80.6° |
| Esna | Luxor | total | 11:40:24 | 13:02:43 | 13:05:36 | 13:08:28 | 14:27:00 | 5m 44s | 100.00% | 82.2° |
| Shalateen | Red Sea | total | 11:49:54 | 13:12:35 | 13:15:23 | 13:18:11 | 14:35:38 | 5m 36s | 100.00% | 80.9° |
| Marsa Alam | Red Sea | total | 11:45:45 | 13:07:54 | 13:10:40 | 13:13:25 | 14:31:00 | 5m 31s | 100.00% | 80.8° |
| Edfu | Aswan | total | 11:41:30 | 13:04:01 | 13:06:47 | 13:09:31 | 14:28:05 | 5m 30s | 100.00% | 82.3° |
| Siwa | Matrouh | total | 11:22:05 | 12:42:26 | 12:45:11 | 12:47:55 | 14:07:57 | 5m 28s | 100.00% | 75.5° |
| Mallawi | Minya | total | 11:34:07 | 12:55:34 | 12:58:17 | 13:01:00 | 14:19:48 | 5m 25s | 100.00% | 80.0° |
| Minya | Minya | total | 11:33:34 | 12:55:28 | 12:57:32 | 12:59:37 | 14:18:58 | 4m 09s | 100.00% | 79.6° |
| Kom Ombo | Aswan | total | 11:42:16 | 13:06:04 | 13:07:44 | 13:09:25 | 14:29:06 | 3m 21s | 100.00% | 82.6° |
| Daraw | Aswan | total | 11:42:19 | 13:06:20 | 13:07:48 | 13:09:16 | 14:29:10 | 2m 55s | 100.00% | 82.7° |
| El Quseir | Red Sea | total | 11:43:12 | 13:06:30 | 13:07:46 | 13:09:02 | 14:28:10 | 2m 31s | 100.00% | 80.6° |
| Aswan | Aswan | partial | 11:42:42 | — | 13:08:17 | — | 14:29:42 | — | 99.81% | 82.9° |
| Farafra | New Valley | partial | 11:28:49 | — | 12:53:16 | — | 14:16:00 | — | 99.69% | 79.5° |
| Safaga | Red Sea | partial | 11:41:46 | — | 13:06:04 | — | 14:26:28 | — | 99.62% | 80.3° |
| Kharga | New Valley | partial | 11:35:59 | — | 13:01:12 | — | 14:23:23 | — | 99.48% | 82.3° |
| Hurghada | Red Sea | partial | 11:40:57 | — | 13:04:59 | — | 14:25:17 | — | 98.56% | 80.0° |
| El Gouna | Red Sea | partial | 11:40:31 | — | 13:04:30 | — | 14:24:49 | — | 98.43% | 79.9° |
| Beni Suef | Beni Suef | partial | 11:33:29 | — | 12:56:51 | — | 14:17:44 | — | 98.20% | 78.6° |
| Faiyum | Faiyum | partial | 11:32:45 | — | 12:55:59 | — | 14:16:53 | — | 97.93% | 78.3° |
| Marsa Matruh | Matrouh | partial | 11:24:05 | — | 12:46:03 | — | 14:07:19 | — | 97.52% | 74.7° |
| Baris | New Valley | partial | 11:37:01 | — | 13:02:30 | — | 14:24:45 | — | 97.46% | 83.1° |
| Mut (Dakhla Oasis) | New Valley | partial | 11:32:37 | — | 12:57:44 | — | 14:20:26 | — | 96.94% | 81.7° |
| Ras Gharib | Red Sea | partial | 11:38:18 | — | 13:01:50 | — | 14:22:05 | — | 96.71% | 79.3° |
| El Tor | South Sinai | partial | 11:39:36 | — | 13:03:05 | — | 14:23:06 | — | 96.00% | 79.2° |
| Sharm El Sheikh | South Sinai | partial | 11:41:26 | — | 13:04:58 | — | 14:24:44 | — | 95.57% | 79.2° |
| Giza | Giza | partial | 11:32:59 | — | 12:55:43 | — | 14:16:07 | — | 94.99% | 77.7° |
| Cairo | Cairo | partial | 11:33:01 | — | 12:55:43 | — | 14:16:05 | — | 94.83% | 77.7° |
| Alexandria | Alexandria | partial | 11:29:33 | — | 12:51:33 | — | 14:11:53 | — | 93.37% | 76.1° |
| Dahab | South Sinai | partial | 11:41:18 | — | 13:04:23 | — | 14:23:49 | — | 93.24% | 78.6° |
| Tanta | Gharbia | partial | 11:32:02 | — | 12:54:13 | — | 14:14:18 | — | 92.74% | 76.8° |
| Suez | Suez | partial | 11:35:52 | — | 12:58:24 | — | 14:18:10 | — | 92.47% | 77.8° |
| Zagazig | Al Sharqia | partial | 11:33:13 | — | 12:55:28 | — | 14:15:26 | — | 92.44% | 77.1° |
| Abu Simbel | Aswan | partial | 11:42:29 | — | 13:08:32 | — | 14:30:27 | — | 91.98% | 85.0° |
| Mansoura | Dakahlia | partial | 11:32:40 | — | 12:54:36 | — | 14:14:22 | — | 91.10% | 76.6° |
| Ismailia | Ismailia | partial | 11:34:50 | — | 12:56:57 | — | 14:16:32 | — | 90.86% | 77.2° |
| Damietta | Damietta | partial | 11:33:22 | — | 12:54:55 | — | 14:14:15 | — | 88.90% | 76.3° |
| Port Said | Port Said | partial | 11:34:29 | — | 12:56:04 | — | 14:15:14 | — | 88.45% | 76.5° |
| Arish | North Sinai | partial | 11:37:46 | — | 12:59:05 | — | 14:17:32 | — | 85.81% | 76.5° |

The per-governorate summary is in [`results/egypt_governorates.csv`](results/egypt_governorates.csv).

## Other countries — selected cities in totality

| Country | City | Local max | Totality | Sun alt. |
|---|---|---|---|---|
| Spain | Cádiz | 10:46:53 (UT+2) | 2m 54s | 37.4° |
| Spain | Málaga | 10:49:06 (UT+2) | 1m 50s | 39.4° |
| Spain | Tarifa | 10:47:28 (UT+2) | 4m 39s | 38.2° |
| Spain | Algeciras | 10:47:41 (UT+2) | 4m 26s | 38.3° |
| Spain | Jerez de la Frontera | 10:47:07 (UT+2) | 1m 39s | 37.6° |
| Spain | Ceuta | 10:47:46 (UT+2) | 4m 48s | 38.5° |
| Spain | Melilla | 10:50:31 (UT+2) | 4m 33s | 41.0° |
| Spain | Marbella | 10:48:29 (UT+2) | 3m 17s | 38.9° |
| Gibraltar | Gibraltar | 10:47:49 (UT+2) | 4m 27s | 38.4° |
| Morocco | Tangier | 09:47:07 (UT+1) | 4m 50s | 37.9° |
| Morocco | Tetouan | 09:47:36 (UT+1) | 4m 51s | 38.4° |
| Morocco | Chefchaouen | 09:47:36 (UT+1) | 4m 13s | 38.5° |
| Morocco | Al Hoceima | 09:49:15 (UT+1) | 4m 26s | 39.9° |
| Morocco | Nador | 09:50:30 (UT+1) | 4m 15s | 41.0° |
| Morocco | Larache | 09:46:33 (UT+1) | 4m 18s | 37.6° |
| Morocco | Oujda | 09:51:44 (UT+1) | 1m 01s | 42.2° |
| Algeria | Oran | 09:53:40 (UT+1) | 5m 08s | 43.4° |
| Algeria | Tlemcen | 09:52:35 (UT+1) | 3m 11s | 42.8° |
| Algeria | Sétif | 10:02:32 (UT+1) | 3m 23s | 49.8° |
| Algeria | Batna | 10:03:46 (UT+1) | 5m 16s | 50.9° |
| Algeria | Biskra | 10:03:06 (UT+1) | 5m 02s | 50.6° |
| Algeria | Mostaganem | 09:54:41 (UT+1) | 5m 02s | 44.2° |
| Algeria | Chlef | 09:56:28 (UT+1) | 4m 34s | 45.5° |
| Algeria | Tébessa | 10:06:58 (UT+1) | 5m 11s | 53.0° |
| Algeria | Djelfa | 09:59:13 (UT+1) | 3m 25s | 47.9° |
| Tunisia | Sfax | 10:11:39 (UT+1) | 5m 39s | 56.2° |
| Tunisia | Kairouan | 10:10:14 (UT+1) | 2m 41s | 55.1° |
| Tunisia | Gabès | 10:10:45 (UT+1) | 4m 06s | 55.8° |
| Tunisia | Djerba (Houmt Souk) | 10:12:07 (UT+1) | 4m 41s | 56.7° |
| Tunisia | Gafsa | 10:08:18 (UT+1) | 5m 09s | 54.1° |
| Tunisia | Tozeur | 10:07:17 (UT+1) | 1m 46s | 53.6° |
| Tunisia | Kasserine | 10:08:13 (UT+1) | 5m 27s | 53.9° |
| Libya | Benghazi | 11:30:58 (UT+2) | 6m 09s | 67.8° |
| Libya | Al Jaghbub | 11:42:35 (UT+2) | 5m 40s | 74.1° |
| Sudan (north-east) | Halaib | 12:19:13 (UT+2) | 5m 18s | 79.7° |
| Saudi Arabia | Jeddah | 13:25:24 (UT+3) | 5m 58s | 76.3° |
| Saudi Arabia | Mecca | 13:26:49 (UT+3) | 5m 05s | 75.4° |
| Saudi Arabia | Taif | 13:28:03 (UT+3) | 3m 49s | 74.7° |
| Saudi Arabia | Abha | 13:37:19 (UT+3) | 6m 03s | 70.7° |
| Saudi Arabia | Al Bahah | 13:32:13 (UT+3) | 5m 09s | 72.9° |
| Saudi Arabia | Najran | 13:41:26 (UT+3) | 5m 10s | 68.1° |
| Saudi Arabia | Jizan | 13:39:50 (UT+3) | 3m 06s | 70.0° |
| Saudi Arabia | Al Lith | 13:29:49 (UT+3) | 6m 10s | 74.5° |
| Saudi Arabia | Al Qunfudhah | 13:33:09 (UT+3) | 5m 58s | 73.1° |
| Saudi Arabia | Khamis Mushait | 13:37:34 (UT+3) | 5m 59s | 70.5° |
| Yemen | Sana'a | 13:45:23 (UT+3) | 2m 26s | 66.9° |
| Yemen | Marib | 13:47:04 (UT+3) | 5m 44s | 65.5° |
| Yemen | Ataq | 13:51:05 (UT+3) | 5m 47s | 62.9° |
| Yemen | Sa'dah | 13:41:48 (UT+3) | 5m 55s | 68.4° |
| Somalia (Puntland & Somaliland) | Bosaso | 14:00:14 (UT+3) | 4m 04s | 57.8° |
| Somalia (Puntland & Somaliland) | Hafun | 14:04:31 (UT+3) | 5m 26s | 54.6° |
| Somalia (Puntland & Somaliland) | Caluula | 14:01:13 (UT+3) | 4m 14s | 56.2° |
| Somalia (Puntland & Somaliland) | Iskushuban | 14:03:23 (UT+3) | 3m 45s | 55.8° |

The full table, including partial-eclipse cities, is in [`results/local_circumstances_all_cities.csv`](results/local_circumstances_all_cities.csv).

## The 41 maps

### Overview

| | | |
|---|---|---|
| **1. World Overview Orthographic**<br>[![World Overview Orthographic](maps/01_world_overview_orthographic.png)](maps/01_world_overview_orthographic.png) | **2. Regional Overview Totality And Obscuration**<br>[![Regional Overview Totality And Obscuration](maps/02_regional_overview_totality_and_obscuration.png)](maps/02_regional_overview_totality_and_obscuration.png) | **3. Central Line Duration Width Profile**<br>[![Central Line Duration Width Profile](maps/03_central_line_duration_width_profile.png)](maps/03_central_line_duration_width_profile.png) |

### Countries on the path

| | | |
|---|---|---|
| **4. Spain**<br>[![Spain](maps/04_country_spain.png)](maps/04_country_spain.png) | **5. Gibraltar**<br>[![Gibraltar](maps/05_country_gibraltar.png)](maps/05_country_gibraltar.png) | **6. Morocco**<br>[![Morocco](maps/06_country_morocco.png)](maps/06_country_morocco.png) |
| **7. Algeria**<br>[![Algeria](maps/07_country_algeria.png)](maps/07_country_algeria.png) | **8. Tunisia**<br>[![Tunisia](maps/08_country_tunisia.png)](maps/08_country_tunisia.png) | **9. Libya**<br>[![Libya](maps/09_country_libya.png)](maps/09_country_libya.png) |
| **10. Egypt**<br>[![Egypt](maps/10_country_egypt.png)](maps/10_country_egypt.png) | **11. Sudan**<br>[![Sudan](maps/11_country_sudan.png)](maps/11_country_sudan.png) | **12. Saudi Arabia**<br>[![Saudi Arabia](maps/12_country_saudi_arabia.png)](maps/12_country_saudi_arabia.png) |
| **13. Yemen**<br>[![Yemen](maps/13_country_yemen.png)](maps/13_country_yemen.png) | **14. Somalia**<br>[![Somalia](maps/14_country_somalia.png)](maps/14_country_somalia.png) |  |

### Egypt — whole country

| | | |
|---|---|---|
| **15. Egypt Governorates Totality**<br>[![Egypt Governorates Totality](maps/15_egypt_governorates_totality.png)](maps/15_egypt_governorates_totality.png) | **16. Egypt Contact Times**<br>[![Egypt Contact Times](maps/16_egypt_contact_times.png)](maps/16_egypt_contact_times.png) |  |

### Egypt — cities

| | | |
|---|---|---|
| **17. Luxor**<br>[![Luxor](maps/17_egypt_city_luxor.png)](maps/17_egypt_city_luxor.png) | **18. Aswan**<br>[![Aswan](maps/18_egypt_city_aswan.png)](maps/18_egypt_city_aswan.png) | **19. Qena**<br>[![Qena](maps/19_egypt_city_qena.png)](maps/19_egypt_city_qena.png) |
| **20. Sohag**<br>[![Sohag](maps/20_egypt_city_sohag.png)](maps/20_egypt_city_sohag.png) | **21. Asyut**<br>[![Asyut](maps/21_egypt_city_asyut.png)](maps/21_egypt_city_asyut.png) | **22. Minya**<br>[![Minya](maps/22_egypt_city_minya.png)](maps/22_egypt_city_minya.png) |
| **23. Beni Suef**<br>[![Beni Suef](maps/23_egypt_city_beni_suef.png)](maps/23_egypt_city_beni_suef.png) | **24. Faiyum**<br>[![Faiyum](maps/24_egypt_city_faiyum.png)](maps/24_egypt_city_faiyum.png) | **25. Cairo**<br>[![Cairo](maps/25_egypt_city_cairo.png)](maps/25_egypt_city_cairo.png) |
| **26. Giza**<br>[![Giza](maps/26_egypt_city_giza.png)](maps/26_egypt_city_giza.png) | **27. Alexandria**<br>[![Alexandria](maps/27_egypt_city_alexandria.png)](maps/27_egypt_city_alexandria.png) | **28. Hurghada**<br>[![Hurghada](maps/28_egypt_city_hurghada.png)](maps/28_egypt_city_hurghada.png) |
| **29. Safaga**<br>[![Safaga](maps/29_egypt_city_safaga.png)](maps/29_egypt_city_safaga.png) | **30. El Quseir**<br>[![El Quseir](maps/30_egypt_city_el_quseir.png)](maps/30_egypt_city_el_quseir.png) | **31. Marsa Alam**<br>[![Marsa Alam](maps/31_egypt_city_marsa_alam.png)](maps/31_egypt_city_marsa_alam.png) |
| **32. Kharga**<br>[![Kharga](maps/32_egypt_city_kharga.png)](maps/32_egypt_city_kharga.png) | **33. Mut Dakhla Oasis**<br>[![Mut Dakhla Oasis](maps/33_egypt_city_mut_dakhla_oasis.png)](maps/33_egypt_city_mut_dakhla_oasis.png) | **34. Edfu**<br>[![Edfu](maps/34_egypt_city_edfu.png)](maps/34_egypt_city_edfu.png) |
| **35. Kom Ombo**<br>[![Kom Ombo](maps/35_egypt_city_kom_ombo.png)](maps/35_egypt_city_kom_ombo.png) | **36. Esna**<br>[![Esna](maps/36_egypt_city_esna.png)](maps/36_egypt_city_esna.png) | **37. Abu Simbel**<br>[![Abu Simbel](maps/37_egypt_city_abu_simbel.png)](maps/37_egypt_city_abu_simbel.png) |
| **38. Sharm El Sheikh**<br>[![Sharm El Sheikh](maps/38_egypt_city_sharm_el_sheikh.png)](maps/38_egypt_city_sharm_el_sheikh.png) | **39. Siwa**<br>[![Siwa](maps/39_egypt_city_siwa.png)](maps/39_egypt_city_siwa.png) | **40. Berenice**<br>[![Berenice](maps/40_egypt_city_berenice.png)](maps/40_egypt_city_berenice.png) |

## Arabic edition and book graphics

- **[`maps_ar/`](maps_ar/)**: the same 41 maps with every label in Arabic. Run `ECLIPSE_LANG=ar python -m eclipse2027.maps`. Matplotlib ≥ 3.11 shapes Arabic and applies the bidi algorithm itself, so strings are passed through unchanged. The maps use Eastern Arabic digits and Arabic city, governorate and country names.
- **[`book/`](book/)**: 224 Arabic figures and a Word edition (`book/word/`) of a ten-chapter book: the science, eclipse records through world history, eclipses in Egypt's history, the 2027 event, safe observing, introductory experiments, photography, apps and planning, extra maps and the Arabic atlas. Open [`book/index.html`](book/index.html) to browse them, and see [`book/README.md`](book/README.md) for details.
- Historical eclipses before 1900 (Ibn Yunus 977/978, Sohag 1882) are computed with ERFA's Moon98/EPV00 and the Espenak–Meeus ΔT polynomials (`eclipse2027/engine.py`). Results are cached in `results/historic_egypt_1000_1900.json` and `results/solar_eclipses_1901_2050.json`.

## How it is computed

1. **Besselian elements** (`eclipse2027/besselian.py`). The maps and book use NASA's published elements (`besselian.elements()`); as an independent check, `besselian.compute()` derives them from DE421: Skyfield gives apparent geocentric positions of the Sun and Moon from JPL **DE421**. The shadow axis, the fundamental-plane coordinates *x, y*, the declination *d*, the hour angle *μ* and the penumbral/umbral radii *l₁, l₂* are computed every 3 minutes over ±3.5 h and fitted with cubic polynomials in UT (residual < 10⁻⁷ Earth radii). The fitted elements are in [`results/besselian_elements.txt`](results/besselian_elements.txt).
2. **Local circumstances** (`eclipse2027/circumstances.py`). For any latitude and longitude this uses vectorised Newton iteration (Explanatory Supplement / Meeus) to find the time of maximum and the contacts C1–C4, then derives the magnitude, the obscuration, the duration of totality and the Sun's altitude. The whole map grids are evaluated at once.
3. **Path of totality**. The central line is the intersection of the shadow axis with the WGS-84 ellipsoid. The northern and southern limits are found by bisection perpendicular to the track. The central-line table is in [`results/central_line.csv`](results/central_line.csv).
4. **Maps** (`eclipse2027/maps.py`). Matplotlib, GeoPandas and Cartopy draw the Natural Earth borders (10 m countries and level-1 provinces such as Egypt's governorates). On each map, blue shows how long totality lasts, orange shows how much of the Sun is covered, the dark-blue lines mark the limits of totality and the red dashed line is the central line. Each Egyptian city map also draws the topocentric Sun–Moon phases from C1 to C4, as seen from that city.

**Accuracy notes:** the observer is at sea level, and the Moon's limb is treated as smooth (no mountain profile), so contact times are good to a few seconds. Edge-of-path durations can differ by more than that, because lunar valleys and mountains are ignored. Local times use the civil offsets in force on 2 Aug 2027 (Egypt EEST UT+3, Spain/Gibraltar CEST UT+2, Morocco UT+1, Algeria/Tunisia UT+1, Libya UT+2, Sudan UT+2, Saudi Arabia/Yemen/Somalia UT+3).

## Reproduce

```bash
pip install -r requirements.txt
python scripts/prepare_geodata.py      # optional: rebuilds data/*.geojson from Natural Earth
python -m eclipse2027.maps             # writes maps/*.png and results/*.csv (~1 min)
python -m eclipse2027.maps city:Luxor  # a single city / country:egypt / world_overview ...
```

The bundled `skyfield-data` package provides the DE421 ephemeris, so the computation needs no network access.
