-- 1 三类住宅基础记述，不混入分析
SELECT id,subject,predicate,object FROM knowledge_units WHERE subject IN ('大师住宅','托尔滕排屋','外廊住宅') AND epistemic_status='来源明示' ORDER BY id;
-- 2 方法与项目责任并置，不证明过程因果
SELECT id,subject,predicate,object FROM knowledge_units WHERE subject='梅耶设计方法' OR predicate IN ('设计实施','设计领导') ORDER BY id;
-- 3 本文分析集中审辨
SELECT id,subject,predicate,object FROM knowledge_units WHERE epistemic_status='本文分析' ORDER BY id;
