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

`coding plan`除了划分系统功能模块，还需要规划harness方案。
每个harness是一个测试方案，用来指示代码中的某个优化点、对应的可修改模块、测试方法和性能指标。
harness关注的性能应与论文中真正关心的性能一致。
当论文需要从多个候选methods中选择主方法时，harness应帮助比较不同method在当前应用场景下经过修改后的潜力。
候选method不应只被naive使用；需要根据当前应用场景对现有方法进行修改，并通过harness测试修改后的效果。
不同method可能有不同优化潜力，需要通过“修改—测试”的过程判断哪个method修改后效果最好。
最终效果最好的修改后method可以作为本文主打方法，其他未修改或naive方法可以作为baseline。
harness应提供评价体系，说明什么样的结果才算“效果好”。
harness应让后续写代码skill能够围绕明确的修改范围和测试方法持续执行“修改—测试—筛选”的过程。
skill应使用deepresearch调研harness相关思想，现场分析哪些harness设计方式适合当前coding plan，而不是把某种harness模板写死。

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
skill里包含目标、输入输出边界、规划对象和关键机制；具体学习哪些代码库、采用哪些工程模式、如何设计模块和harness，应由skill通过deepresearch现场分析后决定。

`coding plan`解释文件应说明当前coding plan为什么这样组织模块、阶段、harness、结果导出和相对路径。
`coding plan`解释文件应帮助用户理解该计划如何承接`paper_blueprint`和`experiment plan`，以及如何为后续写代码、实验执行、画图和论文写作skill提供基础。
