这个skill属于一套基于Codex的autoresearch工具链，任务是根据论文蓝图、experiment plan和coding plan，在用户指定的代码仓库路径下创建一个静态、规整、可扩展的初始代码仓库骨架。
本skill已经进入“生成初始代码仓库”的阶段，不再只规划逻辑模块；它可以创建具体目录、配置、文档、代码接口、harness入口、测试入口和结果artifact约定。
本skill接收一个初始代码仓库路径作为输入，所有创建、修改和引用的项目文件都必须位于该路径之下。
代码仓库内部所有路径都应以用户输入的代码仓库路径为根，使用仓库内相对路径表达；skill不应在仓库路径之外创建、修改或引用项目文件。
如果目标仓库路径已经存在文件，skill应在保护用户已有内容的前提下进行最小必要检查，并根据任务目标创建缺失结构、补充文件或避免覆盖已有文件。

本skill的上游输入是论文蓝图、experiment plan、coding plan和用户指定的代码仓库路径；skill可以假设调用方已经提供或允许读取这些必要输入。
skill应采用input scope原则，只读取生成初始仓库所必需的输入，不主动探索当前目录下的无关文件。
如果用户明确要求基于已有代码仓库初始化或改造，skill才读取目标仓库中与初始化有关的文件；否则应把指定路径视为新仓库或待初始化目录。
当前目录中的无关文件、历史草稿、日志、旧运行结果和其他噪声不应进入仓库设计；缺失的外部工程知识应通过deepresearch调研补充。

本skill不同于`academic-army-coding-plan`：coding plan只规划代码逻辑，不安排具体路径；本skill负责把coding plan落成真实仓库骨架，因此需要安排具体文件和目录。
初始代码仓库应围绕论文蓝图、experiment plan和coding plan中定义的功能目标建立基础代码逻辑，而不是生成与论文实验无关的通用模板项目。
仓库结构应承接coding plan中的模块、harness、testing、结果导出和执行流程设计，但不需要完成具体method的最终实现。
初始仓库应包含足够的基本功能逻辑，使代码结构不是空壳；例如配置解析、数据对象定义、统一接口、adapter或registry、harness入口、测试入口、结果artifact schema和基础导出逻辑。
具体论文方法、candidate methods、baselines、custom optimization、metric实现和实验逻辑应通过清晰placeholder、extension point或统一接口预留给后续写代码skill。
placeholder应语义明确，例如method adapter placeholder、baseline placeholder、metric placeholder、data loader placeholder或harness placeholder，并说明接口契约和预期行为。
placeholder不应伪装成已经完成的算法实现；它应让后续写代码skill清楚知道哪些位置需要填充实现。

在创建仓库前，skill应使用`academic_army_mcp_tools`中的deepresearch调研现有工具、高质量代码库和相关工程实践。
deepresearch调研对象不应被写死，可以包括相关语言生态、packaging工具、实验框架、harness框架、benchmark代码库、paper code、开源科研项目、测试框架、配置系统和工程化模板。
deepresearch应优先寻找高度工程化、维护良好、结构清晰的代码库和工具，不应从质量较差的代码库中学习结构。
deepresearch应分析哪些现有工具packaging做得好、适合直接作为依赖安装调用，哪些工具packaging较差、只能在许可允许的前提下参考或复制必要代码片段。
对packaging良好、维护稳定、接口清晰的工具，应优先通过目标语言生态的标准依赖管理方式接入；对需要复制代码片段的工具，应检查license、来源和可复用条件，并在仓库中保留必要attribution或说明。
skill应把“工具选型”和“代码复制”区分清楚：可安装、维护良好、接口稳定的工具优先作为依赖；只在必要且许可允许时复制小范围代码片段或实现等价简化逻辑。
skill应记录外部工具选择理由，例如为什么某工具适合作为依赖、为什么某工具只适合参考、为什么当前框架适合该实验体系。
skill不应把deepresearch查到的某个优秀代码库结构机械照搬；应根据当前论文需求、实验流程、harness和test结构进行适配。

确定编程语言和基本框架逻辑后，skill应再次用deepresearch搜索该语言和框架的最佳实践。
语言和框架最佳实践调研应服务代码规整性，例如项目结构、dependency management、配置组织、测试组织、CLI设计、logging、typing、formatting、linting、documentation和result artifact管理。
skill不应把某一种语言、框架、包管理器、测试框架或目录模板写死；应根据论文任务、experiment plan、coding plan和deepresearch结果现场选择。
如果论文实验明显适合某种语言、运行时或生态，skill可以据此选型；如果用户已经指定语言、框架或依赖，应优先遵守用户指定内容。
公开最佳实践可以作为调研方向，例如目标生态的官方规范、测试组织文档、研究项目结构规范、静态分析资料和高质量公开库文档，但具体语言、框架和工具链必须由用户输入和deepresearch现场确定。
初始代码仓库的整体文件夹结构应结合目标语言、框架、packaging生态、论文实验需求和deepresearch找到的高质量公开库来确定，不应在skill里预先写死某一种语言或框架的目录模板。
skill应在创建仓库前用deepresearch调研目标语言和框架的最佳实践，以及相关高质量公开库的真实结构，再据此决定源码目录、配置文件、依赖声明文件、入口组织和辅助工具配置。
skill不应在tips或skill正文中提到任何具体编程语言、具体框架、具体包管理器、具体测试框架、具体目录布局案例或具体配置文件名；这些信息应由用户输入和deepresearch现场确定。
skill不应把任何目标语言、运行时或框架生态的目录布局写死；应根据deepresearch结果、用户指定、实验系统复杂度、packaging需求和后续可维护性选择合适结构。
如果用户已经指定语言、框架或项目风格，skill应优先围绕用户指定内容调研该生态的最佳实践；如果用户没有指定，则skill应根据论文蓝图、experiment plan和coding plan选择最合适的语言与框架逻辑。
deepresearch调研文件结构时应优先参考维护良好、工程化程度高、与当前任务接近的公开库，而不是随意参考小型demo、教程仓库或一次性脚本项目。
deepresearch应分析公开库中哪些结构是语言生态惯例，哪些结构是该项目特有选择，哪些结构适合当前论文实验系统，哪些结构不应迁移。
skill应避免机械照搬某个公开库的完整结构；应从多个高质量公开库和官方最佳实践中提炼适合当前论文实验系统的结构。
skill在选择代码库文件结构时，应分析该结构是否会引入不必要的配置项、额外安装步骤、额外导入设置、额外环境变量、额外测试配置或额外命令包装。
skill不应机械采用某种公开库结构；即使某种结构在高质量公开库中常见，也要判断它是否适合当前论文实验仓库的运行方式、测试方式、harness方式和后续实现方式。
对任何目标语言、运行时或框架生态，skill都应优先选择“符合该生态最佳实践且运行路径简单”的结构；最佳结构不是最复杂或最流行的结构，而是能让后续代码skill、harness、test和用户以较少配置理解和运行的结构。
skill应在deepresearch调研高质量公开库时观察：这些库的结构是否依赖复杂build配置、路径别名、module resolution、custom loader、workspace配置、test runner配置或命令包装；如果这些复杂性对当前项目没有必要，不应迁移。
如果某种目录布局、packaging方式、框架组织或工具链会让简单运行命令必须附带多个配置参数，skill应在选型时把它视为结构成本，并考虑更低摩擦的替代方案。
skill应把“减少不必要配置项”作为代码库初始化质量标准之一：默认运行、默认导入、默认测试、默认harness入口应尽量清晰，不应依赖隐藏路径假设或大量全局配置。

初始代码仓库应区分核心系统逻辑、实验执行逻辑、harness逻辑、testing逻辑和结果导出逻辑，避免把所有内容混在一个脚本里。
仓库应尽量保持模块低耦合：method实现不直接控制实验全流程，harness不直接嵌入图表逻辑，testing不依赖真实大规模实验数据。
初始仓库应为candidate methods、baselines和主方法预留统一接口，使不同方法可以在相同输入、相同评估协议和相同metric下比较。
初始仓库应为method adaptation预留空间，使后续可以在已有method基础上根据应用场景修改，而不是只能naive调用现有方法。
具体方法应通过可替换模块、统一接口、adapter、registry、config schema或配置驱动方式接入，避免把某个论文方法写死在框架里。
仓库应支持多阶段实验流程，例如data preparation、method execution、harness evaluation、full-system evaluation、ablation或result export；具体阶段由coding plan决定。
每个实验阶段的代码结构应能被后续实现扩展，而不是只服务一次固定实验。

初始代码仓库采用两层文件夹结构规则：第一层是与autoresearch论文实验强相关的固定顶层目录；第二层是语言、框架、packaging、源码布局和配置文件结构，由deepresearch现场调研最佳实践和高质量公开库后决定。
与论文实验系统强相关的顶层结构应固定保留：`data/`用于输入数据，`output/`用于运行输出，`results/`用于实验结果记录，`harness/`用于所有harness，`test/`用于所有test，`README.md`用于仓库入口说明，`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`用于框架设计与使用说明。
固定目录只规定实验系统的顶层约定，不规定语言生态内部的源码布局；源码放在哪里、package如何命名、配置文件如何组织、构建文件采用什么格式，应由deepresearch和项目选型决定。
skill应把“固定实验目录”和“生态最佳实践目录”协调起来：固定目录服务论文实验工作流，语言和框架目录服务代码可维护性、packaging、依赖管理和工程规范。
skill创建的仓库应同时满足两类要求：对外看起来符合目标语言和框架生态的工程规范，对内能清晰承接论文蓝图、experiment plan、coding plan、harness、test和结果导出需求。
`harness/`下面应为每一种harness单独设置一个子文件夹，用于放置该harness相关的入口、配置、说明、样例输入、schema或其他必要内容。
`test/`下面应为每一种test单独设置一个子文件夹，用于放置该类功能测试相关的测试脚本、fixtures、mock data、最小样例或说明内容。
harness目录和test目录应在职责上分离：harness服务论文目标、性能评估、method筛选和优化循环；test服务功能正确性、接口契约、数据格式和基础行为验证。
harness和test各自的子文件夹名称应表达用途，例如围绕候选方法筛选、模块优化、全系统评估、数据加载测试、metric计算测试、结果导出测试等语义命名；具体名称由当前项目决定。
`data/`、`output/`和`results/`的内部结构可以根据实验计划和目标生态最佳实践进一步细分，但顶层语义应保持稳定：`data/`承载输入数据，`output/`承载程序运行产生的输出artifact，`results/`承载实验结果记录和可供后续分析的数据。
如果目标语言或测试框架默认使用某个目录名，但本skill要求顶层测试目录为`test/`，skill应通过该生态支持的配置方式使测试工具识别`test/`，而不是把顶层目录改成其他名称。

harness结构应承接coding plan中的harness设计，每个harness都应对应明确的研究目标、目标模块、可修改范围、输入协议、评价指标和结果artifact。
每个harness应关联论文蓝图或experiment plan中的claim、实验问题或方法选择问题，说明它服务哪个研究目标。
harness入口应围绕论文关心的指标组织，例如accuracy、latency、throughput、memory、cost、robustness、generalization、sample efficiency、quality score或领域特定metric；具体指标由论文蓝图和experiment plan决定。
harness应支持后续写代码skill执行“修改模块 -> 运行harness -> 读取结果 -> 再修改”的循环，因此需要稳定入口语义、固定输入协议、可解析输出格式和清晰metric定义。
harness输出应优先记录原始、低加工的artifact，例如per-example prediction、raw score、timing trace、resource usage、intermediate decision、error case、log metadata、config snapshot、seed、split和metric values。
harness不应把面向论文图表的数据聚合和转换写进核心逻辑；聚合、绘图和论文表格生成应由后续分析、绘图或论文写作skill基于原始artifact完成。

testing结构应承接coding plan中的testing设计，把项目功能目标具体化为可运行测试脚本。
test应覆盖数据读取、配置解析、method接口、baseline接口、metric计算、结果导出、CLI入口和核心模块交互等功能正确性问题；具体覆盖范围由coding plan决定。
test应使用小型fixture、toy data、mock data或最小样例，为后续开发提供快速反馈。
目标生态中的fixture、setup/teardown、mock data和测试发现机制可以作为测试组织调研参考，但具体测试框架应根据用户输入、项目选型和deepresearch结果决定。
testing应有明确pass/fail标准，验证代码行为、接口契约、数据格式和结果导出是否正确，而不是用论文性能是否最好作为通过标准。
testing输出主要服务debug和开发反馈，应和论文实验结果artifact分开管理。

初始代码仓库应包含基础配置机制，使不同method、dataset、metric、seed、split、harness和实验阶段可以通过配置或命令行参数表达。
仓库应有清晰入口设计，但具体入口形式由语言和框架决定；可以是CLI、task runner、script entrypoint、notebook-free pipeline或框架命令。
初始仓库应避免以notebook作为核心执行结构；如果需要notebook，只应作为探索或展示辅助，不应成为实验系统的唯一入口。
仓库应为小规模样例数据或mock artifact预留位置，使测试和harness结构可以在后续快速接入最小样例。
仓库应为日志、运行元数据和配置快照预留抽象，使实验结果可追踪。
仓库应包含依赖声明文件或等价配置，使后续代码skill能继续安装、扩展和维护依赖。
仓库应包含必要的静态质量工具配置，例如formatter、linter、type checker或等价工具；具体工具由语言和deepresearch结果决定。
初始仓库的源码结构应围绕论文实验系统的抽象来组织，例如核心逻辑、method接口、baseline接口、配置解析、数据处理、评估逻辑、结果导出和运行入口；这些逻辑如何映射到具体文件夹由现场调研后的项目结构决定。

结果导出结构应承接experiment plan和coding plan，使后续绘图和论文写作skill可以从原始artifact转换得到表格、图和统计结果。
结果导出抽象应优先导出原始、低加工的实验artifact，而不是把论文图表转换逻辑写进系统核心代码。
artifact schema应使用稳定字段命名，并与论文蓝图、experiment plan和coding plan中的method名、metric名、dataset名、split名、harness名和实验阶段命名保持一致。
仓库中的文档、配置和代码都应保持命名一致；模块名、harness名、test名、metric名和artifact字段名应能互相对应。

初始代码仓库除了`README.md`外，还应在仓库根目录创建`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`。
`FRAMEWORK.md`使用英文，`FRAMEWORK.zh-CN.md`使用中文；中文版可以自然保留必要的英文模块名、harness名、test名、method名、metric、命令、配置项和代码标识符。
`README.md`应保持简洁，说明仓库用途、快速入口和主要目录；`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`应更系统地说明这个初始框架的结构、思路、用法和扩展方式。
`FRAMEWORK.md`应描述实际生成出来的仓库框架，而不是描述通用模板；其中提到的目录、模块、harness、test和artifact结构应与当前仓库真实内容一致。
`FRAMEWORK.md`应面向后续写代码skill和人类开发者，说明该框架如何承接`paper_blueprint`、experiment plan和coding plan，以及哪些设计是为了支持后续method实现、harness评测、功能测试、结果导出和论文实验迭代。
`FRAMEWORK.md`应解释固定实验目录的含义，例如`data/`用于输入数据，`output/`用于程序运行输出，`results/`用于实验结果记录，`harness/`用于harness，`test/`用于功能测试。
`FRAMEWORK.md`应解释语言和框架相关的源码结构为什么这样组织；这个解释应基于deepresearch得到的目标语言最佳实践和高质量公开库结构，而不是写成“skill规定如此”。
`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`应简要说明为什么选择当前源码布局，以及该布局如何减少不必要配置、降低运行和测试成本。
`FRAMEWORK.md`应说明核心逻辑模块的职责、模块之间的关系、主要接口、可替换method和baseline的接入方式，以及后续实现应该在哪些抽象点继续扩展。
`FRAMEWORK.md`应说明harness结构：每种harness服务什么论文目标、修改哪个逻辑模块、如何运行、关注哪些metric、输出哪些raw artifact，以及如何支持“修改模块 -> 运行harness -> 读取结果 -> 再修改”的循环。
`FRAMEWORK.md`应说明testing结构：每类test验证什么功能目标、使用什么最小输入、期望什么行为、如何区分功能正确性测试和论文目标评测。
`FRAMEWORK.md`应说明结果导出思路：系统应优先导出原始、低加工artifact，后续绘图和论文写作skill再从这些artifact转换出图表、统计结果和论文表格。
`FRAMEWORK.md`可以包含命令用法或命令语义说明，但应只写当前框架真实支持或预留的入口，不应虚构尚未实现的完整实验命令。
`FRAMEWORK.md`应说明placeholder和extension point的含义，明确哪些部分是初始框架已经搭好的，哪些部分是后续写代码skill需要补全的。
`FRAMEWORK.md`不应解释skill内部流程、工具调用细节、沙盒问题、文件读取方式或runtime workaround；它只解释生成出来的代码框架本身。
`FRAMEWORK.zh-CN.md`不需要逐字翻译英文版，但应覆盖同样的信息，使中文用户能够理解框架结构、设计思路、使用方式和后续扩展点。
`FRAMEWORK.zh-CN.md`应使用自然中文表达，中英混排时保持术语稳定，例如统一使用同一个harness名称、模块名称、metric名称和artifact名称。
`README.md`、`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`中的命令、路径和文件引用都应使用仓库内相对路径，不应出现用户机器上的绝对路径。
如果deepresearch发现了可直接安装调用的工具，`FRAMEWORK.md`应简要说明这些依赖的用途；如果某些工具只被参考或只复用了许可允许的代码片段，也应在`FRAMEWORK.md`、`FRAMEWORK.zh-CN.md`或相应说明中记录来源和用途。
如果仓库结构因deepresearch和项目选型发生变化，`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`也应同步反映最终结构，而不是保留预设模板描述。
如果仓库复制或改写了外部代码片段，应在合适的文档或源文件注释中保留来源、license和必要attribution。
文档中解释结构时，应优先用模块名、harness名、test名、method名或自然简称指代内容，而不是依赖抽象编号互相引用。

初始仓库创建前，skill应形成简短的内部仓库结构决策，明确语言和框架选择、固定实验目录、生态源码结构、harness目录、test目录、配置机制、接口抽象、artifact schema和静态检查方式。
最终输出应体现为实际仓库文件，而不是只生成计划。
skill创建仓库时应优先使用自然、语义化的文件夹和模块命名，不应使用`c1/c2/c3/b1/b2/b3`这类抽象编号系统。
文件内容应简洁但可扩展，避免为了显得完整而生成大量无实际作用的模板代码。
如果需要脚本，应围绕稳定入口、可复用参数和清晰职责设计，避免生成大量一次性脚本。
代码中可以保留必要注释，解释抽象接口、placeholder和扩展点；注释应服务后续实现，不解释skill内部流程。
skill可以在内部先形成“为什么选择这种目录结构”的决策，但最终仓库不应包含大段skill流程解释；必要说明应以面向开发者的`FRAMEWORK.md`、`FRAMEWORK.zh-CN.md`、`README.md`或简洁developer notes形式呈现。
所有创建的文件和文件夹都必须位于用户输入的初始代码仓库路径下；仓库内部引用使用相对于该仓库根目录的路径。
如果需要在输出说明中列出仓库结构，只列出实际创建在目标仓库内的相对路径，不使用绝对路径。

初始仓库中的代码应继承`academic-army-coding-style`的作者风格：少抽象、少状态、少转换、强命名、强边界、强顺序一致性。
生成代码时应优先使用最直接的实现路径，不为简单逻辑添加额外中间层、包装层、转换层或临时结构。
代码应短、直、少层级；能内联就内联，能直接传递就直接传递，能删除无意义helper就删除无意义helper。
如果一段逻辑只用一次、很短、没有独立语义，应放在使用点附近；只有真正复用、表达稳定不变量、定义清晰边界或显著提升局部可读性时，才抽成独立helper。
不要创建只负责转手、改名、包装、拆包或重新组装数据的helper；不要创建“拆开又合上”的中间结构。
初始仓库可以预留接口和extension point，但这些抽象必须有真实语义价值，例如稳定method接口、baseline接口、metric接口、artifact writer或harness runner边界。
不要为了未来可能扩展而提前引入复杂结构；当前简单结构能表达清楚时，就保持简单。
skill在设计代码抽象时，应分析每个抽象是否会让调用方代码、配置文件、harness入口、test脚本或method实现变得更长、更绕或更难维护。
skill应优先采用能减少重复、稳定接口、缩短调用路径的抽象；如果一个抽象只把复杂度从模块内部转移到每个调用方，不应采用。
对每个核心抽象，例如registry、adapter、factory、config object、runner、pipeline、plugin interface，skill应评估它带来的收益和代价：是否减少重复实现，是否让method替换更清晰，是否让harness更容易运行，是否让测试更简单。
如果某个抽象会导致大量样板代码，例如每新增一个method都要改多个注册点、写多个配置块、补多个wrapper，skill应考虑更直接的设计。
如果某个接口设计会让所有调用方都需要传入过多参数，skill应考虑把稳定上下文收敛到配置对象、run context或明确的数据结构中，但不要因此引入过重框架。
如果某个配置系统会让简单实验必须写大量配置文件，skill应考虑更轻量的默认值、局部覆盖或命令行参数语义。
如果某个模块拆分会导致大量跨模块转发函数、薄wrapper或只调用一次的抽象层，skill应合并或简化这些模块。
如果某个设计会让test脚本和harness脚本为了调用核心逻辑而写大量准备代码，skill应改进入口和接口，使测试和harness能够直接表达目标。
skill应避免为了“预留扩展性”而过早引入多层抽象；扩展点应围绕论文实验中真实存在的变化点，例如candidate method、baseline、metric、dataset、harness和result artifact。
skill应区分必要复杂度和偶然复杂度：论文实验本身需要的method替换、harness评测、结果导出属于必要复杂度；由目录布局、导入路径、过度封装或配置系统带来的额外负担属于应尽量减少的复杂度。
公共层只放真正公共、稳定、跨多个地方共享的内容；只在局部使用的helper、数据结构、配置、状态或特殊逻辑应放在使用点附近。
共享基础结构只承载所有使用方共同需要的能力，不承载少数使用方的特殊逻辑。
特殊case应尽量留在特殊case的使用位置，不要为了少数情况污染公共层。
创建新层级前应判断能否通过内联、改名、移动位置或删除中间结构解决问题。

初始仓库中的每个变量、状态、配置和数据结构都应属于真实拥有它的层级。
局部流程中产生的内容应留在局部，不要提升成公共状态或共享输入。
只有长期稳定、跨边界仍有语义的数据才进入共享结构；临时状态不应被建模成长期状态。
单次流程中的中间内容应优先作为值直接传递，不要为了保存而改变数据模型。
上层派生并只由上层使用的内容应留在上层，不应伪装成下层模块的输入。
如果某个数据只服务于编排、保存或展示，不应污染业务模块的接口。
层级边界应清楚：谁负责生成、谁负责处理、谁负责保存、谁负责暴露，都应在代码结构中直接体现。

初始仓库的命名必须精确反映真实含义，不使用泛化、含糊、历史残留或与数据形态不一致的名称。
名称应来自论文领域契约、experiment plan、coding plan和当前代码语义，而不是来自临时实现细节。
名称应尽量短而语义完整，删除不增加信息量的前缀、后缀和包装词。
同一个概念在接口、配置、类型、文档、调用点和输出artifact中应使用一致名称。
名称后缀应反映真实数据形态；表示引用、路径、内容、状态、结果、配置的名称不能混用。
如果一个名称暗示它是引用或外部资源，它就不应承载已经读取后的内容；如果一个名称表示内容本身，就不应继续保留引用式或路径式命名。
已由论文蓝图、experiment plan、coding plan或用户输入形成契约的术语、拼写和领域词应保持一致，不应擅自改写。

代码排列顺序应帮助读者理解流程。
执行顺序明确的逻辑，应让代码顺序尽量反映执行顺序；输入、校验、构造、调用、输出等步骤应按自然阅读顺序组织。
语义对应的结构应尽量保持字段顺序、参数顺序和定义顺序一致，减少读者在多个结构之间反复做脑内映射。
相关代码应靠近放置，减少跨文件、跨模块、跨层级跳转。
结构本身应表达意图，而不是依赖大量注释解释绕来绕去的数据流。

初始仓库中的代码应清楚区分“内容本身”和“对内容的引用”。
如果传递的是内容，就使用内容语义的命名；如果传递的是引用，就使用引用语义的命名。
内容和引用的边界应通过命名、接口和数据流直接体现，避免一个变量名暗示它是路径、句柄或标识，但实际承载已读取内容。
当外层负责保存、归档或落盘时，内层不应同时承担同一写入责任。
写入、保存、导出、返回等责任应单一，避免多个层级同时声称负责同一个产物。

如果初始仓库中包含prompt、任务说明、内嵌文案或给agent的指令文本，这些文本也应遵守代码风格。
内嵌任务说明应直接描述任务，不使用角色扮演式开头。
输入说明应清楚区分外部引用和直接内容，输出说明应明确谁负责生成内容、谁负责保存内容。
不要在内嵌文本中使用没有上下文的裸文件名、伪路径或模糊指代。
Prompt文本应短、明确、任务导向，不展示skill内部流程，也不解释为什么采用某个模板。

注释只用于解释非显然决策、约束或特殊原因。
如果代码可以通过简化变得自解释，应优先简化代码，而不是添加注释。
不要用注释解释本可以通过命名、结构或边界表达清楚的内容。
不要把风格分析、实现过程、调试过程或skill规则写进代码注释。
注释应服务后续维护者理解代码，不服务展示生成过程。

初始化已有仓库时应做最小必要修改，避免顺手重构无关代码。
如果任务只是补充初始骨架、重命名、文案调整、接口连接或配置连接，不应顺手整理无关逻辑。
修改现有代码时应贴近当前代码库已有模式，但不要复制已有代码中的坏抽象和坏命名。
遇到复杂代码时，优先判断哪些结构可以删除、内联、移动到使用点或重新命名；不要为了兼容旧结构而继续添加适配层，能删除旧结构时优先删除。

本skill只做静态检查，不运行安装命令、不执行测试、不运行harness、不跑实验。
静态检查可以包括文件是否创建完整、路径是否都在目标仓库内、语法层面是否自洽、配置文件是否存在、接口命名是否一致、文档和代码结构是否匹配等。
静态检查应根据目标语言和框架选择合适工具或检查方式；静态分析的核心是“不执行程序而检查源码或配置”，具体工具由deepresearch现场决定。
静态检查完成后，skill应确认固定顶层结构存在，即`data/`、`output/`、`results/`、`harness/`、`test/`、`README.md`、`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`，并确认关键文件、依赖声明、配置入口、模块接口和结果artifact约定都已经创建。
skill应在静态检查阶段确认语言和框架相关结构与deepresearch得到的最佳实践一致。
skill应在静态检查阶段确认没有把任何具体语言、框架、目录布局案例或公开库示例结构当成无条件模板；最终结构应能追溯到用户输入、项目选型、deepresearch结论和论文实验需求。
skill应在静态检查阶段确认`README.md`、`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`都存在，并且其中描述的目录、模块、harness、test和结果artifact与实际仓库结构一致。
skill应在静态检查阶段确认`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`已经覆盖框架描述、设计思路、目录说明、核心模块、harness说明、test说明、结果导出说明、后续扩展点和基本使用方式。
skill应在静态检查阶段确认`README.md`保持简洁入口定位，`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`只描述实际创建或明确预留的目录、模块、命令和功能，不引用仓库外绝对路径，不把placeholder写成已完成实现。
skill应进行Friction audit检查：静态检查是否存在不必要的导入配置、路径别名、额外环境变量、重复注册点、过长调用链、薄wrapper、过度拆分模块或让harness/test变复杂的抽象；如果存在，应优先改成更直接、更低配置成本的结构。
skill应在静态检查阶段确认默认导入、默认测试入口、默认harness入口和预期运行路径不依赖隐藏路径假设或大量全局配置。
如果需要运行安装、测试、harness或实验，应交给后续代码实现、测试执行或实验执行skill。

本skill应保持论文目标驱动：每个核心模块、harness和test都应能追溯到论文蓝图、experiment plan或coding plan中的需求。
初始仓库不应主动加入与论文实验无关的复杂基础设施，例如过度CI、服务部署、web dashboard、数据库系统或分布式训练框架，除非experiment plan或deepresearch显示确有必要。
skill应尽量使用正向语言描述仓库应包含什么、服务什么目标、如何承接上游计划、如何支持后续实现，减少堆叠防御性规则。
skill应避免把运行时工具失败、沙盒限制、文件读取失败、shell命令受限、MCP调用失败等runtime workaround写进skill内容；这些属于外层runtime或orchestrator职责。
skill输出或报告中不应混入工具失败、权限绕过、文件读取方式等与初始代码仓库设计无关的内容。
如果需要给用户说明结果，应只说明创建了哪些仓库能力、哪些抽象已预留、后续写代码skill应从哪里继续，而不是解释runtime操作细节。

**Hybrid repository layout原则**：初始代码仓库采用“固定实验目录 + 动态生态结构”的混合布局；`data/`、`output/`、`results/`、`harness/`、`test/`、`README.md`、`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`作为论文实验工作流的固定顶层结构，源码目录、packaging文件、构建配置、测试框架配置和语言生态目录由deepresearch现场调研高质量公开库和官方最佳实践后确定。
**No hardcoded language layout原则**：skill不得预设任何具体语言、运行时、框架、包管理器、测试框架、配置文件或目录布局；selected stack相关结构必须来自用户指定、deepresearch调研和当前实验系统需求的共同判断。
**Research-informed structure原则**：仓库结构不是套模板，而是根据论文蓝图、experiment plan、coding plan、目标语言、框架生态、packaging质量和高质量公开库结构综合设计。
**Documentation handoff原则**：`README.md`负责快速介绍仓库，`FRAMEWORK.md`和`FRAMEWORK.zh-CN.md`负责把初始代码框架的设计思路、使用方式、harness/test组织、结果导出和后续扩展点讲清楚，帮助后续写代码skill和用户理解如何在这个框架上继续实现。
**Low-friction framework原则**：初始代码仓库应在符合目标语言和框架最佳实践的前提下，优先选择低配置、低样板、低调用成本的结构；任何目录布局、packaging方式、抽象层、registry、adapter、config系统或runner设计，都应经过“是否让运行、测试、harness或后续method实现变得更复杂”的检查。
**总原则**：这个skill负责把论文蓝图、experiment plan和coding plan落成一个静态、规整、可扩展的初始代码仓库；它应在用户指定路径内创建真实文件结构，为固定实验目录、harness、test、method实现、结果导出和后续代码实现预留清晰抽象，同时通过deepresearch现场选择合适语言、框架、工具和最佳实践。
