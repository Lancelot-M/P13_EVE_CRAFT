REACTIONS = [("Composite", "Composites"), ("Hybrid Polymers", "Polymer"), ("Molecular-Forged Materials", "Molecular")]
COMPOSANTS = [("Protective", "Protective"), ("Construction Components", "Advanced"), ("Capital Construction Components", "Capital Part"), ("Hybrid Tech Components", "Subsystem")]
ITEMS = [("Subcap", "Subcapitaux"), ("Ship", "Ships T2"), ("Capital", "Capitaux"), ("Module", "Modules T2"), ("Charge", "Charges T2"), ("Drone", "Drones T2")]
RIGGS_PROD = [(1, "No rigg"), (0.96, "rigg T1"), (0.95, "rigg T2")]
RIGGS_REACTION = [(1, "No rigg"), (0.978, "rigg T1"), (0.974, "rigg T2")]
REACTION_STRUCTURES = [(1, "Atanor"), (1, "Tatara")]
MANUFACTURING_STRUCTURES = [(1, "Station"), (0.99, "Raitaru"), (0.99, "Azbel"), (0.99, "Sotiyo")]
ARBORESCENCE = [(0, "From Blueprint"), (1, "From Reaction"), (2, "From Raw")]
DECRYPTOR = [(0, "No decryptor"), (1, "Auto"), (2, "decryptor XXX")]
SKILL = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
ME_LIST = [(1, 0), (0.99, 1), (0.98, 2), (0.97, 3), (0.96, 4), (0.95, 5), (0.94,6), (0.93, 7), (0.92, 8), (0.91, 9), (0.90, 10)]
TE_LIST = [(1, 0), (0.98, 2), (0.96, 4), (0.94, 6), (0.92, 8), (0.90, 10), (0.92, 12), (0.94, 14), (0.96, 16), (0.98, 18), (0.80, 20)]

FROM_REACTION = ["Composite", "Hybrid Polymers", "Molecular-Forged Materials"]

PROTECTIVE_COMPONENTS = ["Auto-Integrity Preservation Seal", "Capital Core Temperature Regulator", "Neurolink Protection Cell", "Enhanced Neurolink Protection Cell", "Core Temperature Regulator",
                         "Genetic Lock Preserver", "Genetic Mutation Inhibiter", "Genetic Safeguard Filter", "Genetic Structure Repairer", "Life Support Backup Unit",
                         "Neurolink Enhancer Reservoir", "Programmable Purification Membrane", "Radar-FTL Interlink Communicator", "Gravimetric-FTL Interlink Communicator",
                         "Magnetometric-FTL Interlink Communicator", "Ladar-FTL Interlink Communicator", "U-C Trigger Neurolink Conduit", "R-O Trigger Neurolink Conduit",
                         "S-R Trigger Neurolink Conduit", "G-O Trigger Neurolink Conduit"]
TRIGLAVAN_COMPONENTS = ["Capital Singularity Radiation Convertor", "Capital Trinary State Processor", "Capital Zero-Point Field Manipulator", "Lattice Locked Dekaisogen",
                        "Radiation Absorption Thruster", "Singularity Radiation Convertor", "Trinary State Processor", "Zero-Point Field Manipulator"]

CAPITAUX = ["Titan", "Dreadnought", "Freighter", "Supercarrier", "Carrier", "Force Auxiliary", "Capital Industrial Ship"]
SUBCAP = ["Frigate", "Cruiser", "Battleship", "Industrial", "Destroyer", "Mining Barge", "Combat Battlecruiser", "Attack Battlecruiser"]

""" 
GROUP COULD BE SELECTED
    - COMPOSANTS:
        - Hybrid Tech Components
        - Construction Components except PROTECTIVE COMPO
        - Capital Construction Components except PROTECTIVE COMPO
        - Capital Advanced Components except PROTECTIVE COMPO
        - PROTECTIVE_COMPONENTS
    - REACTIONS:
        - Composite Reaction Formulas
        - Polymer Reaction Formulas
        - Molecular-Forged Reaction Formulas
        ( in the futur - Biochemical Formula)

CATEGORY COULD BE SELECTED
    - SHIP
    - MODULE
    - CHARGE
    - DRONE
    - FIGHTER

FUEL BLOCK SELF PROD:
    - YES
    - NO

RESSOURCES TREE:
    - FROM RAW
    - FROM REACTION
    - BP INPUT

DECRYPTOR:
    - AUTO
    - NO
    - XXX

BP STAT:
    - PIRATE
    - ME
    - TE

Skill:
    - Science 1
    - Science 2
    - Encryption method
"""