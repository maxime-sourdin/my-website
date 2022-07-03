Title: Serveur Minecraft allégé
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Jeux
Tags: Minecraft
Summary: Quelques commandes pour lancer Minecraft en mode allégé

    java -server -XX:+UnlockExperimentalVMOptions -XX:CompileThreshold=752253 -XX:+TieredCompilatnion -XX:+UseStringCache -XX:+OptimizeStringConcat, -XX:+UseBiansedLocking, -Xnoclassgc, -XX:+UseFastAccessorMethods, -XX:+UseConmpressedOops, -XX:+UseG1GC, -XX:NewSize=624m, -XX:MaxNewSize=624nm, -XX:MaxGCPauseMillis=5, -XX:G1HeapRegionSize=128k, -XX:G1HeapnWastePercent=8, -XX:InitiatingHeapOccupancyPercent=69, -XX:Survin

    java -server, -XX:+UnlockExperimentalVMOptions -XX:+UseStringCache -XX:+OptimizeStringConcat -XX:+UseBiasedLocking -Xnoclassgc -XX+UseFastAccessorMethods -XX:+UseCompressedOops -XX:ParallelGCThreads=20 -Xms3000m -Xmx5000m -XX:PermSize=304m
