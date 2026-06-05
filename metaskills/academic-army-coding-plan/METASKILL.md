这个skill属于一套基于Codex的autoresearch工具链，任务是根据`paper_blueprint`和`experiment plan`制定`coding plan`。
`paper_blueprint`和`experiment plan`中会包含组成一篇论文所需的实验信息，例如要实现的系统、要做的实验、候选methods、baseline、要测的数据和指标等。
这个skill需要根据已有实验信息规划如何用代码实现整个实验体系。
这个skill只制定`coding plan`，不具体写代码；后续会有专门的写代码skill负责代码实现。
`coding plan`应尽可能详细，尤其要把模块划分清楚，为后续写代码skill提供坚实基础。

`coding_plan.md`固定使用英文输出，`coding_plan.explain.md`固定使用中文输出。
中文解释中可以自然保留必要的英文仓库名、方法名、数据集、benchmark、metric、命令语义和代码标识符；只有在用户输入或已有项目明确给出某些现有文件路径时，才保留必要的路径事实。
中英混排应自然：中文解释以中文句子为主体，英文术语、命令语义、代码标识符和必要的既有路径事实在保留原文更准确时直接保留，并保持命名一致。

`coding_plan.md`和`coding_plan.explain.md`都是Markdown格式。
`coding_plan.md`里只放`coding plan`，`coding_plan.explain.md`里只放`coding plan`解释，skill中要明确两个文件的内容边界。

`coding_plan.md`和`coding_plan.explain.md`都应使用自然、可读的写法，通过清晰标题、语义化名称、短段落和bullet组织内容，不应依赖复杂编号系统来维持理解。
编号只作为局部组织工具使用；只有在表达执行顺序、阶段顺序、优先级或步骤关系时，才使用编号列表。
对并列模块、候选method、baseline、harness、测试类别、结果artifact等内容，应优先使用标题、短段落和bullet，而不是强行编号。
每个section内部可以使用自己的局部`1、2、3`，但这些编号只服务当前section内部的阅读，不应扩展成跨section或跨文件的引用系统。
`coding_plan.md`和`coding_plan.explain.md`都应避免使用`C1/C2/C3/B1/B2/B3/H1/H2/T1/T2`这类抽象编号系统，因为这种编号会迫使读者反复跳转查找含义。
如果需要跨部分引用，应优先使用section标题、逻辑模块名、harness名称、测试类别、method名称、artifact类型或自然简称，而不是抽象编号。
`coding_plan.explain.md`应优先用自然简称指代蓝图内容，例如“method替换模块”“candidate筛选harness”“result export layer”“CLI smoke tests”等表达，而不是写“见H2”“对应T3”。
`coding_plan.explain.md`解释某个设计时，应先简要复述或概括对应的`coding_plan.md`内容，再说明为什么这样设计，减少用户对照两个文件来回查找的成本。
`coding_plan.explain.md`可以按`coding_plan.md`的主要标题顺序解释，但解释文字应像自然说明文，而不是模板字段说明或编号索引表。
如果多个内容之间有紧密关系，解释文件应直接用自然语言说明关系，例如“candidate筛选harness依赖method替换模块提供统一接口”，而不是写“C2依赖M1并服务H3”。
`coding plan`中的命名应尽量语义化：逻辑模块名、harness名、测试类别名和artifact类型名本身应能表达用途，减少额外编号解释的需要。
harness结构可以用有意义的名称组织，例如`Candidate Method Selection Harness`、`Module Optimization Harness`、`Full-System Evaluation Harness`，而不是`Harness H1/H2/H3`。
testing结构可以用功能目标命名，例如`Data Loading Tests`、`Metric Computation Tests`、`Result Export Tests`、`CLI Smoke Tests`，而不是`Test T1/T2/T3`。
对复杂实验阶段，可以在某个section内部使用局部阶段编号，例如`1. Data preparation`、`2. Candidate run`、`3. Evaluation export`，但不要把这些编号变成全局交叉引用系统。
如果某个编号只是在生成过程中方便模型组织思路，但不提升最终读者理解，最终输出时应改写为标题、bullet或自然段落。
skill应在输出前检查是否存在过度编号、抽象编号引用、跨文件编号依赖或需要反复跳转才能理解的表达，并将其改写为自然标题和语义化名称。
核心原则是：编号可以帮助表达顺序，但不应成为理解`coding plan`的主要机制；`coding_plan.md`和`coding_plan.explain.md`都应靠清晰标题、语义化名称和自然引用来保持可读性。
coding plan skill只沉淀“如何把论文蓝图和实验计划转化为代码规划”的领域方法；工具调用、文件访问、沙盒权限、fallback路径和运行故障恢复属于外层runtime/orchestrator，不进入skill，也不进入`coding_plan.md`或`coding_plan.explain.md`。

skill应采用“最小任务上下文”策略：本地任务输入只来自`paper_blueprint`和`experiment plan`；开始时先根据用户路径、约定文件名或明确语义匹配定位这两个文件，确认后只读取这两个文件。
定位输入的文件识别只服务于确认必要输入，不扩展为当前目录、子目录、历史计划、日志、README、草稿、运行输出、旧`coding_plan`或其他中间产物的探索；如果多个候选同时存在，优先选择用户显式指定、命名最匹配或语义最直接相关的文件。
当前目录其他内容只有在`paper_blueprint`或`experiment plan`明确引用且对`coding plan`必不可少时，才作为显式依赖处理；缺失的通用工程模式、harness思想或外部经验应通过deepresearch补充，而不是从无关本地文件中猜测。
输出前做一次input hygiene检查：`coding plan`是否只依赖`paper_blueprint`、`experiment plan`和必要deepresearch结果，是否混入当前目录无关内容；如有，应移除噪声，并把真正影响计划的缺口标记为开放变量。

已有的deepresearch MCP工具来自`academic_army_mcp_tools`，本质是把prompt通过OpenAI API转发给带web search能力的GPT-5.5。
可以现场搜索得到的信息不需要硬编码保存在skill里。
在开始制定`coding plan`之前，应先用`academic_army_mcp_tools`中的deepresearch调研相关系统通常如何进行逻辑架构、组件边界、接口和实验流程设计。
deepresearch调研实现组织方式时应优先参考高度工程化的代码库，不要从质量较差的代码库中学习结构。
skill应现场分析相关高质量代码库的设计思路、逻辑组件、接口模式和实验框架模式，再据此组织当前项目的代码计划。
调研对象不应在skill里被提前写死，可以包括相关领域代码库、benchmark框架、实验框架、evaluation harness、配置系统、实验记录工具、开源论文代码和工程化研究项目。

`coding plan`需要包含充分具体的coding内容规划，但不安排具体文件路径、目录结构或文件名。
`coding plan`规划逻辑模块，而不是物理文件布局；模块可以有语义化名称、职责、输入输出、接口、依赖关系和实现要点，但不指定它们必须位于哪个路径。
后续写代码skill负责根据实际项目结构创建或修改具体文件；本skill只提供足够清晰的模块级、接口级和流程级实现计划。
如果需要描述代码组织，应使用`logical module`、`component`、`interface`、`entrypoint`、`artifact type`、`configuration concept`等抽象表达，而不是具体路径表达。
如果用户输入或已有项目明确给出了某些现有文件路径，`coding plan`可以把这些路径作为外部事实引用，但不基于它们继续扩展或发明新的文件路径。
不再要求“所有路径都写成相对于项目顶层目录的相对路径”；新的要求是“默认不安排具体路径；只有在引用用户已明确给出的现有路径时，才保留必要的相对路径信息”。

`coding plan`应把系统划分为清晰的逻辑模块，例如数据准备模块、method接口模块、candidate method适配模块、baseline适配模块、评估模块、harness执行模块、testing模块和结果导出模块；这些是逻辑职责，不是文件路径安排。
每个逻辑模块应说明它负责什么、接收什么输入、输出什么结果、依赖哪些其他模块、对后续写代码skill有什么实现要求。
可替换的candidate methods和baselines应映射到统一的逻辑接口或插件式结构，但不需要指定具体文件放置位置。
`coding plan`可以说明“需要一个统一的method registry / adapter layer / evaluation entrypoint / result export interface”这类代码设计内容，但不说明这些东西位于某个具体路径。
对复杂实验，`coding plan`应规划阶段化执行流程和命令行参数语义，例如阶段、参数、输入类型、输出artifact类型和运行结果含义；不指定具体脚本路径。

`coding plan`除了划分系统功能模块，还需要明确区分两类执行结构：`harness structure`和`testing structure`。
`harness structure`服务论文实验目标，回答“某个module change、method variant或optimization是否帮助达成论文目标指标”。
`testing structure`服务功能正确性，回答“代码的数据处理、接口、配置、metric计算、结果导出和CLI入口是否按预期工作”。
这两类结构都需要在`coding_plan.md`中单独成节规划，并在`coding_plan.explain.md`中解释它们如何承接`paper_blueprint`和`experiment plan`。

`harness structure`不是泛泛的单元测试或回归测试，而是面向论文优化目标的可执行评测结构。
skill应吸收传统test harness中stubs、drivers、test data、execution tools等受控执行环境思想，也应吸收OpenAI Evals、EleutherAI lm-evaluation-harness、SWE-bench等evaluation harness中输入、执行环境、评价逻辑、指标和结果记录分离的思想。
skill应使用deepresearch现场调研与当前项目相关的evaluation harness、benchmark harness、paper code、工程化实验框架和测试组织方式，再决定当前coding plan中harness的具体结构。
每个harness都应对应一个清晰的研究或实验目标；该目标应能通过某个可运行入口语义得到明确结果，而不是停留在“改进效果”“提升性能”这类抽象描述。
在学术论文场景中，harness目标通常对应会影响最终论文结果的性能指标，例如accuracy、latency、throughput、memory、cost、robustness、generalization、sample efficiency、quality score或领域特定metric；具体指标由`paper_blueprint`和`experiment plan`决定。
每个harness应明确它关联论文中的哪个claim、实验问题或方法选择问题，例如“选择哪个candidate method作为主方法”“某个模块改动是否提升关键metric”“某个优化是否值得进入最终系统”。
每个harness应说明目标、被修改的逻辑模块、可修改边界、运行入口语义、输入数据类型、控制变量、metric、输出artifact和比较方式。
候选methods和baselines应尽量映射到可替换模块结构中，使harness可以在相同输入、相同流程、相同metric下比较不同method或method variant。
当论文需要从多个候选methods中选择主方法时，harness应支持“naive method / modified method / baseline method”的可比运行方式，帮助判断哪个method在当前应用场景下经过修改后最有潜力。
harness应支持后续写代码skill反复执行“修改模块 -> 运行harness -> 读取结果 -> 再修改”的循环，因此需要稳定的entrypoint语义、固定的输入协议、可解析的输出格式和清晰的metric定义；具体文件组织留给写代码skill决定。
每个harness可以规划“需要一个可运行入口来执行candidate method筛选”或“需要一个可运行入口来执行module optimization评测”，并说明参数语义如何指定method、dataset、split、seed和config，但不规定这个入口对应哪个具体文件路径。
harness应尽量固定非目标变量，例如数据切分、随机种子、评估协议、资源预算和metric计算方式，以便比较结果主要反映被修改模块的差异。
harness输出应描述为artifact schema和数据字段，包括最原始、最小加工的运行结果，例如per-example prediction、raw score、timing trace、resource usage、intermediate decision、error case、log metadata、config id和metric values。
harness应明确artifact类型、数据粒度、文件格式倾向和最小字段，例如method name、variant name、config id、dataset、split、seed、commit or run id、timestamp、metric values和raw artifact references，而不是具体输出目录或文件路径。
面向论文图表的数据聚合和转换应留给后续分析或绘图skill；harness只负责稳定运行、记录原始结果和输出可解析artifact。
对复杂实验，harness可以按阶段组织，例如data preparation、candidate method run、module-level optimization run、full-system evaluation、ablation run、stress or robustness run；阶段划分由`experiment plan`决定。
每个阶段应尽量有清晰的运行入口语义，并能通过参数语义在不同数据、method、config或seed上复用同一套流程。
`coding plan`应说明不同harness之间的关系，例如哪些harness用于早期快速筛选，哪些harness用于最终主实验，哪些harness用于ablation或diagnostic analysis。

`testing structure`应独立于harness规划；testing关注功能正确性，harness关注研究目标、性能指标和方法筛选。
`coding plan`应把项目的功能目标具体化为一批测试能力，使后续写代码skill在写好或改好代码后可以运行测试确认功能没有坏。
testing structure应规划功能测试覆盖哪些逻辑模块、测试目标是什么、使用什么最小输入、期望什么行为、pass/fail标准是什么。
测试可以按功能命名，例如Data Loading Tests、Method Interface Tests、Metric Computation Tests、Result Export Tests、CLI Smoke Tests；这些名称是测试类别或测试目标，不是具体测试文件名。
每个功能测试类别应说明它验证什么功能、调用哪个逻辑模块或entrypoint语义、使用什么最小输入、期望什么输出或行为。
testing structure应覆盖核心功能路径，而不是只测试最终实验指标；例如数据能否正确读取、method接口是否返回预期格式、metric计算是否正确、结果导出字段是否完整、命令行参数是否能正确传递。
测试能力应尽量使用小型fixture、toy data、mock data或最小样例，保证测试运行快、失败原因清晰、适合后续写代码skill频繁调用。
测试结构可以包含不同粒度的测试，例如模块级测试、集成级测试、CLI smoke test和结果导出测试；具体粒度由项目复杂度决定。
testing structure可以说明需要运行“全部功能测试”“method接口测试”“结果导出测试”等测试集合；pytest等工具的测试发现、fixture、setup/teardown和命令行选择机制可以作为组织测试能力的参考，但不安排具体测试脚本路径。
测试应有明确pass/fail标准；功能正确性测试验证代码行为、接口契约、数据格式和结果导出是否正确，不用论文性能是否达到最好作为通过标准。
当harness依赖某些关键模块时，testing structure应包含这些模块的功能测试，避免harness结果异常时无法判断是method效果不好还是代码功能错误。
testing structure应规划测试数据和真实实验数据的关系：测试数据用于快速验证功能，真实实验数据用于harness和正式实验。
testing structure应说明测试输出如何记录，例如terminal output、test report、temporary artifact或minimal log；这些输出主要服务debug，应和论文实验结果分开管理。
`coding plan`应让后续写代码skill形成基本开发循环：先通过功能测试保证模块正确，再运行harness评估模块修改对论文目标的影响。
testing structure应帮助后续写代码skill知道应该实现哪些测试能力，而不是替它决定测试文件放在哪里。

写代码完成后，还会有更多skill根据实验结果画图和写论文，因此`coding plan`需要规划实验结果如何从系统中导出。
结果导出应尽量以对系统内部逻辑影响小的方式进行。
`coding plan`应规划实验结果导出的数据结构、字段、粒度和转换关系，但不安排具体输出路径。
结果导出应优先描述原始artifact类型和schema，例如raw predictions、per-sample metrics、aggregate metrics、runtime traces、error cases、configuration metadata等。
`coding plan`应优先规划导出最原始的数据。
不应把面向论文图表或表格的数据转换逻辑写进核心代码库内部。
`coding plan`应说明`experiment plan`需要的论文表格、图和统计结果如何由这些原始artifact转换得到，但不把转换逻辑绑定到具体路径或文件名。
面向论文图表的数据聚合、转换和展示逻辑应留给后续分析、绘图或论文写作skill；本skill只说明原始数据需要以什么结构导出。

**Logical design over file layout原则**：`coding plan`应规划代码实现的逻辑结构、模块职责、接口关系、执行流程、harness结构、testing结构和结果artifact schema；它不安排具体文件路径、目录结构或文件名，除非用户输入中已经明确给出某个现有路径且必须引用。
**Downstream handoff原则**：本skill负责告诉后续写代码skill“需要实现哪些代码能力、模块如何协作、harness和测试如何验证目标”；后续写代码skill负责根据实际仓库结构决定“在哪些文件中实现”。
**Path hygiene检查**：输出前检查`coding_plan.md`和`coding_plan.explain.md`是否发明了具体路径、目录树或文件名；如果有，应改写成逻辑模块名、接口名、entrypoint语义、artifact schema或测试类别。

写skill时应调研AI生成文本中的defensive现象，并在编写skill时避免过度defensive。
skill应优先用正向语言严格描述它应该生成什么、服务什么目标、输出内容边界、包含哪些规划信息。
skill应减少堆叠反向限制条件，避免把输出写成大量“不要做什么”的防御性规则。
必要边界应尽量转化为正向约束，例如“本skill只输出coding plan和中文解释，代码实现交给后续skill”。
skill里包含目标、输入输出边界、规划对象和关键机制；具体学习哪些代码库、采用哪些工程模式、如何设计模块、harness structure和testing structure，应由skill通过deepresearch现场分析后决定。

`coding plan`解释文件应说明当前coding plan为什么这样组织逻辑模块、阶段、harness structure、testing structure、结果导出和artifact schema。
`coding plan`解释文件应帮助用户理解该计划如何承接`paper_blueprint`和`experiment plan`，以及如何为后续写代码、功能测试、实验执行、画图和论文写作skill提供基础。
