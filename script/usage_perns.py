# -*- coding: utf-8 -*-
"""Usage_perNS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iZuRU6YNthKH3B1sFTgtHUgEHzDwXsHX
"""

#pip install pyspark
#pip install findspark

#import findspark
#findspark.init

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("New App").getOrCreate()

from pyspark.sql.types import *
Schema_UsageData = StructType(
    [StructField("namespace",StringType(),True),
     StructField("timestamp",StringType(),True),
     StructField("kubernetesPodNameKeyword",StringType(),True),
     StructField("kubernetesPodCpuUsageNodePct",DoubleType(),True),
     StructField("kubernetesContainerCpuLimitCores",DoubleType(),True),
     StructField("kubernetesContainerCpuRequestCores",DoubleType(),True),
     StructField("kubernetesPodCpuUsageLimitPct",DoubleType(),True),
     StructField("kubernetesPodMemoryUsageBytes",DoubleType(),True),
     StructField("kubernetesPodCpuUsageNanocores",DoubleType(),True),
     StructField("key",StringType(),True),
     StructField("enviromentName",StringType(),True),
     StructField("toDate",IntegerType(),True),]

)

UsageData = spark.read.csv("/data/usage_20211116.csv",schema=Schema_UsageData)
UsageData.show()
UsageData.count()

from pyspark.sql.functions import *
df1 = UsageData.groupBy('namespace', 'kubernetesPodNameKeyword').avg('KubernetesPodCpuUsageNanocores')
df1.show()
df1.count()

df2 = df1.groupBy('namespace').agg(sum('avg(KubernetesPodCpuUsageNanocores)').alias('namespaceWiseUsage'))
df2.show()
df2.count

df2.registerTempTable("namespaceUsage")
sql = """
select * , namespaceWiseUsage/(select sum(namespaceWiseUsage) from namespaceUsage) as percentUsage from namespaceUsage

"""
spark.sql(sql).show()
spark.sql(sql).count()
#namespaceUsage.count()