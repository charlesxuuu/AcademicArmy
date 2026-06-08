这个skill属于一套基于Codex的autoresearch工具链，任务是根据`paper_blueprint`、`experiment plan`和`coding plan`初始化一个项目脚手架。
本skill处于模板 / 脚手架阶段，核心是先用模板工具、官方初始化方式或高质量template repository生成真实代码库骨架，再叠加论文实验目录和说明文件。
项目初始化skill的核心产物是一个由模板工具、官方初始化命令或高质量template repository生成的真实代码库脚手架，而不是一组README说明文件。
`README.md`、`README.zh-CN.md`、`REFERENCES.md`和`REFERENCES.zh-CN.md`只是脚手架的配套文档，不是主要产物。

本skill接收用户指定的初始代码仓库路径，并只在该路径下创建项目脚手架文件和文件夹。
所有创建的文件和文件夹都必须位于用户输入的代码仓库路径下；仓库内部引用使用相对于仓库根目录的路径。
如果目标仓库路径已经存在文件，skill应在保护用户已有内容的前提下做最小必要检查，根据任务要求在现有内容上生成或补齐脚手架，避免覆盖用户已有文件。
如果用户明确要求基于已有代码仓库初始化或改造，skill才读取目标仓库中与脚手架初始化有关的文件；否则应把指定路径视为新仓库或待初始化目录。

本skill只负责项目脚手架初始化，不实现论文方法、不实现实验流程、不写论文业务逻辑、不跑测试、不跑harness、不执行实验。
skill可以调用选定的模板工具、官方初始化命令或模板仓库来生成starter files、boilerplate structure、依赖声明、入口文件、最小样例和生态相关配置；这些属于项目脚手架的一部分。
skill应区分“模板自带基础代码”和“论文业务代码”：前者可以由模板生成并保留，后者应留给后续代码实现skill。
如果最终仓库只有README、REFERENCES、空目录和说明文件，没有模板生成出的基本代码库结构，应视为skill没有完成项目初始化任务。

skill应只读取生成脚手架所必需的输入，例如`paper_blueprint`、`experiment plan`、`coding plan`和用户指定的仓库路径。
skill应基于这些输入判断项目需要的目标语言、运行时、框架逻辑、实验形态、harness/test需求、输入数据、输出结果和后续实现方向。
这种判断只用于选择初始化方式、生成真实starter repo、配置可安装依赖、叠加固定实验目录、编写README/REFERENCES和创建harness/test说明文件，不用于实现具体method、metric、data loader、result exporter、配置解析或实验runner。
skill不应主动探索当前目录下无关文件；如果需要外部知识，应通过deepresearch调研，而不是从目录噪声中猜上下文。
skill不应把Codex运行环境、沙盒限制、文件读取失败、shell命令受限、MCP调用失败、依赖安装失败等runtime workaround写进skill内容、README或REFERENCES。

skill应使用`academic_army_mcp_tools`中的deepresearch调研当前目标生态通常如何初始化项目。
deepresearch应重点搜索目标生态的官方初始化方式、高质量模板工具、template repository、starter project、boilerplate project、research code template、benchmark template、harness template和目标生态中的高质量公开repo。
skill应调研并比较可实际生成项目结构的工具或来源，例如通用模板生成器、目标生态官方initializer、社区高质量starter template、GitHub template repository或研究代码模板；具体采用哪个由现场调研决定，不写死在skill里。
Cookiecutter、Copier、Yeoman、GitHub template repositories等可以作为deepresearch的候选参考方向，因为它们都支持从模板或generator生成项目结构；但skill不应固定使用其中任何一个。

skill应优先寻找并调用能生成真实starter files或boilerplate structure的工具或来源，而不是只手工创建`README.md`、`REFERENCES.md`和`harness/`。
如果目标生态存在官方或事实标准的初始化命令，skill应优先考虑该初始化方式。
如果官方初始化方式不适合论文实验仓库，skill再考虑通用模板生成器、高质量template repository、research code template、benchmark template或harness template。
skill应优先选择能直接生成基本代码库结构的工具或模板，选择标准包括目标生态惯例、维护状态、license清晰度、目录结构清晰度、配置成本、后续代码skill继续实现的便利性，以及与当前论文实验工作流的匹配度。

如果存在多个候选模板、initializer或template repository，skill应比较它们的生成结果，而不是只看简介。
比较维度包括目录结构、依赖声明、入口文件、测试结构、配置复杂度、文档质量、license、维护状态和与论文实验工作流的匹配度。
skill应避免从质量较差、过度复杂、长期不维护、license不明确或与当前任务无关的公开repo中学习脚手架结构。
选定模板或初始化方式后，skill应实际调用该模板工具、官方初始化命令或模板仓库，在用户指定repo路径下生成基本代码库结构。

使用模板生成后，skill应在生成出的代码库基础上叠加论文实验固定目录和说明文件，而不是用手写目录完全替代模板生成结果。
模板负责目标生态的标准代码库骨架，固定目录负责论文实验工作流。
模板生成出的源码目录、依赖声明、构建配置、测试配置、入口结构和生态相关文件应由模板工具和deepresearch结果决定，不应在skill里写死。
skill应把生成出的模板结构与固定实验目录合并：模板结构保留目标生态的starter repo语义，固定实验目录保留论文实验工作流语义。
如果模板已经生成了某些与固定目录语义相近的目录，skill应保留固定顶层约定，并在README中简要说明两者关系，避免目录语义混乱。
skill正文中不应出现任何具体语言、框架、包管理器、依赖文件、构建文件、源码目录、测试目录或配置文件名的验证规则。
skill编写时不要把具体技术栈文件名当作例子写进通用规则里；即使只是“例如”，模型也可能把它们当成必须验证的固定清单。
如果需要说明某类文件，应使用功能角色名，例如“依赖声明文件”“项目元数据文件”“构建配置”“测试配置”“源码布局”，不要给出具体生态文件名。
如果确实需要在运行中提到具体文件名，只能在已经选定模板并生成repo之后，根据实际仓库内容在README或REFERENCES里自然记录。

选定模板后，skill应根据模板生成结果建立一个内部`project artifact registry`，记录实际存在的项目元数据、依赖声明、安装说明、源码布局、测试布局、harness目录和固定实验目录。
后续依赖写入、README安装说明、REFERENCES记录和静态检查都应基于这个`project artifact registry`，而不是基于skill预设文件名。
`project artifact registry`是skill内部工作清单，不需要作为单独文件输出；必要信息可以自然反映在README和REFERENCES中。
具体要验证哪些文件，只能从三处动态获得：用户明确指定、deepresearch得到的目标生态最佳实践、模板工具实际生成的文件结构。
Do not name or validate any ecosystem-specific files or directories in this skill. Identify dependency declarations, build configuration, source layout, and test layout from the selected template and generated repository, then validate those discovered artifacts by role.

固定实验目录仍应存在：`data/`、`output/`、`results/`、`harness/`。
`data/`用于输入数据，`output/`用于程序运行输出，`results/`用于实验结果记录，`harness/`用于所有论文实验harness。
固定文档仍应存在：`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
固定目录只规定论文实验工作流的顶层语义，不规定目标语言生态内部的源码布局。
测试目录不再固定为某个顶层测试目录；测试文件、测试目录和测试配置应跟随模板工具、目标生态最佳实践和deepresearch调研到的高质量公开repo结构。

`harness/`下面应根据`coding plan`中的每种harness创建独立子文件夹，并在每个子文件夹中放置说明文件。
每种harness的子文件夹名称应语义化，能表达其服务的任务，不应使用`c1/c2/c3/b1/b2/b3`这类抽象编号。
每个harness说明文件应写清楚该harness的任务、关联实验目标、后续应实现的运行入口、输入、metric、输出artifact和实现占位。
skill应先用模板工具、官方初始化方式或template repository生成真实代码库骨架，再识别模板生成出的测试结构。
如果模板已经生成了测试目录或测试入口，skill应把`coding plan`中的test类别映射到模板现有测试结构中，而不是额外创建固定顶层测试目录。
如果模板没有生成测试结构，skill应通过deepresearch调研目标生态的常见测试组织方式，并按该生态的最佳实践创建测试结构。
每一种test仍然需要单独的说明位置，但该位置应放在模板或目标生态决定的测试结构下，而不是强制放在固定顶层测试目录下。
每个test说明文件应写清楚该test类别验证什么功能、后续应覆盖哪些输入输出、pass/fail含义和实现占位。
harness/test说明文件只描述任务和预留结构，不实现具体harness逻辑或测试逻辑。
如果模板测试结构与`coding plan`中的test类别不完全匹配，skill应在不破坏模板生态规范的前提下进行轻量扩展，例如在模板测试区域内增加语义化子目录或说明文件。
skill不应为了统一目录而修改模板的测试体系；如果模板已有测试运行约定，应尽量保持其原生结构，避免引入额外配置成本。

skill应区分两类外部开源资源：`installable dependencies`和`reference-only sources`。
`installable dependencies`指packaging良好、license明确、接口稳定、适合通过目标生态依赖机制直接安装并调用的开源库。
`reference-only sources`指与当前论文实验相关、值得学习或后续参考，但不适合作为依赖直接安装调用的开源代码、论文代码、benchmark实现、harness实现或模板项目。
skill应通过deepresearch搜索相关开源代码和工具，并判断哪些可以作为依赖直接安装调用，哪些只能作为后续实现参考。

对可以直接安装调用的开源库，skill应按照模板生成的目标生态标准，把依赖写入当前项目的依赖声明、项目配置或等价dependency manifest中。
skill只写好依赖配置，不运行安装命令、不解析依赖、不下载依赖包、不生成需要安装命令才能得到的新lock状态。
如果模板生成结果已经包含依赖声明文件，skill应在模板既有机制内补充依赖，而不是另起一套依赖配置方式。
如果模板没有生成依赖声明文件，skill应根据deepresearch到的目标生态最佳实践创建最小必要的依赖配置文件。
如果目标生态通常需要lock file，但lock file必须通过安装或解析命令生成，skill不应为了生成lock file而运行安装；可以保留模板自带lock file，或在README/REFERENCES中说明当前阶段只声明依赖、未执行安装解析。
skill不应在tips里写死任何具体语言、包管理器、依赖文件名或配置文件名；依赖配置方式由模板、目标生态和deepresearch现场决定。

README必须包含一个`Installation`章节，`README.zh-CN.md`必须包含对应的中文“安装”章节。
`Installation`章节应说明如何在当前repo下安装项目依赖和准备本地开发环境，但不应要求用户把项目依赖安装到全局环境中。
skill应使用`academic_army_mcp_tools`中的deepresearch查询目标语言、目标运行时和目标生态的包管理方式、依赖声明方式、环境隔离方式和安装最佳实践。
skill不应在tips或skill正文中写死任何具体语言、包管理器、环境管理工具、依赖文件名或安装命令；这些内容应由deepresearch和模板生成结果现场决定。
如果模板已经生成了依赖声明、环境配置或安装说明，skill应基于模板原生机制补充和修订，而不是另起一套不一致的安装方式。
如果模板没有生成安装说明，skill应根据目标生态最佳实践在README中补充最小、清晰、repo-local的安装步骤。

skill应区分`system prerequisites`和`project dependencies`：前者是用户机器上需要已有的基础工具链或包管理器，后者是当前repo声明并管理的项目依赖。
README中的安装说明可以列出必要的system prerequisites，但skill不应安排安装这些全局工具，也不应把项目依赖安装到全局环境。
README中的项目依赖安装方法应优先使用目标生态支持的repo-local、project-local、workspace-local或environment-isolated方式。
如果目标生态支持本地隔离环境、项目级依赖目录、workspace、sandbox、container或等价机制，skill应优先采用这种方式描述安装流程。
如果目标生态存在多种安装方式，skill应选择更符合当前模板、低配置成本、低全局污染、易于后续harness/test运行的方式。
安装说明应尽量让用户在仓库根目录下执行少量命令即可完成依赖准备，不需要修改全局配置、全局路径或系统级包目录。
如果某些工具必须全局存在才能运行目标生态的包管理命令，README应把它们写成前置条件，而不是写成本skill已经安装或会安装的内容。
README应明确说明当前阶段已经声明依赖和安装步骤，但本skill没有执行安装，后续实现或运行阶段再实际安装。
安装说明应尽量包含：进入repo根目录、创建或激活项目本地隔离环境、安装项目依赖、验证依赖配置已准备好、下一步由后续skill实现代码或运行harness/test。
安装说明不应包含运行实验、运行harness、运行test或执行论文方法的命令；这些属于后续实现和运行阶段。
如果模板生成的安装方式会污染全局环境，skill应通过deepresearch寻找目标生态中更推荐的project-local替代方式，并在README中采用低污染方案。
如果目标生态的最佳实践本身依赖全局工具，但项目依赖仍可隔离安装，README应清楚区分“全局已有工具”和“本repo本地依赖”。

对不能直接安装调用的相关开源代码，skill不应把它们写入依赖配置，也不应在模板阶段复制其业务代码。
对不能直接安装调用但有参考价值的开源代码，skill应记录在`REFERENCES.md`和`REFERENCES.zh-CN.md`中，作为后续代码实现skill的参考来源。
如果某个开源库packaging不规整、依赖过重、接口不稳定、维护不足、license不适合或只需要其中少量逻辑，skill应把它归为reference-only source，而不是强行写入依赖配置。
如果某个开源库license不明确或不兼容，skill只能把它作为阅读参考，并在`REFERENCES.md`中明确标注不要复制或直接复用其代码；公开仓库并不自动等于他人可以自由使用、修改和分发代码，必须看license授权。
如果某个依赖与当前论文实验强相关但安全性、维护状态或依赖治理存在风险，skill应在`REFERENCES.md`中记录这个风险，而不是只把它悄悄写进依赖配置。

`README.md`和`README.zh-CN.md`应说明这是一个由模板工具、官方初始化方式或模板仓库初始化出的项目脚手架，并说明固定实验目录、harness/test预留结构和后续实现方向。
`README.md`使用英文，`README.zh-CN.md`使用中文。
README应简要说明项目用途、上游输入、最终采用的初始化方式、模板生成出的基础代码库结构、固定实验目录含义、模板生成或调研决定的测试结构、harness/test职责差异和后续实现方向。
README可以简要说明“依赖已按目标生态写入配置，但本skill不会执行安装；后续实现或运行阶段再安装依赖”。
README应说明`harness/`服务论文目标评测、method筛选和实验迭代；test结构服务代码功能正确性，并遵循目标生态的模板布局。
README不应替代模板生成；如果最终仓库只有文档和空目录，没有模板生成出的基本代码库结构，应视为skill没有完成项目初始化任务。
README不应声称具体论文方法、实验流程或功能代码已经实现。

`REFERENCES.md`和`REFERENCES.zh-CN.md`应记录deepresearch调研过的模板工具、模板仓库、开源项目和最终选用的生成方式。
`REFERENCES.md`使用英文，`REFERENCES.zh-CN.md`使用中文。
`REFERENCES.md`中应把外部来源按用途分类，例如`Installable dependencies`、`Template sources`、`Reference-only repositories`、`Harness references`、`Benchmark references`、`Future implementation references`。
`REFERENCES.md`应明确记录最终采用的模板来源、生成工具、license、版本或commit、生成方式、保留了哪些模板内容、删除或调整了哪些内容、为什么选择它。
`REFERENCES.md`应说明测试结构为什么采用模板中的位置，或在模板未提供测试结构时说明deepresearch依据了哪些目标生态最佳实践。
`REFERENCES.md`和`REFERENCES.zh-CN.md`应记录包管理和安装方案的来源，包括目标生态最佳实践、模板工具、依赖配置方式、环境隔离方式和最终采用的安装策略。
`REFERENCES.md`中每个installable dependency应记录项目名、来源链接、license、版本或推荐版本范围、用途、为什么适合直接安装调用、将被哪个模块或harness使用。
`REFERENCES.md`中每个reference-only source应记录项目名、来源链接、license、参考内容、为什么不直接作为依赖、后续可能借鉴的结构或代码片段。
如果调研了但没有采用某个候选模板，`REFERENCES.md`可以简要说明未采用原因，例如结构过重、维护不足、license不合适、与实验工作流不匹配或配置成本过高。
如果模板自带文件被保留或改写，`REFERENCES.md`应说明这些文件来自哪个模板以及做了哪些脚手架层面的调整。
`REFERENCES.zh-CN.md`不需要逐字翻译英文版，但应覆盖同样信息，使用户理解外部模板和开源项目如何影响当前脚手架。
`REFERENCES.zh-CN.md`应覆盖`REFERENCES.md`中的同样信息，用中文说明哪些开源库被配置为可安装依赖，哪些只是后续实现参考，以及为什么这样分类。

模板阶段不复制具体业务逻辑代码。
如果deepresearch发现有价值的开源实现，应在`REFERENCES.md`和`REFERENCES.zh-CN.md`中记录为后续实现参考，而不是在本阶段移植代码。
如果模板本身自带starter code、boilerplate code或最小入口文件，可以保留这些模板生成内容；这些属于代码库脚手架的一部分，不等同于实现论文业务逻辑。
GitHub关于Codespaces模板的文档也说明template repositories通常包含starter files和boilerplate code，帮助用户快速开始使用某个库、框架或技术；因此模板阶段可以保留模板自带的基础starter files，但不应生成论文方法实现。
对license不明确或不兼容的项目，只能作为阅读参考，不应把其代码或模板文件复制进仓库。

skill只做脚手架静态检查。
静态检查应确认模板生成确实发生过，最终repo中存在目标生态合理的基础代码库结构，而不只是手写README和空文件夹。
静态检查应确认所有创建路径都位于目标仓库路径内。
静态检查应使用抽象角色描述验证对象，例如`dependency declaration artifact`、`project metadata artifact`、`build configuration artifact`、`source layout selected by the template`、`test layout selected by the template`、`installation instructions`，而不是写具体文件名。
静态检查应确认模板生成的项目元数据、依赖声明、构建配置、源码布局、测试布局和安装说明彼此一致；这些具体对象应从模板生成结果中识别，而不是由skill预设名称。
如果模板生成了某个依赖声明文件，skill应验证“模板选定的依赖声明文件已按目标生态方式更新”；不要在skill里预设这个文件叫什么。
如果模板生成了某个源码目录，skill应验证“源码布局与选定模板和目标生态一致”；不要在skill里预设源码目录叫什么。
如果模板生成了某个测试结构，skill应验证“test目标已映射到模板选定的测试结构中”；不要在skill里预设测试目录或测试文件路径。
如果模板生成了某个构建、打包、运行或工具配置文件，skill应验证“配置与选定模板保持一致”；不要在skill里列举具体配置文件名。
静态检查不应要求存在任何预设的语言文件、构建文件、依赖文件、源码目录或测试目录。
静态检查应确认固定实验目录和文档已叠加到模板结构中：`data/`、`output/`、`results/`、`harness/`、`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`。
静态检查应确认每种harness都在`harness/`下有独立子文件夹和说明文件。
静态检查应确认每种test都已经被映射到模板决定的测试结构中，并有对应说明文件。
静态检查不应要求存在固定顶层测试目录。
如果最终repo同时存在模板测试结构和额外顶层测试目录，skill应检查这是否由模板或deepresearch明确支持；如果只是skill自行强加，应移除或改回模板结构。
静态检查应确认所有installable dependencies已经写入目标生态的依赖配置。
静态检查应确认所有reference-only sources已经写入`REFERENCES.md`和`REFERENCES.zh-CN.md`。
静态检查应确认没有把reference-only source误写成依赖，也没有在模板阶段复制其业务代码。
静态检查应确认没有运行安装命令、没有解析依赖、没有下载依赖包、没有生成需要安装命令才能得到的新lock状态。
静态检查应确认`REFERENCES.md`中的依赖分类与项目配置一致：写进依赖配置的库必须出现在`Installable dependencies`部分，未写入依赖配置的参考项目必须出现在reference-only相关部分。
静态检查应确认README和中文版README都有安装章节。
静态检查应确认安装章节没有声称skill已经运行安装命令。
静态检查应确认安装章节优先使用repo-local或environment-isolated安装方式，而不是默认全局安装项目依赖。
静态检查应确认依赖配置、README安装说明、REFERENCES依赖记录三者一致。
静态检查应确认README中的安装章节与`REFERENCES.md`中的依赖分类保持一致：写入依赖配置的库应出现在installable dependency记录中，reference-only来源不应出现在安装命令或依赖配置里。
静态检查应确认`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`描述的模板来源、生成方式和实际目录结构一致。
静态检查应确认仓库文档只描述脚手架、模板来源和后续实现方向，没有把placeholder写成已完成实现。
静态检查不运行代码、不安装依赖、不执行测试、不运行harness、不执行实验。

推荐的skill流程是：读取`paper_blueprint`、`experiment plan`、`coding plan`和目标repo路径，只提取项目初始化所需的信息；用deepresearch判断目标语言、运行时和框架逻辑；用deepresearch搜索该目标生态的官方初始化方式、高质量模板工具和template repositories；比较候选模板或初始化方式，选择一个最适合当前论文实验仓库的生成方案；在目标repo路径下调用选定方案生成基本代码库结构；识别模板生成出的测试结构和依赖配置机制；用deepresearch区分installable dependencies和reference-only sources；把installable dependencies写入模板生态的依赖配置，把reference-only sources写入REFERENCES；用deepresearch确定目标生态repo-local安装和环境隔离最佳实践，并写入README的Installation章节和中文版README的安装章节；在生成出的结构上叠加固定实验目录；根据`coding plan`为每种harness创建独立子文件夹及说明文件；把每种test映射到模板或目标生态决定的测试结构中并放置说明文件；创建`README.md`、`README.zh-CN.md`、`REFERENCES.md`、`REFERENCES.zh-CN.md`；做脚手架静态检查，确认“模板生成的基本代码库结构 + 依赖配置 + repo-local安装说明 + 固定实验目录 + harness说明 + 模板测试结构中的test说明 + README/REFERENCES文档”都存在且一致。

skill应使用自然、可读的文档写法，不依赖复杂编号系统。
README、REFERENCES和harness/test说明文件应优先使用目录名、harness名、test名、artifact名或自然简称，不使用抽象编号互相引用。
说明文件应清楚表达“这是预留结构”和“后续实现应在这里补充什么”，避免写成已经完成的功能文档。
最终输出应聚焦实际采用了什么模板生成方式、生成了哪些starter repo结构、配置了哪些installable dependencies、README中写了哪种repo-local安装方式、叠加了哪些论文实验目录、哪些harness/test位置已预留，以及后续实现skill应从哪里继续。

**Scaffold generation requirement**：本skill必须通过deepresearch找到适合当前目标生态的项目初始化方式，并实际生成基本代码库脚手架；只创建README、REFERENCES、空目录和说明文件不算完成任务。
**Template-first原则**：项目初始化先通过模板工具、官方initializer或高质量template repository生成真实starter repo，再叠加论文实验目录和说明文件。
**Scaffold-only原则**：本skill只负责创建项目脚手架；具体论文业务代码、实验流程实现、harness逻辑、测试逻辑、代码风格配置和质量审查留给后续skill。
**Template-informed原则**：项目结构应由deepresearch调研到的官方初始化方式、高质量模板工具、template repository和公开repo共同决定，不在tips里写死具体语言、框架或源码布局。
**Updated hybrid layout原则**：`data/`、`output/`、`results/`和`harness/`是论文实验工作流的固定顶层目录；测试结构属于目标语言和模板生态的一部分，应由模板生成结果和deepresearch决定，不固定为某个顶层测试目录。
**Template-first test layout原则**：测试文件放在哪里、如何分层、如何命名、如何被测试工具发现，都应优先遵守模板生成的项目结构；skill只把`coding plan`中的test目标映射进去，不强行改造测试目录。
**Experiment scaffold原则**：固定保留`data/`、`output/`、`results/`和`harness/`，让脚手架天然承接论文实验工作流；模板生成结构负责目标生态的标准代码库骨架和测试结构。
**Scaffold validation原则**：项目初始化完成后，skill应确认“模板生成的基本代码库结构 + 依赖配置 + 固定实验目录 + harness说明 + 模板测试结构中的test说明 + README/REFERENCES文档”都存在且一致；只有文档和空目录不算完成初始化。
**Reference documentation原则**：`REFERENCES.md`和`REFERENCES.zh-CN.md`负责记录模板来源、生成工具、license、版本、采用方式、保留内容、调整内容和选择理由；模板阶段发现的外部代码实现只记录为后续参考，不在本阶段移植。
**Dependency declaration原则**：项目初始化skill负责通过deepresearch选择可直接安装调用的开源库，并把它们写入当前模板生态的依赖配置；它不运行安装。不能直接安装调用的相关开源代码只进入`REFERENCES.md`和`REFERENCES.zh-CN.md`作为后续实现参考，不进入依赖配置。
**Repo-local installation原则**：项目初始化skill应通过deepresearch确定目标生态的包管理和环境隔离最佳实践，把可直接安装调用的依赖写入项目依赖配置，并在`README.md`和`README.zh-CN.md`中写出尽量不影响全局环境的repo-local安装方法；skill只声明和说明安装，不实际运行安装。
**No hardcoded ecosystem artifacts原则**：项目初始化skill不得在通用规则或静态检查中写死任何具体语言生态的文件名、目录名或配置名；所有生态相关artifact都必须来自用户输入、deepresearch、模板文档或模板实际生成结果。
**Template-derived validation原则**：静态检查验证的是“选定模板生成的结构是否完整并与论文实验目录正确合并”，不是验证某个预设技术栈文件清单是否存在。
**Role-based artifact naming原则**：skill内部规则使用功能角色描述文件，例如依赖声明、项目元数据、构建配置、源码布局、测试布局；具体文件名只在选定模板后由实际repo决定。
**Repo scaffold总原则**：这个skill负责把论文蓝图、experiment plan和coding plan转化为一个真实starter repo加论文实验目录的项目脚手架；它通过deepresearch现场选择并调用初始化方式生成基础代码库结构，配置可直接安装调用的依赖，记录reference-only sources，写清楚repo-local安装方法，再叠加固定实验目录、README、REFERENCES和harness/test说明文件，让后续具体实现skill在真实脚手架上继续推进。
