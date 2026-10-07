"""Places used on the maps: countries crossed by totality and their cities.

Coordinates are WGS-84 decimal degrees (N/E positive). ``utc`` is the civil
UTC offset in force on 2 August 2027 (summer time where it applies).
"""

COUNTRIES = {
    # key: (display name, ADM0_A3 codes, utc offset, tz label, map bounds lon0, lon1, lat0, lat1)
    "spain": ("Spain", ["ESP"], 2, "CEST", -8.0, -1.0, 34.6, 38.6),
    "gibraltar": ("Gibraltar & Strait of Gibraltar", ["GIB", "ESP", "MAR"], 2, "CEST", -6.4, -4.7, 35.6, 36.6),
    "morocco": ("Morocco", ["MAR"], 1, "UTC+1", -10.5, -0.5, 30.0, 36.4),
    "algeria": ("Algeria", ["DZA"], 1, "CET", -2.5, 9.5, 30.0, 37.4),
    "tunisia": ("Tunisia", ["TUN"], 1, "CET", 7.3, 11.8, 30.2, 37.6),
    "libya": ("Libya", ["LBY"], 2, "EET", 9.0, 25.5, 22.5, 33.5),
    "egypt": ("Egypt", ["EGY"], 3, "EEST", 24.5, 37.0, 21.5, 32.0),
    "sudan": ("Sudan (north-east)", ["SDN"], 2, "CAT", 29.0, 39.0, 17.0, 23.5),
    "saudi_arabia": ("Saudi Arabia", ["SAU"], 3, "AST", 34.5, 50.0, 15.5, 28.0),
    "yemen": ("Yemen", ["YEM"], 3, "AST", 42.0, 54.5, 11.5, 19.0),
    "somalia": ("Somalia (Puntland & Somaliland)", ["SOM", "SOL"], 3, "EAT", 42.5, 51.8, 6.5, 12.3),
}

CITIES = {
    "spain": [
        ("Cádiz", 36.5271, -6.2886), ("Seville", 37.3891, -5.9845), ("Málaga", 36.7213, -4.4214),
        ("Tarifa", 36.0128, -5.6061), ("Algeciras", 36.1408, -5.4562), ("Jerez de la Frontera", 36.6850, -6.1261),
        ("Granada", 37.1773, -3.5986), ("Almería", 36.8340, -2.4637), ("Córdoba", 37.8882, -4.7794),
        ("Huelva", 37.2614, -6.9447), ("Ceuta", 35.8894, -5.3213), ("Melilla", 35.2923, -2.9381),
        ("Marbella", 36.5101, -4.8825),
    ],
    "gibraltar": [
        ("Gibraltar", 36.1408, -5.3536), ("Tarifa", 36.0128, -5.6061), ("Algeciras", 36.1408, -5.4562),
        ("Ceuta", 35.8894, -5.3213), ("Tangier", 35.7595, -5.8340), ("Tetouan", 35.5785, -5.3684),
        ("La Línea", 36.1681, -5.3478), ("Estepona", 36.4276, -5.1463), ("Barbate", 36.1917, -5.9219),
    ],
    "morocco": [
        ("Tangier", 35.7595, -5.8340), ("Tetouan", 35.5785, -5.3684), ("Chefchaouen", 35.1688, -5.2636),
        ("Al Hoceima", 35.2517, -3.9372), ("Nador", 35.1681, -2.9335), ("Rabat", 34.0209, -6.8416),
        ("Fez", 34.0181, -5.0078), ("Larache", 35.1932, -6.1557), ("Oujda", 34.6814, -1.9086),
        ("Casablanca", 33.5731, -7.5898), ("Meknes", 33.8935, -5.5473), ("Marrakesh", 31.6295, -7.9811),
    ],
    "algeria": [
        ("Oran", 35.6971, -0.6308), ("Algiers", 36.7538, 3.0588), ("Tlemcen", 34.8828, -1.3167),
        ("Constantine", 36.3650, 6.6147), ("Annaba", 36.9000, 7.7667), ("Sétif", 36.1911, 5.4137),
        ("Batna", 35.5550, 6.1742), ("Biskra", 34.8504, 5.7280), ("Mostaganem", 35.9310, 0.0890),
        ("Chlef", 36.1650, 1.3317), ("Tébessa", 35.4040, 8.1240), ("El Oued", 33.3683, 6.8674),
        ("Ghardaïa", 32.4909, 3.6735), ("Djelfa", 34.6704, 3.2630), ("Laghouat", 33.8000, 2.8650),
    ],
    "tunisia": [
        ("Tunis", 36.8065, 10.1815), ("Sfax", 34.7406, 10.7603), ("Sousse", 35.8256, 10.6084),
        ("Kairouan", 35.6781, 10.0963), ("Gabès", 33.8815, 10.0982), ("Djerba (Houmt Souk)", 33.8750, 10.8575),
        ("Gafsa", 34.4250, 8.7842), ("Tozeur", 33.9197, 8.1335), ("Monastir", 35.7643, 10.8113),
        ("Bizerte", 37.2744, 9.8739), ("Kasserine", 35.1676, 8.8365), ("Medenine", 33.3549, 10.5055),
        ("Tataouine", 32.9297, 10.4518),
    ],
    "libya": [
        ("Tripoli", 32.8872, 13.1913), ("Benghazi", 32.1167, 20.0667), ("Misrata", 32.3754, 15.0925),
        ("Sirte", 31.2089, 16.5887), ("Tobruk", 32.0836, 23.9764), ("Derna", 32.7670, 22.6367),
        ("Ajdabiya", 30.7554, 20.2263), ("Al Bayda", 32.7627, 21.7551), ("Jalu", 29.0331, 21.5482),
        ("Kufra", 24.1990, 23.2900), ("Sabha", 27.0377, 14.4283), ("Ghadames", 30.1337, 9.5007),
        ("Brega", 30.4167, 19.5833), ("Al Jaghbub", 29.7425, 24.5167),
    ],
    "egypt": [],  # filled from EGYPT_CITIES below
    "sudan": [
        ("Wadi Halfa", 21.8019, 31.3497), ("Port Sudan", 19.6158, 37.2164), ("Halaib", 22.2190, 36.6400),
        ("Dongola", 19.1698, 30.4766), ("Abu Hamad", 19.5333, 33.3333), ("Atbara", 17.7022, 33.9864),
        ("Karima", 18.5500, 31.8500),
    ],
    "saudi_arabia": [
        ("Jeddah", 21.4858, 39.1925), ("Mecca", 21.3891, 39.8579), ("Medina", 24.5247, 39.5692),
        ("Taif", 21.2703, 40.4158), ("Riyadh", 24.7136, 46.6753), ("Abha", 18.2164, 42.5053),
        ("Al Bahah", 20.0129, 41.4677), ("Yanbu", 24.0890, 38.0637), ("Najran", 17.5656, 44.2289),
        ("Jizan", 16.8892, 42.5511), ("Bisha", 19.9922, 42.6053), ("Al Lith", 20.1497, 40.2711),
        ("Al Qunfudhah", 19.1264, 41.0789), ("Wadi ad-Dawasir", 20.4607, 44.7814), ("As Sulayyil", 20.4607, 45.5779),
        ("Rabigh", 22.7986, 39.0349), ("Khamis Mushait", 18.3000, 42.7333),
    ],
    "yemen": [
        ("Sana'a", 15.3694, 44.1910), ("Aden", 12.7855, 45.0187), ("Taiz", 13.5795, 44.0209),
        ("Al Hudaydah", 14.7978, 42.9545), ("Marib", 15.4591, 45.3253), ("Mukalla", 14.5425, 49.1242),
        ("Sayun", 15.9430, 48.7873), ("Ataq", 14.5377, 46.8319), ("Ibb", 13.9667, 44.1833),
        ("Al Ghaydah", 16.2079, 52.1760), ("Sa'dah", 16.9402, 43.7639), ("Shibam", 15.9266, 48.6266),
        ("Hadibu (Socotra)", 12.6510, 54.0236),
    ],
    "somalia": [
        ("Bosaso", 11.2842, 49.1816), ("Garowe", 8.4054, 48.4845), ("Qardho", 9.5000, 49.0833),
        ("Hafun", 10.4167, 51.2667), ("Berbera", 10.4396, 45.0143), ("Hargeisa", 9.5600, 44.0650),
        ("Erigavo", 10.6167, 47.3667), ("Caluula", 11.9667, 50.7500), ("Iskushuban", 10.2833, 50.2333),
        ("Burao", 9.5221, 45.5336), ("Las Anod", 8.4774, 47.3597),
    ],
}

# (name, governorate, lat, lon, gets its own detailed city map)
EGYPT_CITIES = [
    ("Luxor", "Luxor", 25.6872, 32.6396, True),
    ("Aswan", "Aswan", 24.0889, 32.8998, True),
    ("Qena", "Qena", 26.1551, 32.7160, True),
    ("Sohag", "Sohag", 26.5591, 31.6957, True),
    ("Asyut", "Asyut", 27.1783, 31.1859, True),
    ("Minya", "Minya", 28.1099, 30.7503, True),
    ("Beni Suef", "Beni Suef", 29.0661, 31.0994, True),
    ("Faiyum", "Faiyum", 29.3084, 30.8428, True),
    ("Cairo", "Cairo", 30.0444, 31.2357, True),
    ("Giza", "Giza", 30.0131, 31.2089, True),
    ("Alexandria", "Alexandria", 31.2001, 29.9187, True),
    ("Hurghada", "Red Sea", 27.2579, 33.8116, True),
    ("Safaga", "Red Sea", 26.7292, 33.9365, True),
    ("El Quseir", "Red Sea", 26.1042, 34.2778, True),
    ("Marsa Alam", "Red Sea", 25.0676, 34.8790, True),
    ("Kharga", "New Valley", 25.4390, 30.5586, True),
    ("Mut (Dakhla Oasis)", "New Valley", 25.4950, 28.9790, True),
    ("Edfu", "Aswan", 24.9781, 32.8789, True),
    ("Kom Ombo", "Aswan", 24.4527, 32.9283, True),
    ("Esna", "Luxor", 25.2934, 32.5540, True),
    ("Abu Simbel", "Aswan", 22.3372, 31.6258, True),
    ("Sharm El Sheikh", "South Sinai", 27.9158, 34.3300, True),
    # extra cities: included in tables and on overview maps
    ("Dendera", "Qena", 26.1417, 32.6703, False),
    ("Nag Hammadi", "Qena", 26.0490, 32.2410, False),
    ("Abydos (El Balyana)", "Sohag", 26.1850, 31.9190, False),
    ("Farafra", "New Valley", 27.0580, 27.9700, False),
    ("Baris", "New Valley", 24.6700, 30.6000, False),
    ("Siwa", "Matrouh", 29.2032, 25.5195, True),
    ("Bawiti (Bahariya Oasis)", "Giza", 28.3490, 28.8650, True),
    ("El Hayz (Bahariya)", "Giza", 28.0300, 28.6300, False),
    ("Mandisha (Bahariya)", "Giza", 28.3540, 28.9350, False),
    ("Marsa Matruh", "Matrouh", 31.3543, 27.2373, False),
    ("Port Said", "Port Said", 31.2653, 32.3019, False),
    ("Suez", "Suez", 29.9668, 32.5498, False),
    ("Ismailia", "Ismailia", 30.5965, 32.2715, False),
    ("El Tor", "South Sinai", 28.2397, 33.6219, False),
    ("Dahab", "South Sinai", 28.5096, 34.5136, False),
    ("Arish", "North Sinai", 31.1316, 33.7984, False),
    ("Berenice", "Red Sea", 23.9466, 35.4740, True),
    ("Shalateen", "Red Sea", 23.1339, 35.5940, False),
    ("Mansoura", "Dakahlia", 31.0409, 31.3785, False),
    ("Tanta", "Gharbia", 30.7865, 31.0004, False),
    ("Zagazig", "Al Sharqia", 30.5877, 31.5020, False),
    ("Damietta", "Damietta", 31.4165, 31.8133, False),
    ("Mallawi", "Minya", 27.7314, 30.8418, False),
    ("Tahta", "Sohag", 26.7693, 31.5021, False),
    ("Qus", "Qena", 25.9139, 32.7636, False),
    ("Armant", "Luxor", 25.6167, 32.5333, False),
    ("Daraw", "Aswan", 24.4042, 32.9206, False),
    ("Ras Gharib", "Red Sea", 28.3597, 33.0786, False),
    ("El Gouna", "Red Sea", 27.3949, 33.6782, False),
]

CITIES["egypt"] = [(n, la, lo) for n, _g, la, lo, _m in EGYPT_CITIES]
