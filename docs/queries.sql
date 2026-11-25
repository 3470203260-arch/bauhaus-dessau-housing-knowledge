-- 比较主体与获得方式
SELECT id,subject,predicate,object,source_ids,locator FROM knowledge_units WHERE subject IN ('特尔滕排屋','外廊住宅') AND predicate IN ('设计实施','获得方式');
-- 区分设想和实现
SELECT * FROM knowledge_units WHERE predicate IN ('计划配置','未能实现','实现程度','经历变化');
-- 返回研究解释的证据链
SELECT id,statement,source_ids,locator FROM knowledge_units WHERE epistemic_status='本文分析';
