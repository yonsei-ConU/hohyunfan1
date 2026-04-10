import random
import copy
import statistics
import os
import json

class Trait:
    def __init__(self, trait_id, name, bonus_type, bonus_strength, weight, allowed_types):
        self.id = trait_id
        self.name = name
        self.bonus_type = bonus_type
        self.bonus_strength = bonus_strength
        self.weight = weight
        self.allowed_types = allowed_types

COMBAT = "FRIGATETYPE.COMBAT"
EXPLORE = "FRIGATETYPE.EXPLORE"
INDUSTRY = "FRIGATETYPE.MINING"
TRADE = "FRIGATETYPE.TRADE"
SUPPORT = "FRIGATETYPE.DEFAULT"
ALL_TYPES = [COMBAT, EXPLORE, INDUSTRY, TRADE, SUPPORT]
NON_COMBAT = [EXPLORE, INDUSTRY, TRADE, SUPPORT]
NON_EXPLORE = [COMBAT, INDUSTRY, TRADE, SUPPORT]
NON_INDUSTRY = [COMBAT, EXPLORE, TRADE, SUPPORT]
NON_TRADE = [COMBAT, EXPLORE, INDUSTRY, SUPPORT]
NON_SUPPORT = [COMBAT, EXPLORE, INDUSTRY, TRADE]

TRAIT_DATABASE = [
    Trait("TR_DMG_A", "Advanced Maintenance Drones", "DamageResist", 1, 10, ALL_TYPES),
    Trait("TR_DMG_B", "Holographic Components", "DamageResist", 1, 10, ALL_TYPES),
    Trait("TR_DMG_C", "Self-Repairing Hull", "DamageResist", 1, 10, ALL_TYPES),
    Trait("TR_TIME_1", "Local Time Dilator", "ExpeditionTime", -1, 10, ALL_TYPES),
    Trait("TR_TIME_2", "Alcubierre Drive", "ExpeditionTime", -2, 5, ALL_TYPES),
    Trait("TR_TIME_3", "Experimental Impulse Drive", "ExpeditionTime", -3, 1, ALL_TYPES),
    Trait("TR_FUEL_N1", "Oxygen Recycler", "FuelCost", -2, 10, NON_SUPPORT),
    Trait("TR_FUEL_N2", "Photon Sails", "FuelCost", -2, 10, NON_SUPPORT),
    Trait("TR_FUEL_N3", "Efficient Warp Drive", "FuelCost", -4, 5, NON_SUPPORT),
    Trait("TR_FUEL_N4", "Advanced Power Distributor", "FuelCost", -6, 5, NON_SUPPORT),
    Trait("TR_FUEL_N5", "Solar Panels", "FuelCost", -6, 5, NON_SUPPORT),
    Trait("TR_FUEL_S1", "Antimatter Cycler", "FuelCost", -3, 10, [SUPPORT]),
    Trait("TR_FUEL_S2", "High-Capacity Tanks", "FuelCost", -6, 5, [SUPPORT]),
    Trait("TR_FUEL_S3", "Generator Grid", "FuelCost", -9, 1, [SUPPORT]),
    Trait("TR_FUEL_S4", "Portable Fusion Ignitor", "FuelCost", -9, 1, [SUPPORT]),
    Trait("TR_COM_6A", "Cloaking Device", "Combat", 6, 1, [COMBAT]),
    Trait("TR_COM_6B", "Tremendous Cannons", "Combat", 6, 1, [COMBAT]),
    Trait("TR_COM_4A", "Ablative Armour", "Combat", 4, 5, [COMBAT]),
    Trait("TR_COM_4B", "Experimental Weaponry", "Combat", 4, 5, NON_SUPPORT),
    Trait("TR_COM_3A", "Reinforced Hull", "Combat", 3, 5, NON_COMBAT),
    Trait("TR_COM_3B", "Retrofitted Turrets", "Combat", 3, 5, NON_COMBAT),
    Trait("TR_COM_2A", "Ammo Fabricators", "Combat", 2, 5, [COMBAT]),
    Trait("TR_COM_2B", "Angry Captain", "Combat", 2, 5, [COMBAT]),
    Trait("TR_COM_2C", "Massive Guns", "Combat", 2, 10, NON_COMBAT),
    Trait("TR_COM_2D", "Ultrasonic Weapons", "Combat", 2, 10, NON_COMBAT),
    Trait("TR_COM_1A", "Aggressive Probes", "Combat", 1, 10, NON_COMBAT),
    Trait("TR_COM_1B", "Hidden Weaponry", "Combat", 1, 10, NON_COMBAT),
    Trait("TR_EXP_6A", "Cartography Drones", "Exploration", 6, 1, [EXPLORE]),
    Trait("TR_EXP_6B", "Spacetime Anomaly Shielding", "Exploration", 6, 1, [EXPLORE]),
    Trait("TR_EXP_4A", "Gravitational Visualiser", "Exploration", 4, 5, [EXPLORE]),
    Trait("TR_EXP_4B", "Interstellar Signal Array", "Exploration", 4, 5, [EXPLORE]),
    Trait("TR_EXP_3A", "Long-Distance Sensors", "Exploration", 3, 5, NON_EXPLORE),
    Trait("TR_EXP_3B", "Radio Telescopes", "Exploration", 3, 5, NON_EXPLORE),
    Trait("TR_EXP_2A", "Holographic Displays", "Exploration", 2, 5, [EXPLORE]),
    Trait("TR_EXP_2B", "Realtime Archival Device", "Exploration", 2, 5, [EXPLORE]),
    Trait("TR_EXP_2C", "Anomaly Scanner", "Exploration", 2, 10, NON_EXPLORE),
    Trait("TR_EXP_2D", "Stowaway Botanist", "Exploration", 2, 10, NON_EXPLORE),
    Trait("TR_EXP_1A", "Fauna Analysis Device", "Exploration", 1, 10, NON_EXPLORE),
    Trait("TR_EXP_1B", "Planetary Data Scoop", "Exploration", 1, 10, NON_EXPLORE),
    Trait("TR_IND_6A", "Asteroid Vaporizer", "Mining", 6, 1, [INDUSTRY]),
    Trait("TR_IND_6B", "Ultrasonic Welders", "Mining", 6, 1, [INDUSTRY]),
    Trait("TR_IND_4A", "Terraforming Beams", "Mining", 4, 5, [INDUSTRY]),
    Trait("TR_IND_4B", "Tractor Beam", "Mining", 4, 5, [INDUSTRY]),
    Trait("TR_IND_3A", "Asteroid Scanner", "Mining", 3, 5, NON_INDUSTRY),
    Trait("TR_IND_3B", "Remote Mining Unit", "Mining", 3, 5, NON_INDUSTRY),
    Trait("TR_IND_2A", "Extendable Drills", "Mining", 2, 5, [INDUSTRY]),
    Trait("TR_IND_2B", "Laser Drill Array", "Mining", 2, 5, [INDUSTRY]),
    Trait("TR_IND_2C", "Metal Detector", "Mining", 2, 10, NON_INDUSTRY),
    Trait("TR_IND_2D", "Ore Processing Unit", "Mining", 2, 10, NON_INDUSTRY),
    Trait("TR_IND_1A", "Harvester Drones", "Mining", 1, 10, NON_INDUSTRY),
    Trait("TR_IND_1B", "Mineral Extractors", "Mining", 1, 10, NON_INDUSTRY),
    Trait("TR_TRA_6A", "Mind Control Device", "Trade", 6, 1, [TRADE]),
    Trait("TR_TRA_6B", "Teleportation Device", "Trade", 6, 1, [TRADE]),
    Trait("TR_TRA_4A", "Automatic Investment Engine", "Trade", 4, 5, [TRADE]),
    Trait("TR_TRA_4B", "Propaganda Device", "Trade", 4, 5, [TRADE]),
    Trait("TR_TRA_3A", "Robot Butlers", "Trade", 3, 5, NON_TRADE),
    Trait("TR_TRA_3B", "Well-Groomed Crew", "Trade", 3, 5, NON_TRADE),
    Trait("TR_TRA_2A", "Negotiation Module", "Trade", 2, 5, [TRADE]),
    Trait("TR_TRA_2B", "Trade Analysis Computer", "Trade", 2, 5, [TRADE]),
    Trait("TR_TRA_2C", "HypnoDrones", "Trade", 2, 10, NON_TRADE),
    Trait("TR_TRA_2D", "Remote Market Analyser", "Trade", 2, 10, NON_TRADE),
    Trait("TR_TRA_1A", "AutoTranslator", "Trade", 1, 10, NON_TRADE),
    Trait("TR_TRA_1B", "Economy Scanner", "Trade", 1, 10, NON_TRADE)
]

NEGATIVE_TRAIT_DATABASE = [
    Trait("NEG_COM_1", "Faulty Torpedoes", "Combat", -6, 1, ALL_TYPES),
    Trait("NEG_COM_2", "Low-Energy Shields", "Combat", -4, 1, ALL_TYPES),
    Trait("NEG_COM_3", "Second-Hand Rockets", "Combat", -4, 1, ALL_TYPES),
    Trait("NEG_COM_4", "Cowardly Gunners", "Combat", -2, 1, ALL_TYPES),
    Trait("NEG_COM_5", "Fragile Hull", "Combat", -2, 1, ALL_TYPES),
    Trait("NEG_EXP_1", "Uncalibrated Warp Drive", "Exploration", -6, 1, ALL_TYPES),
    Trait("NEG_EXP_2", "Misaligned Sensors", "Exploration", -4, 1, ALL_TYPES),
    Trait("NEG_EXP_3", "Outdated Maps", "Exploration", -4, 1, ALL_TYPES),
    Trait("NEG_EXP_4", "Haunted Radar", "Exploration", -2, 1, ALL_TYPES),
    Trait("NEG_IND_1", "Clumsy Drill Operator", "Mining", -6, 1, ALL_TYPES),
    Trait("NEG_IND_2", "Small Hoppers", "Mining", -4, 1, ALL_TYPES),
    Trait("NEG_IND_3", "Underpowered Lasers", "Mining", -4, 1, ALL_TYPES),
    Trait("NEG_IND_4", "Wandering Compass", "Mining", -4, 1, ALL_TYPES),
    Trait("NEG_IND_5", "Lazy Crew", "Mining", -2, 1, ALL_TYPES),
    Trait("NEG_IND_6", "Malfunctioning Drones", "Mining", -2, 1, ALL_TYPES),
    Trait("NEG_TRA_1", "Roach Infestation", "Trade", -6, 1, ALL_TYPES),
    Trait("NEG_TRA_2", "Small Hold", "Trade", -4, 1, ALL_TYPES),
    Trait("TRA_TRA_3", "Thief On Board", "Trade", -4, 1, ALL_TYPES),
    Trait("NEG_TRA_4", "Badly Painted", "Trade", -2, 1, ALL_TYPES),
    Trait("NEG_TRA_5", "Rude Captain", "Trade", -2, 1, ALL_TYPES),
    Trait("NEG_UTIL_1", "Leaky Fuel Tubes", "FuelCost", 4, 1, ALL_TYPES),
    Trait("NEG_UTIL_2", "Inefficient Engine", "FuelCost", 2, 1, ALL_TYPES),
    Trait("NEG_UTIL_3", "Poorly-Aligned Ballast", "FuelCost", 2, 1, ALL_TYPES),
    Trait("NEG_UTIL_4", "Oil Burner", "FuelCost", 1, 1, ALL_TYPES),
    Trait("NEG_UTIL_5", "Thirsty Crew", "FuelCost", 1, 1, ALL_TYPES)
]

RANK_UP_THRESHOLDS = [4, 8, 15, 25, 30, 35, 40, 45, 50, 55]

class Frigate:
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
        self.traits = []
        self.negative_traits = []
        self.base_stats = {"Combat": 0, "Exploration": 0, "Mining": 0, "Trade": 0}
        self.current_stats = {"Combat": 0, "Exploration": 0, "Mining": 0, "Trade": 0}
        self.base_fuel_cost = 0
        self.expeditions = 0
        self.rank = 0
        self.frigate_class = "C"

    def assign_specialist_trait(self):
        if self.archetype == COMBAT:
            self.traits.append(Trait("TR_EXCL_COM", "Combat Specialist", "Combat", 15, 0, [COMBAT]))
        elif self.archetype == EXPLORE:
            self.traits.append(Trait("TR_EXCL_EXP", "Exploration Specialist", "Exploration", 15, 0, [EXPLORE]))
        elif self.archetype == INDUSTRY:
            self.traits.append(Trait("TR_EXCL_IND", "Industrial Specialist", "Mining", 15, 0, [INDUSTRY]))
        elif self.archetype == TRADE:
            self.traits.append(Trait("TR_EXCL_TRA", "Trade Specialist", "Trade", 15, 0, [TRADE]))
        elif self.archetype == SUPPORT:
            self.traits.append(Trait("TR_EXCL_SUP", "Support Specialist", "FuelCost", -15, 0, [SUPPORT]))

    def calculate_class(self):
        delta = len(self.traits) - len(self.negative_traits)
        if delta < 3:
            self.frigate_class = "C"
        elif delta == 3:
            self.frigate_class = "B"
        elif delta == 4:
            self.frigate_class = "A"
        else:
            self.frigate_class = "S"

    def trigger_rank_up_milestone(self, silent=False):
        if self.rank >= 10:
            return
        self.rank += 1
        for key in self.current_stats.keys():
            self.current_stats[key] += 1
        stats_keys = list(self.current_stats.keys())
        for _ in range(2):
            self.current_stats[random.choice(stats_keys)] += 1
        if self.negative_traits:
            self.negative_traits.pop(random.randrange(len(self.negative_traits)))
        elif len(self.traits) < 5:
            current_ids = [t.id for t in self.traits]
            valid_pool = [t for t in TRAIT_DATABASE if self.archetype in t.allowed_types and t.id not in current_ids]
            if valid_pool:
                weights = [t.weight for t in valid_pool]
                selected = random.choices(valid_pool, weights=weights, k=1)[0]
                self.traits.append(selected)
        self.calculate_class()

    def display_manifest(self):
        print(f"\n--- [{self.frigate_class}-Class] 호위함 매니페스트: {self.name} ---")
        print(f"함종: {self.archetype.split('.')[-1]} | 원정 횟수: {self.expeditions} (Rank {self.rank})")
        print(f"현재 스탯: {self.current_stats} (역산된 기초 스탯 총합: {sum(self.base_stats.values())})")
        print("활성화된 특성:")
        for idx, t in enumerate(self.traits):
            sign = "+" if t.bonus_strength > 0 else ""
            print(f"  Slot {idx+1}: {t.name} -> {t.bonus_type} {sign}{t.bonus_strength}")
        for t in self.negative_traits:
            print(f"  [!] 페널티: {t.name} -> {t.bonus_type} {t.bonus_strength}")
        print("-" * 50)

def generate_wild_frigate(name, archetype=None):
    if archetype is None:
        archetype = random.choice(ALL_TYPES)
    f = Frigate(name, archetype)
    f.assign_specialist_trait()
    f.base_fuel_cost = random.randint(2, 5) if archetype == SUPPORT else random.randint(8, 12)
    raw_bst = int(random.gauss(4.5, 3))
    bst = max(-5, min(14, raw_bst))
    stats_keys = list(f.base_stats.keys())
    for _ in range(abs(bst)):
        target = random.choice(stats_keys)
        f.base_stats[target] += 1 if bst > 0 else -1
    f.current_stats = f.base_stats.copy()
    f.expeditions = random.randint(0, 30)
    glitch = False
    if f.expeditions in RANK_UP_THRESHOLDS:
        if random.random() < 0.2:
            glitch = True
            for _ in range(6):
                f.current_stats[random.choice(stats_keys)] -= 1
    num_neg = random.randint(1, 2)
    f.negative_traits = random.sample(NEGATIVE_TRAIT_DATABASE, num_neg)
    target_rank = sum(1 for t in RANK_UP_THRESHOLDS if f.expeditions >= t)
    effective_rank_ups = target_rank - 1 if glitch else target_rank
    for _ in range(effective_rank_ups):
        f.trigger_rank_up_milestone(silent=True)
    f.calculate_class()
    return f

def run_monte_carlo_evaluation(target_frigate, iterations=10000):
    print(f"[{target_frigate.name}] 잠재력 분석 시작 (표본 크기: {iterations})...")
    archetype = target_frigate.archetype
    population_results = []
    target_potential_results = []
    for _ in range(iterations):
        wild = generate_wild_frigate("Sample", archetype=archetype)
        while wild.rank < 10:
            wild.trigger_rank_up_milestone(silent=True)
        score = sum(wild.current_stats.values()) + sum(t.bonus_strength for t in wild.traits if t.bonus_type in wild.current_stats)
        population_results.append(score)
    for _ in range(iterations):
        temp_f = copy.deepcopy(target_frigate)
        while temp_f.rank < 10:
            temp_f.trigger_rank_up_milestone(silent=True)
        score = sum(temp_f.current_stats.values())
        target_potential_results.append(score)
    pop_avg = statistics.mean(population_results)
    pop_std = statistics.stdev(population_results)
    target_avg = statistics.mean(target_potential_results)
    z_score = (target_avg - pop_avg) / pop_std if pop_std else 0
    print(f"\n--- 최종 잠재력 레포트 ---")
    print(f"모집단 만렙 평균: {pop_avg:.2f} (σ: {pop_std:.2f})")
    print(f"내 호위함 만렙 기댓값: {target_avg:.2f}")
    print(f"측정된 시그마: {z_score:+.3f} σ")
    if z_score > 3.5: tier = ("HOHYUN", "강호현")
    elif z_score > 2.5: tier = ("LEGENDARY", "전설급")
    elif z_score > 1.5: tier = ("ELITE", "엘리트")
    elif z_score > 0.5: tier = ("GOOD", "우수함")
    elif z_score > -0.5: tier = ("AVERAGE", "평범함")
    elif z_score > -1.5: tier = ("BAD", "부족함")
    elif z_score > -2.5: tier = ("DEFECTED", "결함 있음")
    else: tier = ("CONU", "교체 권고")
    print(f"최종 티어: [{tier[0]}] - {tier[1]}")

def create_frigate_from_input():
    print("\n" + "="*40)
    print(" 🚀 호위함 잠재력 측정기: 데이터 입력")
    print("="*40)
    name = input("호위함 이름: ")
    
    # 함종 입력을 표준화하기 위한 매핑 사전
    archetype_map = {
        'combat': COMBAT, '전투': COMBAT,
        'explore': EXPLORE, '탐험': EXPLORE,
        'mining': INDUSTRY, 'industry': INDUSTRY, '산업': INDUSTRY,
        'trade': TRADE, '무역': TRADE,
        'support': SUPPORT, '지원': SUPPORT, 'default': SUPPORT
    }
    
    print(f"함종 선택 (Combat, Explore, Mining, Trade, Support): ", end="")
    archetype_input = input().lower().strip()
    # 매핑 사전에 없으면 입력값을 대문자로 바꿔서 시도, 실패 시 COMBAT 기본값
    archetype = archetype_map.get(archetype_input, f"FRIGATETYPE.{archetype_input.upper()}")
    if archetype not in ALL_TYPES:
        archetype = COMBAT

    print("\n[1] 현재 화면에 표시된 4대 스탯 입력")
    c = int(input("  전투(Combat): "))
    e = int(input("  탐험(Exploration): "))
    i = int(input("  산업(Mining): "))
    t = int(input("  무역(Trade): "))
    print("\n[2] 성장 상태 입력")
    expeditions = int(input("  누적 원정 횟수: "))
    num_pos = int(input("  긍정적 특성 개수: "))
    num_neg = int(input("  부정적 특성 개수: "))
    f = Frigate(name, archetype)
    f.assign_specialist_trait()
    f.current_stats = {"Combat": c, "Exploration": e, "Mining": i, "Trade": t}
    f.expeditions = expeditions
    f.rank = sum(1 for milestone in RANK_UP_THRESHOLDS if expeditions >= milestone)
    
    key_map = {
        'combat': 'Combat', '전투': 'Combat', 'exp': 'Exploration', '탐험': 'Exploration',
        'mining': 'Mining', 'ind': 'Mining', '산업': 'Mining', 'trade': 'Trade', '무역': 'Trade',
        'fuel': 'FuelCost', '연료': 'FuelCost', 'time': 'ExpeditionTime', '시간': 'ExpeditionTime',
        'dmg': 'DamageResist', 'resist': 'DamageResist', '피해': 'DamageResist'
    }

    print("\n[3] 긍정적 특성 입력 (ㅇㅇ전문가는 제외)")
    p_idx = 0
    while p_idx < num_pos - 1:
        data = input(f"  긍정적 특성 {p_idx+1}: ").lower().split()
        if len(data) < 2: continue
        word, val = data[0], int(data[1])
        if word in key_map:
            match = next((t for t in TRAIT_DATABASE if t.bonus_type == key_map[word] and t.bonus_strength == val), None)
            if match:
                f.traits.append(match)
                print(f"  -> 매칭 성공: {match.name}")
                p_idx += 1

    print("\n[4] 부정적 특성 입력")
    n_idx = 0
    while n_idx < num_neg:
        data = input(f"  부정적 특성 {n_idx+1}: ").lower().split()
        if len(data) < 2: continue
        word, val = data[0], int(data[1])
        if word in key_map:
            match = next((t for t in NEGATIVE_TRAIT_DATABASE if t.bonus_type == key_map[word] and t.bonus_strength == val), None)
            if match:
                f.negative_traits.append(match)
                print(f"  -> 매칭 성공: {match.name}")
                n_idx += 1

    total_curr = sum(f.current_stats.values())
    pos_bonus = sum(t.bonus_strength for t in f.traits if t.bonus_type in f.current_stats)
    neg_penalty = sum(t.bonus_strength for t in f.negative_traits if t.bonus_type in f.current_stats)
    bst_total = total_curr - (pos_bonus + neg_penalty) - (f.rank * 6)

    for key in f.base_stats:
        ratio = f.current_stats[key] / max(1, total_curr)
        f.base_stats[key] = round(bst_total * ratio)
        
    f.calculate_class()
    return f


def save_frigate_to_file(frigate, filename="frigate.txt"):
    data = {
        "name": frigate.name,
        "archetype": frigate.archetype,
        "current_stats": frigate.current_stats,
        "base_stats": frigate.base_stats,
        "expeditions": frigate.expeditions,
        "traits": [t.id for t in frigate.traits],
        "negative_traits": [t.id for t in frigate.negative_traits]
    }
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")
    print(f"\n>> [{frigate.name}]의 데이터가 {filename}에 기록되었습니다.")

def load_all_frigates(filename="frigate.txt"):
    if not os.path.exists(filename):
        return []

    saved_frigates = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            d = json.loads(line)
            
            frigate = Frigate(d["name"], d["archetype"])
            frigate.current_stats = d["current_stats"]
            frigate.base_stats = d["base_stats"]
            frigate.expeditions = d["expeditions"]
            frigate.rank = sum(1 for m in RANK_UP_THRESHOLDS if frigate.expeditions >= m)
            
            for tid in d["traits"]:
                match = next((t for t in TRAIT_DATABASE if t.id == tid), None)
                if match: frigate.traits.append(match)
            
            for tid in d["negative_traits"]:
                match = next((t for t in NEGATIVE_TRAIT_DATABASE if t.id == tid), None)
                if match: frigate.negative_traits.append(match)
                
            frigate.calculate_class()
            saved_frigates.append(frigate)
            
    return saved_frigates


if __name__ == "__main__":
    my_f = create_frigate_from_input()
    save_frigate_to_file(my_f)
    my_f.display_manifest()
    run_monte_carlo_evaluation(my_f, iterations=100000)
