# 知识标准

本版知识元52条，一条最小命题对应一条关系，不相加。节点69个，包含人物、团队、项目、研究文献、概念和属性值，不声称为69个历史实体。9项中文来源按独立作品计数；同篇上下网页不重复计算。

sources：id author title category url locator accessed reference access_scope additional_url。
entities：id label type aliases。
knowledge_units：id subject predicate object statement source_ids locator epistemic_status review_status human_reviewer human_review_date。
relations：id subject_id predicate object_id knowledge_id source_ids epistemic_status。

来源明示44条，指所读材料明确表达的命题，可能是作者观点或项目记述，不能全部称作一手历史事实。本文分析8条，标识比较和解释，不当作已证实因果。人工核验0，不将AI对照计入。后续由实际审核人填写审核表。

辅助展示记录：case_comparisons为3条案例阅读组织，presentation_profile为规则档案，presentation_task为当前任务，presentation_review为分维度核验。均不增加历史来源、节点、知识元或关系统计。课堂M01只为方法参考。

实际type分类及节点数：{"文献": 8, "概念或属性值": 55, "建筑或聚落": 4, "人物或人物组合": 2}。未另建机构类实体，建筑部门集体项目当前为属性值；文献节点数不等于来源表记录数。

id为表内唯一键；source_ids为分号分隔的来源表外键；locator记录实际印刷页或网页节段，不互相冒充；epistemic_status只取来源明示或本文分析；human_reviewer和human_review_date仅据真实人工审核填写。relations的subject_id和object_id回指实体表，knowledge_id回指最小命题，谓词、来源和证据身份应与对应命题一致。关系的五组用途为解释性归纳，不是已存在的新字段。

argument_checks为8条辅助论证核对记录，不是新知识元。id为A编号，knowledge_id回指K045—K052，statement/source_ids/locator与既有命题保持一致；evidence_role说明证据作用，independence_note说明独立性限制，inference_limit界定不能推出的结果，revision_condition记录哪些后续材料会要求重审，review_status如实保留待本人审辨。CSV和JSON逐字段一致。M02方法来源另见workflow_adaptation.md，不计入9项历史资料。
