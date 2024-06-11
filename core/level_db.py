ultimate_doom: dict[str, dict[str, list[int]]] = {
    "E1: Knee-Deep in the Dead": {
        "E1M1: Hangar": [0, 3],
        "E1M2: Nuclear Plant": [1, 6],
        "E1M3: Toxin Refinery": [2, 7],
        "E1M4: Command Control": [3, 3],
        "E1M5: Phobos Lab": [4, 9],
        "E1M6: Central Processing": [5, 4],
        "E1M7: Computer Station": [6, 4],
        "E1M8: Phobos Anomaly": [7, 1],
        "E1M9: Military Base": [8, 2]
    },
    "E2: Shores of Hell": {
        "E2M1: Deimos Anomaly": [10, 4],
        "E2M2: Containment Area": [11, 12],
        "E2M3: Refinery": [12, 6],
        "E2M4: Deimos Lab": [13, 10],
        "E2M5: Command Center": [14, 10],
        "E2M6: Halls of the Damned": [15, 3],
        "E2M7: Spawning Vats": [16, 6],
        "E2M8: Tower of Babel": [17, 0],
        "E2M9: Fortress of Mystery": [18, 1]
    },
    "E3: Inferno": {
        "E3M1: Hell Keep": [19, 1],
        "E3M2: Slough of Despair": [20, 3],
        "E3M3: Pandemonium": [21, 6],
        "E3M4: House of Pain": [22, 4],
        "E3M5: Unholy Cathedral": [23, 10],
        "E3M6: Mt. Erebus": [24, 3],
        "E3M7: Limbo": [25, 4],
        "E3M8: Dis": [26, 0],
        "E3M9: Warrens": [27, 1]
    },
    "E4: Thy Flesh Consumed": {
        "E4M1: Hell Beneath": [28, 2],
        "E4M2: Perfect Hatred": [29, 3],
        "E4M3: Sever the Wicked": [30, 22],
        "E4M4: Unruly Evil": [31, 2],
        "E4M5: They Will Repent": [32, 2],
        "E4M6: Against Thee Wickedly": [33, 3],
        "E4M7: And Hell Followed": [34, 4],
        "E4M8: Unto the Cruel": [35, 1],
        "E4M9: Fear": [36, 2]
    }
}

doom_ii: dict[str, dict[str, list[int]]] = {
    "Hell on Earth": {
        # [*] Maps 1 - 11
        "MAP01: Entryway": [37, 5],
        "MAP02: Underhalls": [38, 1],
        "MAP03: The Gantlet": [39, 1],
        "MAP04: The Focus": [40, 3],
        "MAP05: The Waste Tunnels": [41, 3],
        "MAP06: The Crusher": [42, 3],
        "MAP07: Dead Simple": [43, 1],
        "MAP08: Tricks and Traps": [44, 7],
        "MAP09: The Pit": [45, 6],
        "MAP10: Refueling Base": [46, 18],
        "MAP11: Circle of Death / 'O' of Destruction": [47, 3],
        
        # [*] Maps 12 - 20
        "MAP12: The Factory": [48, 4],
        "MAP13: Downtown": [49, 8],
        "MAP14: The Inmost Dens": [50, 0],
        "MAP15: Industrial Zone": [51, 11],
        "MAP16: Suburbs": [52, 4],
        "MAP17: Tenements": [53, 3],
        "MAP18: The Courtyard": [54, 4],
        "MAP19: The Citadel": [55, 9],
        "MAP20: Gotcha!": [56, 7],
        
        # [*] Maps 21 - 30
        "MAP21: Nirvana": [57, 0],
        "MAP22: The Catacombs": [58, 3],
        "MAP23: Barrels o'Fun": [59, 2],
        "MAP24: The Chasm": [60, 4],
        "MAP25: Bloodfalls": [61, 2],
        "MAP26: The Abandoned Mines": [62, 4],
        "MAP27: Monster Condo": [63, 8],
        "MAP28: The Spirit World": [64, 7],
        "MAP29: The Living End": [65, 0],
        "MAP30: Icon of Sin": [66, 0],
        
        # [*] Secret Maps
        "MAP31: Wolfenstein": [9, 4],
        "MAP32: Grosse": [67, 6]
    }
}

doom_ii_master_levels: dict[str, dict[str, list[int]]] = {
    "N/A": {
        "MAP01: Attack": [68, 1],
        "MAP02: Canyon": [72, 4],
        "MAP03: The Catwalk": [73, 2],
        "MAP04: The Combine": [74, 1],
        "MAP05: The Fistula": [76, 1],
        "MAP06: The Garrison": [77, 5],
        "MAP07: Titan Manor": [85, 7],
        "MAP08: Paradox": [82, 7],
        "MAP09: Subspace": [83, 2],
        "MAP10: Subterra": [84, 1],
        "MAP11: Trapped on Titan": [86, 2],
        "MAP12: Virgil's Lead": [88, 1],
        "MAP13: Minos' Judgement": [80, 5],
        "MAP14: Bloodsea Keep": [71, 4],
        "MAP15: Mephisto's Maosoleum": [79, 5],
        "MAP16: Nessus": [81, 1],
        "MAP17: Geryon": [78, 2],
        "MAP18: Vesperas": [87, 2],
        "MAP19: Black Tower": [70, 4],
        "MAP20: The Express Elevator to Hell": [75, 4],
        "MAP21: Bad Dream": [69, 1]
    }
}

final_doom_tnt_evilution: dict[str, dict[str, list[int]]] = {
    "N/A": {
        # [*] Maps 1 - 11
        "MAP01: System Control": [89, 1],
        "MAP02: Human BBQ": [90, 4],
        "MAP03: Power Control": [91, 3],
        "MAP04: Wormhole": [92, 8],
        "MAP05: Hanger": [93, 3],
        "MAP06: Open Season": [94, 1],
        "MAP07: Prison": [95, 4],
        "MAP08: Metal": [96, 4],
        "MAP09: Stronghold": [97, 11],
        "MAP10: Redemption": [98, 5],
        "MAP11: Storage Facility": [99, 2],
        
        # [*] Maps 12 - 20
        "MAP12: Crater": [100, 2],
        "MAP13: Nukage Processing": [101, 6],
        "MAP14: Steel Works": [102, 4],
        "MAP15: Dead Zone": [103, 6],
        "MAP16: Deepest Reaches": [104, 4],
        "MAP17: Processing Area": [105, 4],
        "MAP18: Mill": [106, 5],
        "MAP19: Shipping/Respawning": [107, 4],
        "MAP20: Central Processing": [108, 7],
        
        # [*] Maps 21 - 30
        "MAP21: Administration Center": [109, 4],
        "MAP22: Habitat": [110, 9],
        "MAP23: Lunar Mining Project": [111, 3],
        "MAP24: Quarry": [112, 3],
        "MAP25: Baron's Den": [113, 4],
        "MAP26: Ballistyx": [114, 2],
        "MAP27: Mount Pain": [115, 2],
        "MAP28: Heck": [116, 2],
        "MAP29: River Styx": [117, 3],
        "MAP30: Last Call": [118, 1],
        
        # [*] Secret Maps
        "MAP31: Pharaoh": [119, 2],
        "MAP32: Caribbean": [120, 3]
    }
}

final_doom_plutonia_experiment: dict[str, dict[str, list[int]]] = {
    "N/A": {
        # [*] Maps 1 - 11
        "MAP01: Congo": [121, 1],
        "MAP02: Well of Souls": [122, 0],
        "MAP03: Aztec": [123, 1],
        "MAP04: Caged": [124, 4],
        "MAP05: Ghost Town": [125, 1],
        "MAP06: Baron's Lair": [126, 6],
        "MAP07: Caughtyard": [127, 1],
        "MAP08: Realm": [128, 1],
        "MAP09: Abattoire": [129, 2],
        "MAP10: Onslaught": [130, 3],
        "MAP11: Hunted": [131, 1],
        
        # [*] Maps 12 - 20
        "MAP12: Speed": [132, 2],
        "MAP13: The Crypt": [133, 1],
        "MAP14: Genesis": [134, 3],
        "MAP15: The Twilight": [135, 19],
        "MAP16: The Omen": [136, 0],
        "MAP17: Compound": [137, 2],
        "MAP18: Neurosphere": [138, 1],
        "MAP19: NME": [139, 1],
        "MAP20: The Death Domain": [140, 2],
        
        # [*] Maps 21 - 30
        "MAP21: Slayer": [141, 0],
        "MAP22: Impossible Mission": [142, 4],
        "MAP23: Tombstone": [143, 5],
        "MAP24: The Final Frontier": [144, 7],
        "MAP25: The Temple of Darkness": [145, 1],
        "MAP26: Bunker": [146, 4],
        "MAP27: Anti-Christ": [147, 3],
        "MAP28: The Sewers": [148, 4],
        "MAP29: Odyssey of Noises": [149, 2],
        "MAP30: The Gateway to Hell": [150, 0],
        
        # [*] Secret Maps
        "MAP31: Cyberden": [151, 1],
        "MAP32: Go 2 It": [152, 2]
    }
}

doom_64: dict[str, dict[str, list[int]]] = {
    "Main Campaign": {
        # [*] Maps 1 - 10
        "MAP01: Staging Area": [153, 4],
        "MAP02: The Terraformer": [154, 2],
        "MAP03: Main Engineering": [155, 5],
        "MAP04: Holding Area": [156, 2],
        "MAP05: Tech Center": [157, 1],
        "MAP06: Alpha Quadrant": [158, 3],
        "MAP07: Research Lab": [159, 4],
        "MAP08: Final Outpost": [160, 2],
        "MAP09: Even Simpler": [161, 0],
        "MAP10: The Bleeding": [162, 7],
        
        # [*] Maps 11 - 20
        "MAP11: Terror Core": [163, 4],
        "MAP12: Altar Of Pain": [164, 2],
        "MAP13: Dark Citadel": [165, 2],
        "MAP14: Eye Of The Storm": [166, 1],
        "MAP15: Dark Entries": [167, 1],
        "MAP16: Blood Keep": [168, 1],
        "MAP17: Watch Your Step": [169, 2],
        "MAP18: Spawned Fear": [170, 5],
        "MAP19: The Spiral": [171, 0],
        "MAP20: Breakdown": [172, 3],
        
        # [*] Maps 21 - 24
        "MAP21: Pitfalls": [173, 3],
        "MAP22: Burnt Offerings": [174, 6],
        "MAP23: Unholy Temple": [175, 3],
        "MAP24: No Escape": [176, 3],
        
        # [*] "Fun" levels (25 - 27)
        "MAP25: Cat And Mouse": [177, 1],
        "MAP26: HardCore": [178, 0],
        "MAP27: Playground": [179, 0],
        
        # [*] Map 28
        "MAP28: The Absolution": [180, 0],
        
        # [*] Secret maps
        "MAP29: Outpost Omega": [181, 7],
        "MAP30: The Lair": [182, 4],
        "MAP31: In The Void": [183, 0],
        "MAP32: Hectic": [184, 0]
        
        # /-/ Extra maps (Title Map)
        # [i] Won't be included since it is not playable
    },
    "The Lost Levels (2020)": {
        # [*] The Lost Levels episode (2020 re-release)
        "MAP34: Plant Ops": [185, 5],
        "MAP35: Evil Sacrifice": [186, 3],
        "MAP36: Cold Grounds": [187, 1],
        "MAP37: Wretched Vats": [188, 4],
        "MAP38: Thy Glory": [189, 5],
        "MAP39: Final Judgement": [190, 0],
        
        # [*] The Lost Levels' "fun" level (map 40)
        "MAP40: Panic": [191, 0]
    }
}

no_rest_for_the_living: dict[str, dict[str, list[int]]] = {
    "N/A": {
        "MAP01: The Earth Base": [192, 7],
        "MAP02: The Pain Labs": [193, 12],
        "MAP03: Canyon of the Dead": [194, 5],
        "MAP04: Hell Mountain": [195, 8],
        "MAP05: Vivisection": [196, 8],
        "MAP06: Inferno of Blood": [197, 11],
        "MAP07: Baron's Banquet": [198, 11],
        "MAP08: Tomb of Malevolence": [199, 3],
        "MAP09: March of the Demons": [200, 5]
        # [!?] still can't believe this ends in 200 exactly LMAO
    }
}
