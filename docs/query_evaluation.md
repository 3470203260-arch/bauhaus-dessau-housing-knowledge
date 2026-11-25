# 查询与知识发现能力的实际检验

本记录来自现有SQLite实际查询，不增加知识元或关系统计；不等同史实已获一手认证。

## 三类住宅的基础记述

```sql
SELECT id,subject,predicate,object FROM knowledge_units WHERE subject IN ('大师住宅','托尔滕排屋','外廊住宅') AND epistemic_status='来源明示' ORDER BY id;
```

实际返回9条：K035、K036、K037、K038、K039、K040、K042、K043、K044

## 方法与项目责任并置

```sql
SELECT id,subject,predicate,object FROM knowledge_units WHERE subject='梅耶设计方法' OR predicate IN ('设计实施','设计领导') ORDER BY id;
```

实际返回8条：K007、K008、K009、K010、K011、K012、K042、K043

## 研究解释单独审核

```sql
SELECT id,subject,predicate,object FROM knowledge_units WHERE epistemic_status='本文分析' ORDER BY id;
```

实际返回8条：K045、K046、K047、K048、K049、K050、K051、K052

## 可以解释什么

第一项使同一来源中的三类空间关系能够按相同问题检索；第二项把方法研究与项目责任放在一起，暴露过程证据尚未衔接的缺口；第三项把8条解释与44条来源明示分开，便于针对解释过度进行审核。

不能由这三项查询推出隐性师承、项目成功率或真实住户体验。知识发现体现在问题关系和证据缺口的显现，不冒充新发现的历史事实。