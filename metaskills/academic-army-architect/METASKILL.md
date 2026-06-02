这个skill属于一套基于Codex的autoresearch工具链，任务是为论文生成战略层面的paper blueprint，而不是生成完整论文、实验计划、绘图计划或面向用户的建议清单。
论文蓝图主要是给后续AI规划skill读取和继承的，不是主要给人看的；因此蓝图应像一份可实施的论文战略方案，客观描述论文方案、核心信息、目标、约束和开放变量。
后续还会运行论文内容编排规划、实验规划、绘图规划等更具体的skill；本skill只负责明确能支撑后续规划的核心论文信息，不应提前细化section段落、实验表、figure layout、实现步骤或战术级选择。

skill应明确使用来自`academic_army_mcp_tools`的deepresearch工具；这个工具本质是把prompt通过OpenAI API转发给带web search能力的GPT-5.5，因此目标venue、高引论文、近期写作风格、autoresearch工具现状等动态信息应现场检索，不必硬编码进skill。

`paper_blueprint.md`和`paper_blueprint.explain.md`都是Markdown文件；`paper_blueprint.md`只包含英文论文蓝图，`paper_blueprint.explain.md`只包含中文论文蓝图解释，skill中必须明确两个文件的内容边界，避免互相混入。
`paper_blueprint.md`固定用英文输出；`paper_blueprint.explain.md`固定用中文输出，但可以自然保留英文论文标题、会议名、数据集、benchmark、method name和技术术语。
中英混排要自然：中文解释应以中文句子为主体，英文术语只在保留原名更准确、更符合领域习惯时出现，术语命名应稳定一致，避免机械翻译和反复中英文并列。

skill应调研SIGGRAPH、CVPR、SIGCOMM、NSDI等顶级会议中的高引论文，分析它们为什么优秀，并提炼问题定义、贡献定位、storytelling、证据链、实验说服力、领域影响等方面的共性模式。
skill输出的`paper_blueprint.explain.md`中应针对目标venue和相关领域分析高引论文的优点，并把这些优秀模式用于解释当前蓝图中的取舍。
分析写作手法和storytelling时，使用的论文必须较新，以反映当前审稿人偏好的叙事方式和写作风格；分析method、数据集、benchmark、baseline、技术背景时，可以使用稍早但仍有代表性的经典论文。

编写skil时应使用`academic_army_mcp_tools`里的deepresearch调研相关autoresearch工具、论文、开源代码、benchmark、agent workflow和prompt设计案例，并根据具体发现提炼对当前skill有用的设计模式。调研对象不限于相关autoresearch工具，也可以包括autoresearch论文、open-source code、agent workflow、paper-writing agent、literature-review agent、scientific discovery agent、prompt template和benchmark。

一个优秀的论文蓝图应明确论文的核心idea、核心问题、目标读者、目标venue、领域语境、审稿预期，以及为什么这个问题对该venue的读者重要。
蓝图应明确现有方法、系统、数据集、benchmark或理论框架的关键不足，并说明本文与已有工作的差异化定位。
蓝图应明确论文希望审稿人相信的1到3个核心claim，以及每个claim需要哪类证据支撑。
蓝图应明确论文的贡献形态，例如method、system、dataset、benchmark、analysis、theory、measurement、application insight等，并说明这些贡献如何共同服务核心claim。
蓝图应明确method或系统设计背后的高层逻辑，但不展开具体模块实现、参数设置、训练细节或工程步骤。
蓝图应明确实验或评估的战略目标，例如要证明有效性、泛化性、鲁棒性、效率、可解释性、实际部署价值或领域洞察，但不提前生成具体实验表格和逐项实验安排。
蓝图应明确数据集、benchmark、baseline和metric的选择原则，而不是过早固定所有战术配置。
蓝图应明确最小充分证据链，即论文至少需要哪些证据才能让核心claim成立。
蓝图应明确各部分如何共同支撑核心claim，使后续内容规划、实验规划和绘图规划都能围绕同一条认知路径展开。
蓝图应明确论文最重要的风险点和薄弱环节，但这些风险点应作为论文方案中的开放变量或后续规划重点，而不是写成面向用户的提醒。
蓝图应明确哪些信息已经由用户指定，哪些信息仍是开放变量；已经被用户明确指定的内容应被当作设计约束，而不是再次变成“需要验证的问题”。
蓝图应明确后续skill需要继承的核心约束，例如叙事目标、核心claim、证据需求、术语命名、目标venue偏好、贡献边界和读者认知路径。
蓝图应偏向战略规划，减少让用户在多个精确战术方向上做选择；当信息不足时，应先输出战略层面能确定的结构，再把真正影响合理性的未知信息标为开放变量。
可以把skill做成目标导向：先明确idea，再将idea分解为若干论文目标，然后围绕目标组织蓝图中的问题定位、贡献策略、证据策略、venue fit和后续规划约束。
蓝图中的每个目标都应服务核心claim，并能指导后续skill展开内容、实验或图表规划。
蓝图解释中应解释每个目标背后的思想、目标之间的联系，以及蓝图中的安排如何帮助论文达成这些目标。

蓝图结构采用清晰标题和局部条目，而不是复杂全局编号；每个section可以有自己的1、2、3，但不要使用C1/C2/C3/B1/B2/B3这类需要反复回看的编号系统。
推荐蓝图包含类似Core Thesis、Paper Goals、Target Venue Fit、Contribution Strategy、Evidence Strategy、Positioning Against Prior Work、Downstream Planning Constraints等战略性section。
`paper_blueprint.explain.md`的主要功能是帮助用户确认`paper_blueprint.md`中的项目是否合理，而不是解释skill流程、模板设计或工具调用过程。
解释文件应让用户理解整篇论文的核心出发点，也就是“为什么要这么写”，并说明蓝图中每个细节如何从这些出发点推导出来，从而使得用户看到不合理内容时可以通过解释文件判断是哪个核心出发点错了，还是从核心出发点推导到具体安排的中间环节错了。
解释文件应包含对论文蓝图重点内容的概括，不能只有解释；每段解释前应先复述对应蓝图正文内容，让解释文件可以相对独立阅读，不必频繁对照蓝图文件。
解释文件应按蓝图标题顺序逐条解释重要内容，说明每条蓝图内容与核心思想、其他部分、核心claim、venue偏好、证据链和后续规划之间的关系。
解释文件应避免大量跨引用编号，不要使用c1/c2/c3/b1/b2/b3式引用；section已有标题时，应优先用标题、自然简称或近义表达指代对应部分。
解释文件的写法应更像对论文方案的清晰讲解，而不是对模板字段的逐项说明；不要到处写“见第几条”“对应B2”这类需要跳转理解的表达。

解释文件开头应记录“用户已经明确的内容”，例如idea、目标venue、领域、方法方向、数据集、benchmark、技术限制、写作偏好等；这部分只放在解释文件，不放进蓝图文件。后续用户用skill修改蓝图时，“用户已经明确的内容”应持续累积，并作为之后生成和修改蓝图的设计约束。
“需要验证的问题”或“开放验证项”应与“用户已经明确的内容”联动：每次生成或修改时先检查某个问题是否已被用户明确指定，若已指定则转化为已确认约束，若未指定且确实影响蓝图合理性才保留为开放验证项。
随着用户明确的信息越来越多，开放验证项应越来越少，不能反复询问已经明确的内容。

蓝图中不应出现Artifact cautions、Do not assume reviewers will run code、Assumptions to validate这类面向用户的提醒或待办式内容。
与reproducibility、artifact、assumption相关的内容如果确实与论文方案有关，应改写成论文内部的客观设计约束、证据需求或开放变量，而不是写成用户提醒。
skill应检查输出中是否混入与论文本身无关的内容，例如用户操作建议、artifact cautions、流程解释、模板解释、工具使用理由等；这些内容应删除或改写为论文设计信息。
解释文件不应输出“为什么正式蓝图采用实施计划格式”这类skill内部决策；这类问题的根因通常是skill没有区分“内部生成流程”和“用户可见解释”。
内部流程、格式选择、工具调用、模板设计属于skill实现细节；用户可见解释只解释论文层面的设计决策及其推导关系。

skill应减少过度defensive写法，优先用正向语言描述期望输出，例如“蓝图以论文方案为对象，使用客观陈述描述已选策略和开放变量”，而不是堆叠“不要写什么”。
必要的反向限制只保留少数高风险边界；多数约束应改写为目标导向的正向要求，例如“解释文件只解释论文设计决策及其推导关系”。
skill prompt应清晰、具体、结构化，明确输入、输出文件、语言、目标、边界、动态检索策略和质量标准，减少模型自行补充无关内容的空间。
编写skill时应把目标改成“生成目标导向的论文战略蓝图”，把蓝图对象改成“供后续AI规划skill继承的论文核心信息”，把解释文件对象改成“供用户确认蓝图合理性的推导说明”。
编写skill时应加入User-specified facts累积机制、Open validation items收缩机制、文件边界规则、解释前复述蓝图内容的规则、用标题自然引用section的规则，以及“只解释论文设计，不解释skill流程”的规则。
编写skill时应删除或改写Artifact cautions、Assumptions to validate等面向用户的字段，并确保蓝图偏战略、后续skill补战术。
