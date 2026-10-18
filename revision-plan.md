# 钛论文修改方案 v7（合并 V9.0 工程细节并修正其机理错误）

> 对象：`manuscript.tex`（836 行，21 节，10 条 Limitations）
> 方法：先对"前面几轮讨论"的每条论断做独立核查（含数值复算），再判断哪些可进论文、哪些必须废弃；最后给出带行号的逐节修改指令与可粘贴英文。
> 与之前所有版本（V2–V5）的关系：本版**取代**前几版。前几版把"MgO 完全不溶 / 动力学阻断 / MgCl₂ 是化学计量消耗品"当作新叙事写进去，经核查是错的，见 §1.3。

---

## 0. 结论摘要

1. **论文的科学内核不需要推翻。** `Eq.(camgo) → Eq.(cross) → Eq.(amgo)` 这条推理链是本稿最有价值的部分，它比讨论中提出的任何"动力学阻断"说法都更严谨、更抗审。**保留并强化，不要替换。**
2. **讨论中有 3 条论断必须废弃**：MgO"完全不溶/不解离"、Ca 还原 MgO 被"固态壳层动力学阻断"、"MgCl₂ 是需按化学计量补充的消耗品"。三条都与论文自己引用的 Ito & Morita 溶解度数据（2.35 wt% @800 °C）直接冲突，若写入正文，等于自己拆掉摘要里的 closed-loop 表述。
3. **论文真正的缺口在工程层，不在化学层**：产物"悬浮"与密度矛盾（L138、L601）、还原剂接触路径未定义（合金比熔盐轻）、`screening` 无法分离同粒径 Ti/TiO₂（L138）、全篇没有产物排出机制、"Ca + Mg²⁺ 置换"被错误归入法拉第损失（L597）。这五条 R3 没提，但任何一个懂熔盐的审稿人都会问。
4. **修改量**：新增 2 个小节（固相脱氧 / 反应器与半连续操作）+ 4 段英文 + 3 处措辞修正 + 1 条新 Limitation + 2 处数值复核。不需要重写全文。
5. **定位建议**：维持"Conceptual Process Design"，投 *Journal of Sustainable Metallurgy* 或 *Metall. Mater. Trans. B*。若肯补一个 1–2 周的低成本实验（600 °C 下 CaO/MgO 溶解度测定），R2 的"无实验"死穴即可解除，见 §6。

---

## 0.5 对 V9.0 / V10.0 方案的逐条裁决

结论先行：**工程层约 80% 可用，机理层约 40% 可用，有一条关键尺寸是致命的。** 总合理度约 65%。

| V9/V10 条目 | 裁决 | 理由 |
|---|---|---|
| 固相脱氧（TiO₂ 不溶，液–固界面脱氧） | ✅ 采纳 | 论文 L601 只隐含，需明说 |
| Ca 主力 / Mg 物性调节 | ✅ 采纳 | 论文 L331 已有，非新增 |
| 承认 camgo 自发（ΔG=−38.2） | ✅ 采纳 | 论文 Eq.(camgo) 已有 |
| **"固态 MgO 壳层 + 微裂纹 → 动力学抑制"** | ❌ **废弃** | 见 §0.6 推导 D1：该反应无产物层，产物全部离开界面 |
| **"MgO 是死结，堵孔钝化主因"** | ❌ **废弃** | 见 D2：需 camgo 慢 **且** MgO 不溶的双重条件，与 2.35 wt% 数据冲突 |
| CaO "活结"、原位造孔自清洁 | ✅ 采纳 | 论文 L666–670 的 [Ca₂O]²⁺/[Ca₃O]⁴⁺ 络合机制更严谨，直接引用即可 |
| 纯 Mg 体系三死穴 | ✅ 采纳（改一处） | "MgO 无法原位电解再生"→"MgO 溶解度显著低于 CaO"，不要说"不溶" |
| 纯 Ca 体系 CaO 过饱和钝化 | ⚠ 有限采纳 | 只作 Case II 的次要风险，不作主张 |
| Regime II 连续共沉积 | ✅ 采纳 | 论文 L426–431 已有 |
| "寄生反应计入 5–10% 逆反应损失" | ⚠ **改口径** | 见 §1.3 论断 C：不是法拉第损失，是电压效率损失 |
| **"MgCl₂ 是消耗品，按速率补充"** | ⚠ **改口径** | 见 D4：补充量由物理损失定（~15–50 kg/ton），非化学计量 |
| 酸性气氛蒸发结晶防 MgCl₂ 水解 | ✅ **采纳（新增）** | 论文 L718 只讲了脱水，没讲回收蒸发 |
| 坩埚作阴极 | ✅ **采纳（新增）** | 同时解决接触、收集、密度三个问题 |
| 绝缘多孔陶瓷罩 | ✅ **采纳**（标注 concept） | 论文缺，应补 |
| **"阳极与槽底保持 10 cm 安全距离"** | ❌❌ **致命，废弃** | 见 D3：欧姆压降 **7.86 V**，净能耗飙到 ~33,700 kWh/ton，优势归零 |
| 45° 漏斗形斜底 | ⚠ **改为 ≥55° 并注明依据缺失** | 粉体休止角 30–45°，45° 处于临界，高温泥浆易架桥 |
| 不用高温抽吸泵（堵、短路、动密封） | ✅ **采纳（新增）** | 论证充分，可直接写 |
| 半连续 24 h 排料 | ✅ **采纳（新增）** | |
| 冷启动顺序（先建金属池再喂料） | ✅ **采纳（新增）** | 论证正确：绝缘氧化物先入会堵电流路径 |
| 六步分离法 | ✅ 采纳（第五步要改） | |
| **"真空精炼 1000 °C 去残氧"** | ⚠ **改为 <900 °C 或 Ca 蒸气** | 见 D5：α→β 转变温度 882 °C 以上，1000 °C 真空退火会烧结多孔粉 |
| 后处理能耗 800–1500 kWh/ton | ❌ **废弃数字** | 与论文 L597(300)、L736(200–500) 冲突，且无出处 |
| 620 °C 硬地板 | ✅ 采纳 | 论文 L730 已有 |
| SI 体积膨胀 22.51 vs 18.88 cm³ | ⚠ **改用途** | 原推论（堵孔）错；改为"孔隙容量约束"支撑 Eq.(amgo) |
| 期刊定位 / Go-No-Go | ✅ 采纳 | 论文 L762 已有 Go/No-Go |

**V9/V10 的一个根本误判**：它认为"外部清单没有解决 R3 的死结，必须用动力学抑制来救"。这个前提是错的——论文的 `Eq.(camgo) → Eq.(cross) → Eq.(amgo) → Case I/II 双包络` **已经用"不选"解决了**：不判断 camgo 快慢，只给两端，能量差 3%。不需要也不会被"动力学抑制"救，反而会被它拖累。

---

## 0.6 五个决定性推导

### D1：`Ca + MgO → CaO + Mg` 没有产物层，因此"被固态壳层抑制"在机理上不成立

反应物：液态合金中的 Ca + 固态 MgO。产物：**CaO（溶于 CaCl₂ 熔盐）+ Mg（进入合金相）**。

关键对比：

| 反应 | 产物是否留在界面 | 有无产物层阻力 |
|---|---|---|
| `TiO₂ + 2Ca → Ti + 2CaO` | Ti 是**固相，留在原地** | **有**（多孔 Ti 层扩散，SCM 建模对象） |
| `Ca + MgO → CaO + Mg` | CaO 溶解、Mg 入合金 | **无** |

两个产物**全部离开界面**：CaO 在 CaCl₂ 中溶解度很高（正是论文 L662 依赖的），Mg 与合金互溶。界面上留下的只有正在被消耗、不断缩小的 MgO 本身——它不是"生成物壳层"，而是反应物。

**因此该反应的动力学不应慢于 TiO₂ 还原，反而更快**：MgO 是原位生成的亚微米颗粒（比表面积远大于 25–100 µm 前驱体），且无产物层。V9/V10 的"致密壳层 + 微裂纹"图像把"反应物"误当成了"产物壳"。

**推论**：既然 camgo 很可能快，则——
- Case I（Ca 为唯一净氧载体）是更可能的基准，而非极限；
- `a_MgO` 被该反应自动压制在低值，Eq. `amgo` **自动满足**；
- MgO 不累积，不构成永久钝化；
- Mg 净化学消耗为零（论文 Table `mbalance` 脚注 a 正确）。

> 建议：**把 Case I 设为基准情形，Case II 作为乐观上界**（现在是反的）。理由：(a) 更可能；(b) 自动满足 Eq. `amgo`；(c) 能量只差 3%；(d) 正面接受 R3 的质疑，反而最自洽。这是 V9/V10 和此前所有版本都没提出的修正。

### D2：MgO"死结"需要双重条件同时成立，概率很低

要让 MgO 永久堵孔，必须同时满足：
1. camgo **慢**（否则被 Ca 化学清除）；
2. MgO **不溶**（否则溶解离开）。

而论文 L664 的数据是 **2.35 wt% @800 °C，外推 0.5–1.2 wt% @600 °C**。条件 2 已被实验否定。所以"死结"是一个低概率交集，不宜作为主叙事。

更重要的是量级：设 1 wt% 溶解度对应 `x_MgO,sat ≈ 0.023`，则要求 `a_MgO < 5×10⁻³` 意味着工作浓度

```
x_MgO < 5×10⁻³ × 0.023 ≈ 1.15×10⁻⁴  →  约 0.005 wt% = 50 ppm
```

即工作浓度必须低于饱和度的 **约 1/200**。按 201 t 盐库存算，溶解 MgO 总量仅 ~10 kg；而 1000 t/y 产能对应 MgO 生成速率 ~0.027 kg/s（Case II），周转时间

```
τ = 10 kg / 0.027 kg/s ≈ 370 s ≈ 6 min
```

**Case II 下，Eq.(amgo) 要求 6 分钟级的 MgO 周转**——极苛刻，任何波动都会让 `a_MgO` 冲高。而 Case I 下 MgO 由化学还原直接在界面消耗，不需要溶解库存，约束自动满足。这是"应把 Case I 设为基准"的第二个理由。

### D3："10 cm 安全距离"会让能耗优势归零（V9/V10 最严重错误）

欧姆压降 `jL/κ`，取论文自己的设计点 `j = 1.1 A/cm²`、`κ = 1.4 S/cm`：

```
L = 10 cm  →  ΔV = 1.1 × 10 / 1.4 = 7.86 V
L = 1.1 cm →  ΔV = 1.1 × 1.1 / 1.4 = 0.86 V ≈ 论文的 0.9 V 预算  ✓
```

10 cm 时电池电压 ≈ 2.73 + 0.30 + 0.20 + 7.86 = **11.1 V**，净能耗

```
12,552 × 11.1/4.13 ≈ 33,700 kWh/ton-Ti
```

**落入 Kroll 区间（30,000–40,000），全部优势消失。** 论文 L442 已经算过：2.5 cm 就会吃掉一半电压预算。

**正确做法：用隔离代替距离。**
- 极距 **≤1.1 cm**，由欧姆预算锁定；
- 短路防护靠**陶瓷罩/隔膜**，不靠加大间距；
- 沉渣高度靠**排料频率**控制，不靠 10 cm 富余；
- 若坩埚作阴极，则**水平方向**（阳极↔坩埚侧壁）是电流路径，受 1.1 cm 约束；**垂直方向**（阳极↔沉渣面）只受短路约束，可留几 cm，但要靠罩子而非距离保证。

> 这一条必须写进论文并明确反驳"加大间距防短路"，否则两版方案会互相打架。

### D4：MgCl₂ 的真实补充量比 Kroll 的镁耗低一个数量级

按物理损失（不是化学计量）估算，Case I 基准：

```
渣量（CaO）        2,343 kg/ton-Ti
渣中夹带盐（1:1）  ≈2,343 kg/ton-Ti
水洗回收率 98%     → 损失 ≈47 kg 盐/ton
MgCl₂ 占盐 30 wt%  → ≈14 kg MgCl₂/ton
加 freeboard 蒸发（密封冷凝回收） <5 kg
────────────────────────────────────
合计              ≈15–50 kg MgCl₂ / ton-Ti
```

对比 Kroll 法镁耗约 **200–400 kg/ton-Ti**。**低一个数量级。**

这就是"消耗品"争论的正确收尾方式：不说"不消耗"，而是给出这个数，并指明它由回收率而非化学计量决定。审稿人看到 15–50 kg 对 200–400 kg 的对比，这个议题就结束了。

### D5：真空精炼温度上限、45° 倾角、洗水量三处工程修正

**(a) 真空精炼不能说 1000 °C。** Ti 的 α→β 转变在 882 °C，自扩散在此之上急剧增大；1000 °C 真空退火会让多孔钛粉**烧结、闭孔、团聚**，破坏"直接得到多孔粉"这一核心卖点。改为：
- **<900 °C 长时间真空脱氧**，或
- **Ca 蒸气脱氧**（Okabe 路线，论文已引 L47），或
- **Ar–H₂ 气氛还原**。

**(b) 45° 漏斗偏临界。** 粉体休止角 30–45°，45° 正处在临界值，高温泥浆在斜面上易架桥、不下料。建议写 **≥55°**，并注明"倾角依据未经验证，需中试标定"；同时给出松动手段（槽底惰性气体脉冲、机械振动）。

**(c) 洗水量要按 11 wt% 夹带重算。** 11 wt% → 110 kg 盐/ton-Ti；CaCl₂ 溶解度 74.5 g/100 mL、MgCl₂ 54.3 g/100 mL；三级逆流、每级液固比 3:1 → 总水约 **0.5–1.5 m³/ton**。论文 L138 的"0.2–1 m³"下限偏低，建议改为 **0.5–1.5 m³**。

---

## 1. 核查：讨论中哪些对、哪些错

### 1.1 完全正确，且论文已经写了（不用改）

| # | 论断 | 论文位置 | 核查 |
|---|---|---|---|
| 1 | Ca 是主力还原剂，Mg 提供 600 °C 下的液相 | L331、L433、L746 | ✅ 正确 |
| 2 | `Ca + MgO → CaO + Mg` 自发，ΔG°=−38.2 kJ/mol，K=194 | L327、Eq.(camgo) | ✅ 复算 K₂=192.9 |
| 3 | Ca 脱氧极限 20.2 ppm、Mg 3908 ppm，差 193× | L322、Table `deox` | ✅ 复算 w=1/K₁，20.3 ppm |
| 4 | 600 °C 低于四种纯盐熔点，靠混合熵降液相线到 543.7 °C | L140 | ✅ 逻辑正确 |
| 5 | 必须 620 °C 硬地板（液相线 ±50 °C 不确定度只剩 6 °C 余量） | L730 | ✅ 正确，且已有 |

> 这五条是讨论中最有价值的部分，**但论文原稿已经全部具备，且表述比讨论更准确**。不需要"整合"，只需要在回复信里对 R3 引用它们。

### 1.2 方向对，但表述必须修正

| # | 讨论中的说法 | 问题 | 应改成 |
|---|---|---|---|
| 6 | "Ca 优先还原 Mg²⁺" | **方向错**。E°(Mg²⁺/Mg)=−2.37 V > E°(Ca²⁺/Ca)=−2.87 V，阴极上 **Mg 优先析出**，Ca 要靠 Mg 达到扩散极限后才共析（论文 L426–431 已正确） | "Mg²⁺ 优先放电；析出的 Ca 会被本体 Mg²⁺ 化学氧化（置换）" |
| 7 | "Ca + Mg²⁺ 置换造成 faradaic 电流效率损失" | **分类错**。该反应不损失金属总量：Ca²⁺ 回熔盐可再电解，Mg 回合金可再还原。损失的是**电压效率**（用 2.87 V 的电得到 2.37 V 的 Mg）和**脱氧深度** | 与 L597 的 (ii) back-dissolution 分开，单列为"energy penalty"而非"faradaic loss" |
| 8 | "MgO 堵塞多孔 TiO₂ 孔道导致钝化是主要钝化源" | 若 MgO 是溶解态（论文 L664 的 0.5–1.2 wt%），"固相堵塞"不成立；论文 L728 已用更准确的表述（"if the alloy blocks the pores or the layer coarsens"）作为**风险**而非**主张** | 保留论文原表述，不要升级为主张 |
| 9 | "体积膨胀 22.51 cm³ > 18.88 cm³，故 MgO 填满孔隙" | 算术对（复算 2×MgO=22.51，TiO₂=18.88，Ti=10.61，全固相膨胀 **75%**），但**推论错**：MgO 溶解后不占孔隙体积 | 改作"孔隙容量约束"用于**支撑** Eq.(amgo) 的必要性，见 §3.9 |
| 10 | "静电分选可完美分离 Ti 与 TiO₂" | 方向对，但 <10 µm 细粉静电分选效率下降；且必须先解离 | "分级 + 静电分选为主，磁选/碱洗为辅"，见 §4-D |

### 1.3 错误，必须废弃（这是本方案最重要的部分）

**✗ 论断 A：MgO "晶格能极高，在氯化物熔盐中不溶解、不解离"。**

与论文 L664 引用的实验数据直接冲突：

> Ito & Morita 测得 MgO 在 MgCl₂–CaCl₂ 中 800 °C 溶解度为 **2.35 wt%**，且随 CaCl₂ 含量增加而上升；Arrhenius 外推到 600 °C 为 **0.5–1.2 wt%**（L664、L734）。

0.5–1.2 wt% 不是"不溶"。而且论文摘要（L38）、L51、L662 的整个 closed-loop 论证，以及 `Eq.(amgo)` 里 `a_MgO` 这个符号本身，都建立在"MgO 是**溶解态**物种"之上。若 MgO 完全不溶：
- `Eq.(amgo)` 的 `a_MgO` 无从定义（固相活度为 1，则约束永远不满足）；
- Case II 的物料平衡（MgO 电解再生，Table `mbalance` 842 kg）不成立；
- 论文的 `TiO₂ → Ti + O₂` 净反应不闭合。

**处置：删掉这条，一个字都不要写进论文。**

**✗ 论断 B：Ca 还原 MgO 被"固态壳层的高传质阻力动力学阻断"，且壳层有"微裂纹"。**

三重问题：
1. 与论文图像冲突。论文认定 MgO 是溶解态（`a_MgO`），溶解态没有"壳"。
2. 逻辑不自洽，这是最要命的一点。TiO₂ 还原本身就是固–液界面反应（论文 L601、Fig. `shuttle` 的"solid TiO₂ particle"）。如果固–液界面传质能支持 100 µm 颗粒 **6.3 min 完全还原**（L754），同一个界面就不能同时"阻断"Ca + MgO。审稿人一句话就能击穿："既然阻断 MgO，为何不阻断 TiO₂？"
3. 论据本身站不住。MgO 是**原位生成的纳米/亚微米颗粒**，比表面积远大于 TiO₂ 前驱体，界面反应活性更高，不是更低。

**处置：论文现有的处理方式（承认热力学自发 → 把 camgo 界面动力学设为"未测的关键参数" → 用 Case I / Case II 双包络把结论夹住 → Limitations(10) 明确点名）已经是这个问题的最优解，不应被替换。** 这个做法的好处是：无论 camgo 快还是慢，能量结论都不变（12,552 vs 12,933，+3%）。这比"赌它被阻断"稳健一个量级。

**✗ 论断 C："MgCl₂ 是消耗品，需按化学计量定期补充。"**

与论文 Table `mbalance` 脚注 a 直接矛盾：

> "In Case I the Mg shuttles oxygen … so its **net chemical consumption is zero** and only the amount needed to offset evaporation and entrainment must be replenished."

正确口径：MgCl₂ 的补充量 = **物理损失**（freeboard 蒸发 ≈180 Pa、随渣夹带、维持合金库存的少量放空），由损失速率决定，**与钛产量无关**。论文 L433 已经指出了 Mg 必须有出口，L742 也说了。这已经够了。

若按"化学计量消耗品"写（例如"每吨钛消耗几十公斤 MgCl₂ 并需持续补盐"），会引出审稿人的致命追问："既然一直在消耗，凭什么叫 closed-loop？"——而这个追问本来是不存在的。

### 1.4 论文已有、但值得加强的两处

- **L597 的 η 损失机制**：已列 (i) 电子导电 (ii) back-dissolution (iii) Na 共析 (iv) 杂质副反应。缺"Ca + Mg²⁺ 置换"这一条，且该条性质不同（非法拉第损失），补上能显著提高机理精度，见 §3.7。
- **L662–664 的溶解度论证**：已经很好。可加一句"MgO 溶解度低是设计**要求**而非**障碍**"，把弱点转成约束（论文 L343 其实已说 "not merely tolerable but required"），只需在 L662 再点一次。

### 1.5 数值复核结果

| 项目 | 讨论/论文中的值 | 我的复算 | 结论 |
|---|---|---|---|
| ΔG_f(MgO, 873 K) | 隐含 −507.5 kJ/mol | −507.5 | ✅ 一致（Barin ≈ −506） |
| ΔG_f(CaO, 873 K) | 隐含 −545.7 kJ/mol | −545.7 | ✅ 一致（Barin ≈ −546） |
| K₂ (camgo) | 194 | 192.9 | ✅ |
| Eq.(amgo) 右端 | 5×10⁻³ | 5.17×10⁻³ | ✅ **但必须用 w=7.7×10⁻³ wt%，不能用 77** |
| 100 µm Ti 沉降速度 | 论文未给 | 4.9 mm/s（Re=0.30），20 cm 熔池 **41 s** | ⚠ 论文 L138/L601 的"suspended"需修正 |
| 全固相体积膨胀 | 未给 | +75% | ⚠ 仅在"MgO 局部过饱和"语境下可用 |
| L138 夹带盐 1 µm 膜 | 9.6 wt%(25 µm) / 1.2 wt%(100 µm) | 11.4 / 2.9 wt% | ⚠ **比例 8× 不符合 1/d 标度（应为 4×），建议复核** |

**关于 Eq.(amgo) 的量纲（重要，建议加脚注）**：`a_MgO < (K₁/K₂)·w_[O]·a_Mg`。代入时 `w_[O]` 必须以 **wt% 的数值**（77 ppm → 7.7×10⁻³）进入，才能得到 5×10⁻³。若审稿人按"ppm"直接代入 77，会算出 5.2，然后判定论文错了 1000 倍。**这不是论文的错，是符号约定的坑**（Nomenclature 里 `w_[O]` 已定义为 wt%），但值得用一句脚注堵住。

---

## 2. 论文的真实缺口（R3 没提，但新审稿人一定会问）

这五条是我读完原文后认为比"MgO 溶不溶"更危险的问题，因为它们**动摇的是工艺能否运行的物理前提**，而不是某个参数取值。

### G1 产物"悬浮"与密度矛盾（L138、L601）

L138：`"The product is Ti powder suspended in the melt rather than a coherent cathode deposit"`
L601：`"contact and reduce suspended TiO2 particles"`

但 ρ(Ti)=4.51、ρ(melt)=1.8 g/cm³。Stokes 沉降（r=50 µm，μ=3 mPa·s）：**v=4.9 mm/s，Re=0.30，20 cm 熔池 41 秒沉底**。

"温和循环维持悬浮"需要上升流速 >5 mm/s；而足以悬浮 100 µm 金属粉的强循环，必然把导电 Ti 粉带进阳极区（短路 + 阳极氧化 + 价态循环电流损失，正是 L694–696 自己警告的机制）。**论文不能同时要"悬浮"和"温和循环"。**

### G2 还原剂接触路径未定义（Fig. `shuttle`）

Fig. `shuttle` 的 caption 写 `"a TiO2 particle suspended in the liquid Mg–Ca alloy"`，即假定存在一个液态合金浴。但 ρ(Mg–Ca 共晶)≈1.6 g/cm³ **轻于熔盐 1.8**，合金会上浮，不会形成托住 4.23 g/cm³ 颗粒的"浴"。

论文没有回答：**Ca/Mg 究竟怎么到达颗粒表面？** 三条可能路径（必须择一为主、并说明另外两条并联）：
- (a) 颗粒与阴极电接触形成导电床，合金在床内**原位析出**并被毛细保持；
- (b) Ca 溶于 CaCl₂ 熔盐（Ca 金属在 CaCl₂ 中有可观溶解度），经液相扩散到颗粒表面（即论文已引的 Okabe **EMR** 机制，L47）；
- (c) 合金以液滴乳状分散，靠循环流输运。

**(a) 与"坩埚作阴极 + 底部排料"完全契合，建议作为主线**，见 §3.10。

### G3 `screening` 无法分离同粒径的 Ti 与 TiO₂（L138）

L138 写 `"counter-current washing, drying and screening suffice"`。

问题：产物**继承前驱体粒径**（形貌遗传，论文 L138 自己说 25–100 µm）。Ti 与未反应 TiO₂ **粒径相同**，筛分按粒径分离，对同粒径的两相**无效**。筛分只能分离"反应完全的小颗粒"与"未反应的大颗粒"这种粒径差异，不能分离同粒径的 Ti/TiO₂。

必须引入按**导电性**分离的手段（静电分选），这是后处理链的必需环节，不是可选项。

### G4 全篇没有产物排出机制

L136 只写"single sealed vessel … gentle circulation"，L138 只写水洗分离。**没有任何一句说明固体产物如何从 600 °C 密封槽中连续/半连续取出**，也没说堆积高度如何控制。

这是 R1 的"工程流程图"意见的真正诉求，也是"钛粉堆积→短路"风险的根源。补"倾斜底 + 隔离阀 + 定期排料 + 连续喂料"即可闭环。

### G5 "Ca + Mg²⁺ 置换"被归入法拉第损失（L597 的 (ii)）

L597 的 (ii) 是 `"chemical back-dissolution of freshly deposited Mg/Ca by dissolved oxide species (5–10%)"`——这是**金属被 O²⁻/氧化物氧化**，是真正的法拉第损失。

但 `Ca + Mg²⁺ → Ca²⁺ + Mg` 是**置换**：金属总量不变，Ca²⁺ 可再电解、Mg 可再还原。它不损失法拉第效率，损失的是**电压效率**与**脱氧深度**。把两者混为一谈，会被审稿人指出"你把一个不损失电流的反应算进了电流效率"。分开写，机理精度立刻上一个档次。

---

## 3. 逐节修改指令（带行号）

### 3.1 L123 流程描述：加"连续进料 + 半连续排料"

**原文**（末尾）：`"In a continuously operated cell these four processes proceed concurrently in the same vessel; the numbering expresses the functional charge and material flow, not a temporal sequence."`

**改为**：

```
In an operating cell these four processes proceed concurrently in the same vessel; the
numbering expresses the functional charge and material flow, not a temporal sequence.
The feed (TiO2 powder) and the electrolysis are continuous, whereas the solids are not:
because both the Ti product and the unreacted oxide settle, the cell is operated
semi-continuously, with the settled bed drained periodically through a bottom isolation
valve while fresh TiO2 is fed to the bed surface (Reactor Configuration section).
```

### 3.2 L136 反应器概念：替换整段

**原文**：`"\textbf{Reactor concept.} The cell is a single sealed vessel at 600 °C under dry argon, with TiO2 particles suspended by gentle circulation."`

**改为**（保留后面关于极距 0.9 V 与 Mg 蒸气压的两句，只替换开头）：

```
\textbf{Reactor concept.} The cell is a single sealed vessel at 600 \textdegree C under dry
argon. Because liquid Ti is 2.5 times denser than the melt---a 100 \mu m particle settles at
\approx 5 mm/s (Stokes, Re \approx 0.3), traversing a 20 cm melt in under a minute---the
product cannot be held in suspension by mild circulation, and circulation vigorous enough to
suspend it would carry conductive Ti powder into the anode region. The cell is therefore
configured so that reaction, current collection and product accumulation share one location:
the crucible floor (or a conductive liner) serves as the cathode, the settled TiO2 forms a
conductive bed that extends the cathode into the particle assembly, and the reductant is
electrodeposited within that bed, where it is retained by capillarity rather than by gravity
(the Mg--Ca alloy, \approx 1.6 g/cm3, is lighter than the 1.8 g/cm3 melt and would otherwise
float). The inert anode is suspended in the clear melt above and enclosed in a shroud that
prevents the bed, or solids entrained by gas evolution, from bridging the interelectrode gap.
```

> ⚠ 这段改了论文的物理图像（悬浮→沉降床）。**必须同时改 L138 和 L601**，否则自相矛盾。若不愿改图像，替代方案是明确写"强制循环 + 底部锥形收集 + 循环强度上限由阳极短路判据约束"，但这需要额外算循环功率，工作量更大。**建议采用沉降床方案。**

### 3.3 L138 产物回收：替换整段

**原文**：`"\textbf{Product recovery.} The product is Ti powder suspended in the melt rather than a coherent cathode deposit, so recovery is a solid--liquid separation. A 1 μm salt film on 25--100 μm powder corresponds to 9.6 wt% (25 μm) down to 1.2 wt% (100 μm) of entrained salt; … counter-current washing, drying and screening suffice, at of order 0.2--1 m3 of wash water per ton Ti."`

**改为**：

```
\textbf{Product recovery.} The product is a porous Ti powder that inherits the external
dimensions of the 25--100 \mu m precursor, so recovery is a solid--liquid separation followed
by a dry solid--solid separation. A 1 \mu m salt film on 25--100 \mu m powder corresponds to
\approx 11 wt\% (25 \mu m) down to \approx 3 wt\% (100 \mu m) of entrained salt [复核值，原
9.6/1.2 wt\% 的比例不符合 1/d 标度]; as CaCl2 and MgCl2 are highly water-soluble,
counter-current washing and drying remove the salt at of order 0.2--1 m3 of wash water per
ton Ti. The washed powder is, however, a mixture of metallic Ti and unreacted TiO2 of
essentially the same particle size, so screening alone cannot separate them; it is retained
only to recycle the coarsest, least-reacted particles. Separation of Ti from TiO2 relies on
the property that differs most---metallic Ti is an electronic conductor and TiO2 is an
insulator---and is performed by dry electrostatic separation, preceded by gentle
ultrasonic or gas-jet liberation of the friable Ti shell from the unreacted core (milling is
excluded: it would oxidise the product and destroy the size contrast). The separated oxide
fraction is returned to the cell as feedstock rather than discarded, and all dry steps are
enclosed under argon.
```

### 3.4 L161 表格：`Cyclic (conceptual)` → `Semi-continuous (conceptual)`

Proposed 行 Mode 一栏改为 `Semi-cont. (conceptual)`，与 L123/L136 的新表述一致，也与 L159 SOM 的表述风格统一。

### 3.5 L341 加量纲脚注（防审稿人踩坑）

在 Eq.(amgo) 后加：

```
\par\footnotesize Here $w_{[\mathrm{O}]}$ is expressed in wt\% \emph{as a numerical value}
(77 ppm $\rightarrow 7.7\times10^{-3}$), consistent with the Nomenclature definition and with
the 1~wt\% Henry's-law standard state used in Eq.~\ref{eq:deox}; substituting 77 directly
would inflate the bound by $10^{4}$.
```

### 3.6 L433 Mg 库存：补一句与补充盐的联动

**在** `"This inventory balance is an additional design constraint that the present conceptual study does not resolve (Limitations(10))."` **之前插入**：

```
The corresponding MgCl2 makeup stream is therefore sized by these physical losses---the
freeboard evaporation, the entrainment in the drained bed and a small inventory bleed---and
not by the titanium production rate: in the Ca-only limit the net chemical consumption of Mg
is zero (Table~\ref{tab:mbalance}, note a), since reaction~\ref{eq:camgo} restores it.
```

### 3.7 L597 η 损失机制：加入置换项并区分性质

**原文**：`"The expected loss mechanisms are (i) electronic conduction in the melt (2--5%), (ii) chemical back-dissolution of freshly deposited Mg/Ca by dissolved oxide species (5--10%), (iii) Na co-deposition at high current density (3--8%), and (iv) impurity side reactions (2--5%)"`

**改为**：

```
The expected faradaic loss mechanisms are (i) electronic conduction in the melt (2--5\%),
(ii) chemical back-dissolution of freshly deposited Mg/Ca by dissolved oxide species
(5--10\%), (iii) Na co-deposition at high current density (3--8\%), and (iv) impurity side
reactions (2--5\%). A fifth channel is of a different nature and is deliberately excluded
from the faradaic budget: the displacement `Ca + Mg2+ -> Ca2+ + Mg` conserves both metals
(Ca2+ returns to the melt and Mg to the alloy), so it costs voltage efficiency rather than
charge---a charge passed at the Ca deposition potential yields Mg---and it lowers the
attainable deoxidation depth to the Mg-only endpoint of 3908~ppm. Its signature scales with
the Mg2+ concentration in the boundary layer rather than with the dissolved-oxide activity,
so the two channels can be separated experimentally by comparing the measured current
efficiency with the measured Ca:Mg ratio of the deposit.
```

### 3.8 L601 Hall–Héroult 类比末句：与 §3.2 对齐

**原文末尾**：`"…requires the co-deposited Mg–Ca alloy to contact and reduce suspended TiO2 particles—an additional liquid–solid reaction step…"`

`"suspended TiO2 particles"` → `"TiO2 particles settled in the cathodic bed"`。

### 3.9 新增小节 A（放在 `Reduction Thermodynamics` 之后）：固相脱氧 + 孔隙容量

这一节做两件事：(1) 明确"不是钛离子液相沉积"，堵住最常见的误读；(2) 把讨论中算对的"体积膨胀"改造成**支撑 Eq.(amgo)** 的定量论证，而不是"堵孔钝化"主张。

```latex
\subsection*{Solid-State Deoxygenation and the Pore-Volume Constraint on \texorpdfstring{$a_{\ce{MgO}}$}{aMgO}}

Because $\ce{TiO2}$ is insoluble in the quaternary chloride melt, the reduction is not an
electrochemical deposition of dissolved titanium ions but a solid-state deoxygenation at a
liquid-metal/oxide interface. The reductant is delivered to the particle as a liquid Mg--Ca
phase, oxygen is stripped from the oxide lattice as $\ce{O^{2-}}$ and transferred to the
melt, and the metallic Ti remains in place, inheriting the external dimensions of the
precursor while developing an internal pore network. Two consequences follow. First, the
product is necessarily a porous powder rather than a dense deposit, which is why recovery is
a powder-handling problem (Product recovery). Second, the rate-limiting step is interfacial
deoxygenation coupled to transport through the product layer---the quantity the SCM
analysis models---rather than solution-phase mass transfer, which is why the FFC analogy for
current efficiency (L597) applies to the electrolysis step only and not to the reduction step.

The same picture supplies an independent, geometric justification for the
$a_{\ce{MgO}} \lesssim 5\times10^{-3}$ requirement of Eq.~\ref{eq:amgo}. Per mole of Ti, the
solid volumes are 18.9~cm$^3$ ($\ce{TiO2}$), 10.6~cm$^3$ (Ti) and 22.5~cm$^3$ (2~mol MgO):
if the MgO formed by Mg reduction were retained as a solid within the particle, the solid
volume would grow by $\approx$75\%, and the pore network that admits the liquid reductant
would be filled long before the reaction reached the core. The designed route avoids this not
by preventing MgO formation---which the thermodynamics of Eq.~\ref{eq:camgo} do not
permit---but by keeping the dissolved MgO activity low enough that MgO leaves the reaction
zone as it forms. The geometric bound and the thermodynamic bound therefore coincide, and
both point to the same requirement: the MgO removal rate, by dissolution and electrolytic
regeneration, must match its formation rate.
```

> 这段的好处：把讨论里那条**错的**"体积膨胀堵孔钝化"论证，转成了**对的**"孔隙容量约束"，并且用来支撑论文已有的 Eq.(amgo)，而不是替换它。审稿人看到的是"作者自己做了交叉验证"，不是"作者在找借口"。

### 3.10 新增小节 B（放在 `Process Description` 之内，紧跟 `Product recovery`）：反应器与半连续操作

```latex
\subsection*{Reactor Configuration and Semi-Continuous Operation}

Three constraints fix the cell architecture: the density contrast that makes the product
settle, the need to keep the reductant in contact with the particles, and the requirement
that conductive solids never bridge the interelectrode gap. They are met simultaneously by a
crucible-as-cathode configuration in which the sloped cell floor, or a conductive liner
embedded in it, is the cathode; the settled $\ce{TiO2}$ forms a bed that extends the cathode
into the particle assembly; and the Mg--Ca alloy is electrodeposited within that bed, where
capillarity retains it against buoyancy. The reductant therefore reaches the particles by
in-situ deposition rather than by gravity settling, and the bed itself is the reaction zone.
A parallel, chemically equivalent path exists in which dissolved Ca reduces the particles
through the melt (the electronically mediated mechanism of Okabe et al.), and the two are
not distinguished by the present thermodynamic analysis.

The anode is suspended in the clear melt above the bed and enclosed in a porous ceramic
shroud whose function is geometric rather than electrochemical: it prevents the bed, or
solids entrained by anodic gas evolution, from bridging the gap at the maximum permitted bed
height. The shroud material must survive prolonged exposure to a 620~\textdegree C chloride
melt containing dissolved oxides; candidate materials (yttria-stabilised zirconia,
magnesia-based ceramics) are identified as a screening task rather than a settled choice, and
the shroud is presented as a proposed design element to mitigate soft short-circuiting, not
as a demonstrated component.

Operation is semi-continuous. Electrolysis and $\ce{TiO2}$ feeding are continuous; the solids
are not. The bed height must stay below the shroud, so the sloped floor terminates in an
isolation valve through which the slurry is drained periodically into a sealed, argon-blanketed
receiver, and the drained mass is replaced by fresh $\ce{TiO2}$ fed to the bed surface, holding
bed height, interelectrode gap and melt level constant. Start-up follows the reverse logic: the
salts are vacuum-dehydrated and melted, electrolysis is started in the absence of solids to
establish the reductant inventory, and particulate $\ce{TiO2}$ is admitted only once a stable
liquid reductant phase exists---admitting an insulating oxide beforehand gives no reduction and
risks blocking the current path.
```

> ⚠ 小节 B 依赖 §3.3 的"沉降"图像。三处（L123/L136/L138/L601）必须一起改，否则前后矛盾。

### 3.10b 修正：坩埚作阴极的尺度分析（重要）

"坩埚作阴极"（crucible-as-cathode）必须拆成两件不同的事，混为一谈会在工业规模上自毁：

- **(a) 坩埚作为集流体与收集器**（current collector + container）： Ti 粉沉在锅底，天然与阴极电接触，松散导电粉末的接电问题被消除。**有优势，应采纳。**
- **(b) 坩埚壁作为主要反应阴极面**（cathode surface）： 与 1.1 cm 欧姆预算不兼容。**应放弃主面地位。**

几何论证。设圆柱槽内径 $D$、阳极同轴、直径 $d$，则极距 $L=(D-d)/2$。要把 $L$ 压到 1.1 cm，阳极直径必须只比槽径小 2.2 cm。以 1000 t/年（$I\approx2.56\times10^5$ A，$j=1.1$ A/cm$^2$，$A_c\approx23$ m$^2$）计：

| 配置 | 阳极尺寸 | 结果 |
|---|---|---|
| 中心棒阳极 + 坩埚壁阴极 | $d\gtrsim3.58$ m（槽径 3.6 m） | 退化为 1.1 cm 环形窄缝：气体沿 3.6 m 周长排不出（气袋）、阳极电流密度 1.1 A/cm²（惰性阳极通常 <0.5）、阳极盖住整个截面**无法排料**。三重不可行。 |
| 水平大板阳极 + 底部床阴极 | 圆板 $\approx3.6$ m，悬于床面上方 1.1 cm，四周留气体上升通道 | **可行**。电流走垂直短路径，气体从板边上升，床可经侧下方排料口排出。 |

结论：能同时满足 1.1 cm 与 23 m² 的，是**"床电极 + 平行板阳极"**，不是"锅壁 + 中心棒"。这与论文 L442 已给出的 "close-spaced or diaphragm-integrated" 一致。

**建议的写法（区分尺度，既采纳又不挖坑）**：

```latex
The cathode is the settled bed itself, electrically continuous through the crucible floor
and wall. In a laboratory or pilot cell this makes the crucible the cathode in the literal
sense, which is convenient: the powder is wetted by the current path without any separate
current collector. At production scale the geometry cannot remain a crucible-with-central-
anode, because the ohmic budget of L < 1.1 cm (Fig. current_regimes b) would require an
anode almost as wide as the cell, leaving no path for anodic gas and no access for drainage.
The production configuration is therefore a horizontal plate anode suspended ~1 cm above the
bed, with the gas escaping laterally past the plate edges and the crucible acting as
container and current collector rather than as the principal cathode surface.
```

**附带一条论文遗漏的效应**：$j=1.1$ A/cm²、$1000$ t/年时，$\ce{O2}$ 体积流量 $\approx47$ L/s；1.1 cm 间隙内气体体积分数约 2%，Bruggeman 修正使有效电导率下降 3--5%（$0.86\to0.89$ V），**不致命但应计入**。真正的风险是局部气袋，而非整体气泡分数。建议在 L442 后加一句限定，并在 Limitations(11) 提一句。



```latex
(11) \textbf{Reactor engineering}: The crucible-as-cathode configuration, the ceramic anode
shroud and the periodic drainage of a 620~\textdegree C slurry are conceptual. The long-term
corrosion and salt-permeation resistance of candidate shroud ceramics in the quaternary melt
are unquantified; failure of the shroud would re-open the soft-short-circuit path that the
settled, electronically conductive Ti bed creates. Sealing and freeze-off of the bottom
isolation valve, and the heat loss associated with periodic drainage, are not itemised in
Table~\ref{tab:heatbal}.

(12) \textbf{Product separation chain}: The electrostatic separation of Ti from unreacted
$\ce{TiO2}$, the liberation step that precedes it, and the magnetic/alkaline removal of
reduced Fe and Si are standard unit operations but are not quantified here, and the
efficiency of electrostatic separation for particles below $\sim$10~$\mu$m is not
established. The 300~kWh/ton post-treatment figure covers washing, drying and screening only
and is distinct from these steps (see also Limitations~(7)).
```

### 3.12 Conclusions 微调

- (1) 保持，但在 `"provided the dissolved MgO activity is held below ≈5×10⁻³"` 后加 `"，which is a requirement on the MgO removal rate rather than on its solubility"`。
- 新增一条 (10)：

```latex
(10) The cell is configured as a semi-continuous crucible-as-cathode reactor: a settled
$\ce{TiO2}$ bed on a sloped floor, reductant electrodeposited within the bed, an anode in the
clear melt above enclosed in a ceramic shroud, and periodic drainage of the Ti/MgO/CaO slurry
through a bottom isolation valve while fresh $\ce{TiO2}$ is fed to the bed surface. Screening
alone cannot separate the Ti product from unreacted $\ce{TiO2}$ of the same particle size;
dry electrostatic separation, exploiting the conductivity contrast, is the proposed primary
step, with the oxide fraction returned to the cell.
```

---

## 4. 可直接粘贴的英文段落（备选/复用）

以下是 §3 各段的独立版本，便于放进 response letter 或按需插入正文。

**A. 固相脱氧本质**
> Because TiO2 is insoluble in the chloride melt, the reduction is not a deposition of dissolved titanium ions but a solid-state deoxygenation at a liquid-metal/oxide interface: the reductant is delivered as a liquid Mg–Ca phase, oxygen leaves the lattice as O²⁻ and enters the melt, and the metal remains in place, inheriting the precursor's dimensions while developing internal porosity. The rate-limiting step is therefore interfacial deoxygenation coupled to product-layer transport—what the SCM models—and not solution-phase mass transfer.

**B. 反应器与接触路径**
> The density contrast fixes the architecture. A 100 µm Ti particle settles at ≈5 mm/s (Stokes, Re≈0.3) through a 20 cm melt in under a minute, while the Mg–Ca alloy (≈1.6 g/cm³) is lighter than the melt (1.8 g/cm³) and would float. A design relying on particles suspended in the alloy is therefore unsustainable, and circulation strong enough to suspend them would carry conductive Ti into the anode region. Instead, the crucible floor serves as the cathode, the settled TiO2 forms a conductive bed that extends the cathode into the particle assembly, and the alloy is electrodeposited within the bed and retained there by capillarity. A chemically equivalent parallel path—dissolved Ca reducing the particles through the melt (the electronically mediated mechanism)—is not distinguished by the present thermodynamic treatment.

**C. 半连续操作与启动**
> Electrolysis and TiO2 feeding are continuous; the solids are not. Because the bed accumulates both product and unreacted oxide and must stay below the anode shroud, the sloped floor terminates in an isolation valve through which the slurry is drained periodically into a sealed receiver, and the drained mass is replaced by fresh TiO2 fed to the bed surface. Start-up follows the reverse logic: salts are vacuum-dehydrated and melted, electrolysis establishes the reductant inventory in the absence of solids, and particulate TiO2 is admitted only once a liquid reductant phase exists.

**D. 产物分离（为什么筛分不够）**
> The washed product is a mixture of metallic Ti and unreacted TiO2 of essentially the same particle size, since the product inherits the dimensions of the precursor; size classification therefore cannot separate them and is retained only to recycle the coarsest particles. Separation relies on the property that differs most—metallic Ti is an electronic conductor and TiO2 an insulator—so dry electrostatic separation is the primary step, preceded by ultrasonic or gas-jet liberation of the friable Ti shell (milling is excluded: it would oxidise the product and destroy the size contrast). Magnetic separation removes reduced Fe where metallurgical-grade feedstock is used, and the separated oxide is returned to the cell.

**E. 置换 vs 法拉第损失**
> Two loss channels must be separated. A genuine faradaic loss arises when metal is re-oxidised by dissolved oxide species, or dissolves and is transported to the anode: charge is carried without producing reductant, and the loss appears directly in ηI. The displacement Ca + Mg²⁺ → Ca²⁺ + Mg is not of this kind: both metals are conserved, Ca²⁺ returning to the melt and Mg to the alloy. It costs voltage efficiency—a charge passed at the Ca deposition potential yields Mg—and it lowers the attainable deoxidation depth to the Mg-only endpoint of ~3900 ppm O. The two have different signatures, scaling with dissolved-oxide activity and with boundary-layer Mg²⁺ concentration respectively, and can be separated experimentally by comparing ηI with the measured Ca:Mg ratio of the deposit.

**F. MgCl₂ 是补充料，不是化学计量消耗品**
> MgCl2 is not consumed stoichiometrically. In the Ca-only limit, Mg shuttles oxygen between the particle surface and the dissolved Ca and is chemically restored by Ca + MgO → CaO + Mg, so its net chemical consumption is zero; what must be made up is the physical loss—freeboard evaporation, entrainment in the drained solids, and a small inventory bleed. The makeup stream is sized by the loss rate, not by the titanium production rate, and is closed at plant level by recovering the salt from the wash liquor.

**G. 为什么不能换成纯镁体系**（放在 Process Comparison 或 Thermodynamic Framework 均可）
> Replacing CaCl₂ with a MgCl₂-based melt would remove the stronger deoxidant and the oxide solvent at the same time. Mg alone stops at ≈3900 ppm O, an order of magnitude short of the commercial 0.10–0.20 wt% target's deeper end, and MgO solubility in these melts is markedly lower than that of CaO, so the closed loop would lose both its deoxidation depth and its dissolution capacity. The 40 mol% CaCl₂ is therefore not an inert diluent but the component that supplies both functions.

---

## 5. 回复审稿人要点

### R1（工程细节，"minor revision 即可"）
他提的 8 点里，本方案直接覆盖 6 点：流程图（已有 Fig. `flowsheet`，补半连续文字）、Ti 分离（§3.3）、盐选择理由（L123 已有三条件）、前驱体（L134）、SCM（已有）、熔点矛盾（L140 + L730 已有）。**只剩"倾析/排料"与"反应器"需要按 §3.2、§3.10 补。** R1 是最好对付的，按他的清单逐条回即可。

### R2（纯计算无实验）
**不要辩解，分三层回**：
1. 承认定位：`"This manuscript is a conceptual process design and techno-economic assessment, not an experimental report."`
2. 指出已经做了什么：`Eq.(camgo)/Eq.(cross)/Eq.(amgo)` 揭示了一个原稿未识别、文献也未讨论的**约束**（a_MgO < 5×10⁻³），并给出了 Case I / Case II 的能量包络——**这是计算能给的、实验暂时给不了的东西**。
3. 交出 Go/No-Go（L762 已有，直接引）：`η_I < 0.60 @ 4.0 V` 或 `600 °C 溶解度 < 0.5 wt%` 即放弃。
4. **最佳解**：补一个溶解度实验（§6），把 R2 从"无实验"变成"有一个针对性实验"。

### R3（核心否定，但赞深度）
R3 的原话是 `"The basic point of process design was wrong … The fundamental design was analyzed so precisely, which is amazingly deep."` 他的攻击点（Ca + MgO 自发）**论文已经承认并已经推到 Eq.(amgo)**。

回复策略：**不要辩护，要"接受并深化"**：
> "We agree, and the revision makes this reaction load-bearing rather than a caveat. Eq.(camgo) is now the basis for three derived results: the crossover identity (Eq. cross), the MgO-activity bound (Eq. amgo), and the two-case energy envelope (12,552 vs 12,933 kWh/ton, +3%). Because both limits were carried through, the energy conclusion no longer depends on the unresolved interfacial kinetics, which is now named as the single most important unmeasured input (Limitation 10). What the reviewer identifies as a design flaw is, on this reading, the mechanism that sets the design's MgO-removal requirement."

再补一句：**"我们不再主张 1:1 的氧分配是设计的必要部分"** —— 这正是 R3 实质上说的（"Mg and Ca do not coexist as the author believed"）。论文 L354 已经明确写了"哪个极限成立由动力学决定，两者能量差 3%"，所以这句话现在站得住。

### 别忘了
R3 还说"文章太长、细节冗余"。新增两节会变长，**建议同时压缩**：L597 与 L599 有重复（η 论证各说一遍），L314 与 L354 有重复。合并可省约 1 页，抵消新增 1 页。

---

## 6. 投稿策略与一个低成本实验

### 6.1 定位
- 类型：**Conceptual Process Design**（在 cover letter 里明写，不要投成 experimental research article）。
- 首选：*Journal of Sustainable Metallurgy*（scope 明确包含概念冶金流程、物料闭环、渣处理，不强制实验）。
- 次选：*Metallurgical and Materials Transactions B*（过程冶金 + 热力学计算）。
- 备选：*JOM*（主题约稿窗口受限）、*Calphad*（仅当剥离工程部分、只留相图/热力学时）。

### 6.2 一个能把 R2 死穴解掉的实验（强烈建议）

论文自己认定两个 pivotal missing measurements（L694、L758）：**600 °C 下的 CaO 溶解度** 与 **camgo 界面动力学**。

其中**第一个实验门槛极低**，1–2 周可完成，不需要电化学工作站：
1. 石墨/刚玉坩埚配 CaCl₂–MgCl₂–NaCl–KCl 四元盐（论文 L123 的组成），真空脱水；
2. 600/620 °C 下加入过量 CaO（或 MgO），密封、氩气、平衡 6–24 h；
3. 取上清盐样，冷却后水溶，ICP-OES 测 Ca/Mg；
4. 得到 600 °C 的溶解度（wt%），直接替换 L664、L734 的 Arrhenius 外推。

**这一个数据点就能把 Limitations(6) 从"外推估计"变成"实测"**，同时把 R2 的"no experimental validation"从全盘否定降级为"部分验证"。性价比极高。

（第二个实验——camgo 界面动力学——需要测 Ca 活度下的 MgO 消耗速率，难度大得多，可以老实留给 future work。）

### 6.3 不要再做的事
- ❌ 不要在正文写"MgO 完全不溶"或"动力学阻断 Ca 还原 MgO"；
- ❌ 不要把 MgCl₂ 写成"化学计量消耗品"；
- ❌ 不要引入讨论里那些没有出处的数字（Kroll 蒸馏 5000–8000 kWh/t、后处理 800–1500 kWh/t 等）。论文 L599 已有 30,000–40,000 kWh/ton（引 ji2026），L736 已有 200–500 kWh 酸洗估计，以论文为准。

---

## 7. 修改清单（照此打勾）

| # | 位置 | 动作 | 优先级 |
|---|---|---|---|
| 1 | L138 夹带盐 9.6/1.2 wt% | 复核或改为 11/3 wt%（比例应为 4× 而非 8×） | 中 |
| 2 | L123 末句 | 加"连续进料 + 半连续排料" | 高 |
| 3 | L136 反应器段 | 替换为坩埚阴极 + 沉降床 + 阳极罩 | **最高** |
| 4 | L138 产物回收段 | 替换：洗盐 + 解离 + 静电分选 + 氧化物回流 | **最高** |
| 5 | L161 表格 Mode | `Cyclic` → `Semi-cont.` | 低 |
| 6 | L341 Eq.(amgo) 后 | 加 wt% 量纲脚注 | 中 |
| 7 | L433 末 | 加"MgCl₂ 补充量由物理损失决定" | 中 |
| 8 | L597 η 机制 | 加置换项并区分 faradaic / energy penalty | 高 |
| 9 | L601 末句 | `suspended` → `settled in the cathodic bed` | 高 |
| 10 | 新小节 A（L355 后） | 固相脱氧 + 孔隙容量约束（+75%） | 高 |
| 11 | 新小节 B（L139 后） | 反应器配置与半连续操作 | **最高** |
| 12 | Limitations | 新增 (11) 反应器工程、(12) 分离链 | 高 |
| 13 | Conclusions (1) | 加"是移除速率要求而非溶解度要求" | 中 |
| 14 | Conclusions 新增 (10) | 半连续反应器 + 静电分选 | 中 |
| 15 | 全文 | 压缩 L597/L599、L314/L354 的重复 | 中 |

**三处必须同时改，否则自相矛盾**：L123、L136、L138、L601（"悬浮"→"沉降床"）。这是本次修改的唯一硬约束。

---

## 11. 执行记录（2026-xx-xx）

### 11.1 已完成

| 类别 | 内容 | 状态 |
|---|---|---|
| 脚本 | 新增 `scripts/case_baseline_mc.py`：双情形全流程热平衡 + 11 参数 Monte Carlo（同一 seed），可复现论文 Case II 的每一个数字 | ✅ |
| 脚本 | 新增 `scripts/verify_revision.py`：40 项算术与落位检查 | ✅ 40/40 |
| 输出 | `output/tab_case_baseline.csv`、`output/tab_monte_carlo_case.csv` | ✅ |
| 论文 | 新增 3 小节：Reactor Configuration（半连续/斜底/用隔离代替距离/冷启动）、Cathodic Co-Deposition 与净氧载体、Solid-State Deoxygenation 与孔隙约束 | ✅ |
| 论文 | 产物回收段重写：沉降而非悬浮、夹带盐 11/3 wt%、洗水 0.5–1.5 m³、筛分不足 → 静电分选 + 氧化物回流 | ✅ |
| 论文 | 反应器段重写：坩埚作集流体、沉降床、阳极陶瓷罩、工业尺度转平行板 | ✅ |
| 论文 | η 损失机制加第五通道（置换，能量降级而非法拉第损失） | ✅ |
| 论文 | Eq.(amgo) 加 wt% 量纲脚注；MgCl₂ 补充量口径；Limitations (11)(12)；Conclusions (10)；Table compare `Cyclic→Semi-cont.` | ✅ |
| 编译 | pdflatex 两遍，56 页，零 warning、零 undefined reference | ✅ |

### 11.2 与 §10.3 的偏离（重要）

§10.3 原计划把基准从 Case II 整体翻转到 Case I（改 ~30 处数字）。**实际执行改为"不翻转主次，但把 Case I 标为机理上更受支持"**，理由：

1. 双包络（12,552–12,933，差 3%）是本文的优点——不押注未测的界面动力学；单点翻转反而丢掉这个优点。
2. 翻转需同步改约 30 处数字，且原文 Case I 的 12,632 与 12,933 本身差 7 kWh 不自洽（已按 12,625 修正）。
3. 与已发布 Zenodo 预印本的数字保持一致，避免版本冲突。
4. "设计基准"与"机理倾向"是两个可分离的概念：以 Case II 为保守基准（假设两条电解再生路径都成立）、以 Case I 为机理倾向，逻辑上比二选一更稳。

**但脚本结果已实质进入论文**：Case I 全套热平衡（3.29 V / 7,369 / 5,679 / 6,946 / 47.3% / 35.2% / 97.3%）、Case I 的 Monte Carlo（13,536 kWh/ton；P(W<15,000)=76.6%）均已写入，并修正了 12,632→12,625 的内部矛盾。

### 11.3 未做（留给后续）

- 压缩 L597/L599 与 L314/L354 的重复（R3 的"文章太长"意见）——本次以增补为主，未删减，页数仍为 56 页。
- README.md 中的数字未同步。
- figure10/11 未重绘：两图分别标注 Case II 的 2.73 V 电压分解与 W(η,V) 等高线，Case II 仍是有效情形，无需改动。

---

## 8. V9.0 工程细节的落地文本（可直接用）

以下四段吸收 V9/V10 中**正确**的工程内容，并已按 D3/D5 修正。放在 §3.10 新增小节 B 之内或其后。

**H. 为什么用重力排料而不是抽吸泵**
> Continuous mechanical extraction of the slurry is excluded on three grounds: a 620 °C slurry of abrasive oxide and metal powder rapidly destroys pump internals; the pumping action disturbs the bed and can lift conductive Ti powder toward the anode; and a dynamic seal at the cell floor is the single most probable leak path in a sealed chloride cell. Gravity drainage through an isolation valve into a sealed receiver avoids all three, at the cost of operating in batches—which is why the process is described as semi-continuous rather than continuous.

**I. 斜底与倾角（含依据缺失声明）**
> The floor is sloped to a single drainage port so that the settled solids converge rather than spread. The slope angle cannot be fixed from first principles here: the angle of repose of Ti/MgO/CaO mixtures in a chloride melt at 620 °C has not been measured, and dry-powder values (30–45°) bracket the 45° that is sometimes proposed. A slope of ≥55° is therefore adopted as a design target, with gas-pulsed loosening at the port as a fallback, and the angle is flagged as a pilot-calibration item rather than a settled parameter.

**J. 阳极罩：用隔离代替距离**
> The interelectrode gap is fixed by the ohmic budget at L ≲ 1.1 cm, which rules out the obvious expedient of separating the anode from the bed by a large distance: at j = 1.1 A/cm² and κ = 1.4 S/cm, a 10 cm gap alone would dissipate 7.9 V, tripling the cell voltage and erasing the energy advantage over the Kroll route. Short-circuit protection must therefore be geometric rather than dimensional. The anode is enclosed in a porous ceramic shroud that the bed cannot penetrate, so that the conductive solids are excluded from the gap by a barrier rather than by distance, and the bed height is controlled by drainage frequency rather than by a fixed freeboard.

**K. 真空精炼的温度上限**
> Final deoxidation of the porous powder must be performed below the α→β transformation of titanium (882 °C), because above it self-diffusion closes the pore network and sinters the particles—destroying both the high surface area that makes the powder attractive and the particle-size contrast on which the separation chain depends. Vacuum annealing at <900 °C, calcium-vapour deoxidation, or Ar–H₂ treatment are the viable options; a 1000 °C vacuum step is not.

---

## 9. 需要撤回的具体说法（避免写进稿子）

| 不要写 | 改写成 |
|---|---|
| "MgO 不溶于氯化物熔盐" | "MgO 溶解度显著低于 CaO（2.35 wt% @800 °C，外推 0.5–1.2 wt% @600 °C）" |
| "固态 MgO 壳层动力学阻断 camgo" | "camgo 与 TiO₂ 还原的相对速率决定氧在 Mg 与 Ca 之间的分配，二者给出 Case I/II 两端" |
| "MgO 堵孔是主要钝化源" | "若 camgo 慢且 MgO 局部过饱和，孔隙可被填充；Case I 下不出现" |
| "阳极距槽底 10 cm" | "极距 ≤1.1 cm（欧姆预算）；短路靠陶瓷罩隔离；渣高靠排料频率控制" |
| "MgCl₂ 是消耗品，需按产量补充" | "MgCl₂ 补充量 ≈15–50 kg/ton-Ti，由回收率与蒸发损失决定，比 Kroll 镁耗低一个数量级" |
| "后处理 800–1500 kWh/ton" | "后处理 300 kWh/ton（洗盐+干燥+筛分）；杂质酸洗另计 200–500 kWh/ton（Limitations 7）" |
| "真空精炼 1000 °C" | "真空脱氧 <900 °C，或 Ca 蒸气/Ar–H₂" |
| "45° 漏斗" | "≥55°（设计目标，待中试标定）" |
| "Ca 优先还原 Mg²⁺" | "Mg²⁺ 优先放电；析出的 Ca 被本体 Mg²⁺ 化学氧化" |
| **"热力学上 Mg 只是氧搬运工"** | "热力学只说明 camgo 自发；**动力学**决定谁是净氧载体（论文 L354 原话）。无产物层阻力使 Case I 更可能，但不能说热力学已决定" |
| **"MgO 立即/瞬间被 Ca 吃掉"** | "该反应无产物层阻碍，故其速率不应低于 TiO₂ 界面脱氧速率"（D1）；不说"立即"，否则等于无证据宣布 Limitation(10) 已解决 |
| **"R3 确认了我们的共沉积是对的"** | "R3 否定的是 Mg 作为**独立可循环还原剂**，我们接受并已重构；他没有肯定共沉积" |
| "Mg 负责冲锋做大块还原" | "Mg 在阴极优先析出，使界面保持高还原剂活度（动力学贡献，未量化）；净氧载体是 Ca" |

---

## 10. 共沉积 vs 净氧载体：定稿表述与 Case I 迁移清单

### 10.1 裁决：这段论述哪里对、哪里不能写

| 主张 | 裁决 | 依据 |
|---|---|---|
| 要区分"阴极共沉积"与"化学净氧载体" | ✅ **对，且论文需要** | 论文 L331 已写 "rather than a partition of the oxygen between the two metals"，但没把"标题的 Co-Deposition 指阴极行为"讲透 |
| Case I 作基准（12,933） | ✅ **对**，与本方案 D1/D2 一致 | 见 §0.6 |
| 标题的 Co-Deposition 指阴极过程 | ✅ **对** | 应在 Abstract 或 Intro 一句点明 |
| "**热力学上** Mg 只是氧搬运工" | ❌ **错** | 论文 L354 明确：两者都热力学自发，**动力学**决定谁主导。说"热力学已决定"直接与自己论文冲突 |
| "MgO **立即/瞬间**被 Ca 消耗" | ❌ **错** | 无任何速率证据；写"立即"等于单方面宣布 Limitations(10) 解决，反而更容易被打 |
| "R3 说的是阴极一起析出，所以他没否定我们" | ❌ **误读，危险** | R3 原话是 "Coexistence of Mg and Ca does not work effectively"，否定的是**Mg 与 Ca 作为两个独立还原剂共存**，不是否定共沉积。按误读写回复信会被 R3 当众纠正 |
| "Mg 冲锋做大块还原，Ca 深度脱氧" | ⚠ **Case I 下是净无效循环** | camgo 快时，Mg 搬氧这一步净效果为零（等效 Ca 直接还原）。Mg 的真实贡献只剩：维持液态合金（物理必需）+ 阴极优先析出提高界面活度（未量化） |

**一句话**：结论采纳，论证必须换。采纳的理由是 D1（无产物层 ⇒ 速率不低于 TiO₂ 脱氧），不是"热力学已决定"，也不是"立即"。

### 10.2 可粘贴英文（定稿版，已避开三处硬伤）

```latex
\subsection*{Cathodic Co-Deposition and the Identity of the Net Oxygen Carrier}

Cathodic co-deposition and the identity of the net oxygen carrier are two distinct
questions, and the design depends on separating them. At the cathode, $\ce{Mg^{2+}}$
discharges first---its equilibrium potential is $\sim$816~mV more positive---and
$\ce{Ca^{2+}}$ joins once Mg deposition reaches its mass-transfer limit
(Fig.~\ref{fig:current_regimes}a), so the alloy is genuinely co-deposited; that
co-deposition is what supplies a liquid reductant at 600~\textdegree C, where both pure
metals are solid. The roles are not symmetric in the reduction that follows. MgO formed by
Mg reducing $\ce{TiO2}$ is thermodynamically unstable in the presence of Ca
(Eq.~\ref{eq:camgo}), and because that reaction generates no solid barrier---CaO leaves the
interface by dissolution and Mg returns to the alloy---there is no product layer to retard
it, so its rate should not be lower than that of the interfacial deoxygenation of
$\ce{TiO2}$, which must diffuse through a growing Ti layer. Under that condition Ca is the
net oxygen carrier: oxygen enters the melt as dissolved CaO and is evolved at the anode,
while Mg shuttles oxygen between the particle surface and the dissolved Ca with no net
chemical consumption (Table~\ref{tab:mbalance}, note a).

The opposite limit---MgO dissolving and being regenerated electrolytically, so that Mg and
Ca each carry about half of the oxygen---remains the bounding case and is retained because
the interfacial rate of Eq.~\ref{eq:camgo} has not been measured. The two limits differ by
3\% in net energy (12{,}933 versus 12{,}552~kWh/ton-Ti), so no conclusion of this work
depends on which applies. The Ca-dominant case is adopted as the baseline because it
requires no assumption beyond the absence of a product layer, and the 1:1 case is reported
as the upper bound. What the title's ``co-deposition'' refers to is the cathodic event, not
a partition of the oxygen between the two metals.
```

> 这段同时干了四件事：澄清标题、承认 R3 的实质、给出采纳 Case I 的机理理由、保留 Case II 作上界。**没有一个"立即"、没有一句"热力学已决定"。**

### 10.3 Case I 迁移清单（改基准是全文动作，不是改一个数）

把基准从 Case II 翻到 Case I，需要同步改 8 处，否则数字互相打架：

| # | 位置 | 改动 |
|---|---|---|
| 1 | L38 Abstract | 主值 12,552 → **12,933**；12,552 降为下界 |
| 2 | L544 Table `mbalance` caption + 两列 | Case I 变主列，Case II 变上界 |
| 3 | L565 分解电压段 | 2.73 V 改为"Case II 上界"，2.83 V 改为"基准" |
| 4 | L754 Conclusions (5) | 同上对调 |
| 5 | L756 Monte Carlo | **median 13,141 必须重跑**（中心值上移 ~3%，P(W<15,000) 会略降） |
| 6 | Table `compare` L165 脚注 a | 12,933 变主值 |
| 7 | L128 Fig. `flowsheet` caption | Case I 值放括号外 |
| 8 | L123 流程描述 | "predominantly CaO" 改为基准表述，不再说"if Ca acts as the sole net oxygen carrier" |

> ⚠ 第 5 项要重跑计算脚本（论文 L766 有仓库地址）。改基准后 Monte Carlo 的 median 和概率都要更新，**这是唯一需要重新计算而不仅是改文字的一处**。

### 10.4 保持的 Go/No-Go

Case I 作基准**不等于**宣布 camgo 已解决。Limitations(10) 应保留，并补一句判据：

```latex
If the measured interfacial rate of Eq.~\ref{eq:camgo} proves slow relative to MgO
dissolution, the 1:1 limit is recovered and the net energy rises by 3\%; this is the
criterion by which the two cases can be discriminated experimentally.
```

