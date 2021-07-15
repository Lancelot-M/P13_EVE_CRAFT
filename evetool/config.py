REACTIONS = [("Composite", "Composites"), ("Hybrid Polymers", "Polymer"), ("Molecular-Forged Materials", "Molecular")]
COMPOSANTS = [("Protective", "Protective"), ("Construction Components", "Advanced"), ("Capital Construction Components", "Capital Part"), ("Hybrid Tech Components", "Subsystem")]
ITEMS = [("Subcap", "Subcapitaux"), ("Ship", "Ships T2"), ("Capital", "Capitaux"), ("Module", "Modules T2"), ("Charge", "Charges T2"), ("Drone", "Drones T2")]
RIGGS_PROD = [(1, "No rigg"), (0.96, "rigg T1"), (0.95, "rigg T2")]
RIGGS_REACTION = [(1, "No rigg"), (0.978, "rigg T1"), (0.974, "rigg T2")]
REACTION_STRUCTURES = [(1, "Atanor"), (1, "Tatara")]
MANUFACTURING_STRUCTURES = [(1, "Station"), (0.99, "Raitaru"), (0.99, "Azbel"), (0.99, "Sotiyo")]
ARBORESCENCE = [(0, "From Blueprint"), (1, "From Reaction"), (2, "From Raw")]
DECRYPTOR = [(0, "Auto"), (1, "No decryptor")]
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

COST_INDEX = 1.03

DECRYPTORS_LIST = [
    {
        "Probability": 1.20,
        "Add Run": 1,
        "Add ME": 2,
        "Name": "Accelerant Decryptor"
    },
    {
        "Probability": 1.80,
        "Add Run": 4,
        "Add ME": -1,
        "Name": "Attainment Decryptor"
    },
    {
        "Probability": 0.60,
        "Add Run": 9,
        "Add ME": -2,
        "Name": "Augmentation Decryptor"
    },
    {
        "Probability": 1.90,
        "Add Run": 2,
        "Add ME": 1,
        "Name": "Optimized Attainment Decryptor"
    },
    {
        "Probability": 0.90,
        "Add Run": 7,
        "Add ME": 2,
        "Name": "Optimized Augmentation Decryptor"
    },
    {
        "Probability": 1.50,
        "Add Run": 3,
        "Add ME": 1,
        "Name": "Parity Decryptor"
    },
    {
        "Probability": 1.10,
        "Add Run": 0,
        "Add ME": 3,
        "Name": "Process Decryptor"
    },
    {
        "Probability": 1,
        "Add Run": 2,
        "Add ME": 1,
        "Name": "Symmetry Decryptor"
    }
]