这个skill属于一套基于Codex的autoresearch工具链，任务是根据`paper_blueprint`和`experiment plan`制定`coding plan`。
`paper_blueprint`和`experiment plan`中会包含组成一篇论文所需的实验信息，例如要实现的系统、要做的实验、候选methods、baseline、要测的数据和指标等。
这个skill需要根据已有实验信息规划如何用代码实现整个实验体系。
这个skill只制定`coding plan`，不具体写代码；后续会有专门的写代码skill负责代码实现。
`coding plan`应尽可能详细，尤其要把模块划分清楚，为后续写代码skill提供坚实基础。

`coding_plan.md`固定使用英文输出，`coding_plan.explain.md`固定使用中文输出。
中文解释中可以自然保留必要的英文仓库名、方法名、数据集、benchmark、metric、文件路径、命令和代码标识符。
中英混排应自然：中文解释以中文句子为主体，英文术语、路径、命令和代码标识符在保留原文更准确时直接保留，并保持命名一致。

`coding_plan.md`和`coding_plan.explain.md`都是Markdown格式。
`coding_plan.md`里只放`coding plan`，`coding_plan.explain.md`里只放`coding plan`解释，skill中要明确两个文件的内容边界。

已有的deepresearch MCP工具来自`academic_army_mcp_tools`，本质是把prompt通过OpenAI API转发给带web search能力的GPT-5.5。
可以现场搜索得到的信息不需要硬编码保存在skill里。
在开始制定`coding plan`之前，应先用`academic_army_mcp_tools`中的deepresearch调研相关代码通常如何组织。
deepresearch调研代码结构时应优先参考高度工程化的代码库，不要从质量较差的代码库中学习结构。
skill应现场分析相关高质量代码库的设计思路、代码结构和优秀模式，再据此组织当前项目的代码计划。
调研对象不应在skill里被提前写死，可以包括相关领域代码库、benchmark框架、实验框架、evaluation harness、配置系统、实验记录工具、开源论文代码和工程化研究项目。

`coding plan`需要考虑`paper_blueprint`和`experiment plan`中提到的候选methods和baselines在代码库中的位置。
候选methods、baselines等可选内容应尽量对应到代码库中可替换的模块结构。
`coding plan`应说明哪些模块承载可替换method，哪些模块承载baseline，哪些模块承载共享流程。
对复杂实验，`coding plan`应设计多个阶段，而不是把所有流程混在一起。
每个实验阶段应尽量设计成可以一键调用的命令。
同一套实验流程应能通过不同命令行参数在不同数据上运行，并输出对应实验结果。

`coding plan`除了划分系统功能模块，还需要明确区分两类执行结构：`harness structure`和`testing structure`。
`harness structure`服务论文实验目标，回答“某个module change、method variant或optimization是否帮助达成论文目标指标”。
`testing structure`服务功能正确性，回答“代码的数据处理、接口、配置、metric计算、结果导出和CLI入口是否按预期工作”。
这两类结构都需要在`coding_plan.md`中单独成节规划，并在`coding_plan.explain.md`中解释它们如何承接`paper_blueprint`和`experiment plan`。

`harness structure`不是泛泛的单元测试或回归测试，而是面向论文优化目标的可执行评测结构。
skill应吸收传统test harness中stubs、drivers、test data、execution tools等受控执行环境思想，也应吸收OpenAI Evals、EleutherAI lm-evaluation-harness、SWE-bench等evaluation harness中输入、执行环境、评价逻辑、指标和结果记录分离的思想。
skill应使用deepresearch现场调研与当前项目相关的evaluation harness、benchmark harness、paper code、工程化实验框架和测试组织方式，再决定当前coding plan中harness的具体结构。
每个harness都应对应一个清晰的研究或实验目标；该目标应能通过运行某个命令或脚本后得到明确结果，而不是停留在“改进效果”“提升性能”这类抽象描述。
在学术论文场景中，harness目标通常对应会影响最终论文结果的性能指标，例如accuracy、latency、throughput、memory、cost、robustness、generalization、sample efficiency、quality score或领域特定metric；具体指标由`paper_blueprint`和`experiment plan`决定。
每个harness应明确它关联论文中的哪个claim、实验问题或方法选择问题，例如“选择哪个candidate method作为主方法”“某个模块改动是否提升关键metric”“某个优化是否值得进入最终系统”。
每个harness应明确要优化的目标模块、可修改范围、需要保持稳定的接口、运行入口、输入数据、评价指标、结果输出和比较方式。
候选methods和baselines应尽量映射到可替换模块结构中，使harness可以在相同输入、相同流程、相同metric下比较不同method或method variant。
当论文需要从多个候选methods中选择主方法时，harness应支持“naive method / modified method / baseline method”的可比运行方式，帮助判断哪个method在当前应用场景下经过修改后最有潜力。
harness应支持后续写代码skill反复执行“修改模块 -> 运行harness -> 读取结果 -> 再修改”的循环，因此需要稳定的命令入口、固定的输入协议、可解析的输出格式和清晰的metric定义。
每个harness应在`coding plan`中说明推荐的运行命令形式，例如通过相对路径脚本和命令行参数指定method、dataset、split、seed、config和output directory；具体命令格式由项目语言和工程结构决定。
harness应尽量固定非目标变量，例如数据切分、随机种子、评估协议、资源预算和metric计算方式，以便比较结果主要反映被修改模块的差异。
harness输出应包括最原始、最小加工的运行结果，例如per-example prediction、raw score、timing trace、resource usage、intermediate decision、error case和log metadata。
harness应明确结果文件的相对路径、文件格式和最小字段，例如method name、variant name、config id、dataset、split、seed、commit or run id、timestamp、metric values和raw artifact paths。
面向论文图表的数据聚合和转换应留给后续分析或绘图skill；harness只负责稳定运行、记录原始结果和输出可解析artifact。
对复杂实验，harness可以按阶段组织，例如data preparation、candidate method run、module-level optimization run、full-system evaluation、ablation run、stress or robustness run；阶段划分由`experiment plan`决定。
每个阶段应尽量有一键调用入口，并能通过命令行参数在不同数据、method、config或seed上复用同一套流程。
`coding plan`应说明不同harness之间的关系，例如哪些harness用于早期快速筛选，哪些harness用于最终主实验，哪些harness用于ablation或diagnostic analysis。

`testing structure`应独立于harness规划；testing关注功能正确性，harness关注研究目标、性能指标和方法筛选。
`coding plan`应把项目的功能目标具体化为一批测试脚本，使后续写代码skill在写好或改好代码后可以运行测试确认功能没有坏。
测试脚本应从功能模块出发组织，例如data loading、preprocessing、model or method interface、training or inference pipeline、metric computation、result export、configuration parsing、CLI entrypoints等；具体模块由coding plan中的系统结构决定。
每个功能测试应说明它验证什么功能、调用哪个模块或命令、使用什么最小输入、期望什么输出或行为。
testing structure应覆盖核心功能路径，而不是只测试最终实验指标；例如数据能否正确读取、method接口是否返回预期格式、metric计算是否正确、结果导出字段是否完整、命令行参数是否能正确传递。
测试脚本应尽量使用小型fixture、toy data、mock data或最小样例，保证测试运行快、失败原因清晰、适合后续写代码skill频繁调用。
测试结构可以包含不同粒度的测试，例如模块级测试、集成级测试、CLI smoke test和结果导出测试；具体粒度由项目复杂度决定。
testing structure应明确推荐的测试命令，例如运行全部测试、运行某个模块测试、运行某个CLI smoke test；pytest等工具的测试发现、fixture、setup/teardown和命令行选择机制可以作为组织测试命令的参考。
测试应有明确pass/fail标准；功能正确性测试验证代码行为、接口契约、数据格式和结果导出是否正确，不用论文性能是否达到最好作为通过标准。
当harness依赖某些关键模块时，testing structure应包含这些模块的功能测试，避免harness结果异常时无法判断是method效果不好还是代码功能错误。
testing structure应规划测试数据和真实实验数据的关系：测试数据用于快速验证功能，真实实验数据用于harness和正式实验。
testing structure应说明测试输出如何记录，例如terminal output、test report、temporary artifact或minimal log；这些输出主要服务debug，应和论文实验结果分开管理。
`coding plan`应让后续写代码skill形成基本开发循环：先通过功能测试保证模块正确，再运行harness评估模块修改对论文目标的影响。
testing structure和harness structure都应使用项目顶层目录下的相对路径，不应依赖代码仓库的绝对顶层路径。

写代码完成后，还会有更多skill根据实验结果画图和写论文，因此`coding plan`需要规划实验结果如何从系统中导出。
结果导出应尽量以对系统内部逻辑影响小的方式进行。
`coding plan`应优先规划导出最原始的数据。
不应把面向论文图表或表格的数据转换逻辑写进核心代码库内部。
`coding plan`应说明`experiment plan`中需要的实验结果如何由导出的原始数据进一步转换得到。
数据转换逻辑应作为后续分析、绘图或论文写作skill可使用的信息，而不是混入系统核心逻辑。

`coding plan`不应该知道代码仓库的顶层目录绝对路径。
`coding plan`中的所有路径都应写成相对于项目顶层目录的相对路径。

写skill时应调研AI生成文本中的defensive现象，并在编写skill时避免过度defensive。
skill应优先用正向语言严格描述它应该生成什么、服务什么目标、输出到哪里、包含哪些规划信息。
skill应减少堆叠反向限制条件，避免把输出写成大量“不要做什么”的防御性规则。
必要边界应尽量转化为正向约束，例如“本skill只输出coding plan和中文解释，代码实现交给后续skill”。
skill里包含目标、输入输出边界、规划对象和关键机制；具体学习哪些代码库、采用哪些工程模式、如何设计模块、harness structure和testing structure，应由skill通过deepresearch现场分析后决定。

`coding plan`解释文件应说明当前coding plan为什么这样组织模块、阶段、harness structure、testing structure、结果导出和相对路径。
`coding plan`解释文件应帮助用户理解该计划如何承接`paper_blueprint`和`experiment plan`，以及如何为后续写代码、功能测试、实验执行、画图和论文写作skill提供基础。
