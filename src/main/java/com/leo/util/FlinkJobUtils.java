package com.leo.util;

import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * @author suyh
 * @since 2025-03-06
 */
@Slf4j
public class FlinkJobUtils {
    private static final String JOB_ID_PREV = "Job has been submitted with JobID ";

    public static String buildCohortJobSubmitCommand(String flinkHome, String jobJar, int dates, String pns) {
        return String.format("/bin/bash %s/bin/flink run -d -p 4 %s/%s --cds.flink.batch.date=%d --cds.flink.batch.pns=%s",
                flinkHome, flinkHome, jobJar, dates, pns);
    }

    public static String buildRealtimeJobSubmitCommand(String flinkHome, String jobJar, int dates, String pns) {
        return String.format("/bin/bash %s/bin/flink run -d -p 4 %s/%s --realtime.trend.batch.runtime.dates=%d --realtime.trend.batch.runtime.pns=%s",
                flinkHome, flinkHome, jobJar, dates, pns);
    }

    public static String buildRepetitionJobSubmitCommand(String flinkHome, String jobJar, int dates, String pns) {
        return String.format("/bin/bash %s/bin/flink run -d -p 4 %s/%s --cdap.batch.runtime.form-date=%d --cdap.batch.runtime.pns=%s",
                flinkHome, flinkHome, jobJar, dates, pns);
    }

    public static String flinkJobSubmit(String command) {
        String jobId = null;

        try {
            Process process = Runtime.getRuntime().exec(command);

            // 获取脚本的标准输出流
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                // System.out.println(line);
                if (line.startsWith(JOB_ID_PREV)) {
                    jobId = line.substring(JOB_ID_PREV.length()).trim();
                    log.debug("jodId: " + jobId);
                }
            }

            // 获取脚本的错误输出流
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            while ((line = errorReader.readLine()) != null) {
                // System.err.println(line);
            }

            // 等待脚本执行完成并获取退出状态码
            int exitCode = process.waitFor();
            log.info("脚本执行完成，退出状态码: " + exitCode);
            if (exitCode != 0) {
                return null;
            }

        } catch (IOException | InterruptedException e) {
            log.error("command: {} failed. jobId: {}", command, jobId, e);
        }

        return jobId;
    }

    public static boolean flinkClusterRestart(String flinkHome) {
        try {
            {
                String command = String.format("/bin/bash %s/bin/stop-cluster.sh", flinkHome);
                Process process = Runtime.getRuntime().exec(command);

                // 获取脚本的标准输出流
                BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    System.out.println(line);
                }

                // 获取脚本的错误输出流
                BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                while ((line = errorReader.readLine()) != null) {
                    System.err.println(line);
                }

                int exitCode = process.waitFor();
                log.info("停止flink 集群，退出状态码：{}", exitCode);
                if (exitCode != 0) {
                    return false;
                }
            }

            {
                String command = String.format("/bin/bash %s/bin/start-cluster.sh", flinkHome);
                Process process = Runtime.getRuntime().exec(command);
                int exitCode = process.waitFor();
                log.info("启动flink 集群，退出状态码：{}", exitCode);
                if (exitCode != 0) {
                    return false;
                }
            }

            return true;
        } catch (IOException | InterruptedException e) {
            log.error("shell exec failed.", e);
            return false;
        }
    }
}
