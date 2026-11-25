-- 比较三类住宅的生活关联；不是使用效果调查
SELECT id,subject,predicate,object,source_ids,locator FROM knowledge_units WHERE subject IN ('大师住宅','托尔滕排屋','外廊住宅');
-- 对照梅耶方法与集体项目，不能由比较推出直接因果
SELECT * FROM knowledge_units WHERE subject='梅耶设计方法' OR predicate IN ('设计实施','设计领导');
-- 单独审核8条研究解释
SELECT id,statement,source_ids,locator FROM knowledge_units WHERE epistemic_status='本文分析';
